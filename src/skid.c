#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <linux/perf_event.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

struct counter_value {
    uint64_t count;
    uint64_t enabled;
    uint64_t running;
};

static volatile sig_atomic_t interrupted;

static void handle_signal(int signo)
{
    interrupted = signo;
}

static int wait_child(pid_t child, int *status)
{
    while (!interrupted) {
        if (waitpid(child, status, 0) == child)
            return 0;
        if (errno != EINTR)
            return -1;
    }
    errno = EINTR;
    return -1;
}

static int start_child(pid_t *child, const char *benchmark)
{
    int status;
    pid_t parent = getpid();

    *child = fork();
    if (*child < 0)
        return -1;
    if (*child == 0) {
        /* a killed controller must not leave the benchmark running. */
        if (prctl(PR_SET_PDEATHSIG, SIGKILL) || getppid() != parent)
            _exit(126);
        if (ptrace(PTRACE_TRACEME, 0, NULL, NULL))
            _exit(126);
        raise(SIGSTOP);
        execl(benchmark, benchmark, NULL);
        _exit(127);
    }
    if (wait_child(*child, &status))
        return -1;
    if (!WIFSTOPPED(status) || WSTOPSIG(status) != SIGSTOP) {
        errno = ECHILD;
        return -1;
    }
    if (ptrace(PTRACE_SETOPTIONS, *child, NULL,
               PTRACE_O_EXITKILL | PTRACE_O_TRACEEXEC | PTRACE_O_TRACEEXIT))
        return -1;
    if (ptrace(PTRACE_CONT, *child, NULL, NULL))
        return -1;
    if (wait_child(*child, &status))
        return -1;
    if (!WIFSTOPPED(status) || (status >> 16) != PTRACE_EVENT_EXEC) {
        errno = ENOEXEC;
        return -1;
    }
    return 0;
}

static int open_counter(pid_t child, struct perf_event_attr *attr, int signo)
{
    struct f_owner_ex owner = { .type = F_OWNER_TID, .pid = child };
    int fd;

    fd = syscall(SYS_perf_event_open, attr, child, -1, -1, PERF_FLAG_FD_CLOEXEC);
    if (fd < 0)
        return -1;
    if (fcntl(fd, F_SETOWN_EX, &owner) || fcntl(fd, F_SETSIG, signo) ||
        fcntl(fd, F_SETFL, O_ASYNC | O_NONBLOCK)) {
        close(fd);
        return -1;
    }
    return fd;
}

static int read_counter(int fd, struct counter_value *value)
{
    if (ioctl(fd, PERF_EVENT_IOC_DISABLE, 0))
        return -1;
    if (read(fd, value, sizeof(*value)) != sizeof(*value)) {
        errno = EIO;
        return -1;
    }
    if (!value->running || value->running != value->enabled) {
        errno = EBUSY;
        return -1;
    }
    return 0;
}

static const char *measure(pid_t child, int fd, int signo, uint64_t period,
                           struct counter_value *value, uint64_t *ip)
{
    struct user_regs_struct regs;
    siginfo_t info;
    int status;

    /* ENABLE keeps counting after overflow, through the signal-delivery stop. */
    if (ioctl(fd, PERF_EVENT_IOC_RESET, 0) ||
        ioctl(fd, PERF_EVENT_IOC_ENABLE, 0))
        return "could not enable counter";
    if (ptrace(PTRACE_CONT, child, NULL, NULL))
        return "could not resume benchmark";
    if (wait_child(child, &status))
        return "could not wait for benchmark";
    if (!WIFSTOPPED(status))
        return "benchmark exited without an overflow stop";
    if ((status >> 16) == PTRACE_EVENT_EXIT) {
        unsigned long exit_status;

        if (period)
            return "benchmark exited before overflow notification";
        if (ptrace(PTRACE_GETEVENTMSG, child, NULL, &exit_status) || exit_status)
            return "benchmark exited unsuccessfully";
    } else {
        if (!period || WSTOPSIG(status) != signo ||
            ptrace(PTRACE_GETSIGINFO, child, NULL, &info) || info.si_fd != fd)
            return "benchmark stopped for a signal other than counter overflow";
    }
    if (read_counter(fd, value))
        return "counter did not run for the full measurement or could not be read";
    if (ptrace(PTRACE_GETREGS, child, NULL, &regs))
        return "could not read stopped registers";
    *ip = regs.rip;
    return NULL;
}

static int parse_number(const char *text, uint64_t *value)
{
    char *end;

    if (*text == '-')
        return -1;
    errno = 0;
    *value = strtoull(text, &end, 0);
    return errno || end == text || *end ? -1 : 0;
}

int main(int argc, char **argv)
{
    struct perf_event_attr attr = {0};
    struct counter_value value = {0};
    struct sigaction action = { .sa_handler = handle_signal };
    uint64_t numbers[5], ip = 0;
    const char *error = NULL;
    pid_t child = -1;
    int fd = -1, status, signo = SIGRTMIN + 4;
    FILE *output;

    if (argc != 8) {
        fprintf(stderr, "usage: skid-helper type config config1 config2 period output benchmark\n");
        return 2;
    }
    for (int i = 0; i < 5; i++) {
        if (parse_number(argv[i + 1], &numbers[i])) {
            fprintf(stderr, "invalid counter argument\n");
            return 2;
        }
    }
    if (numbers[0] > UINT32_MAX || numbers[4] == 1 || numbers[4] > INT32_MAX) {
        fprintf(stderr, "invalid counter type or period (use 2..2147483647)\n");
        return 2;
    }
    sigemptyset(&action.sa_mask);
    sigaction(SIGTERM, &action, NULL);
    sigaction(SIGINT, &action, NULL);
    attr.size = sizeof(attr);
    attr.type = numbers[0];
    attr.config = numbers[1];
    attr.config1 = numbers[2];
    attr.config2 = numbers[3];
    attr.sample_period = numbers[4];
    attr.disabled = 1;
    attr.pinned = 1;
    attr.exclude_kernel = 1;
    attr.exclude_hv = 1;
    attr.exclude_guest = 1;
    attr.wakeup_events = 1;
    attr.read_format = PERF_FORMAT_TOTAL_TIME_ENABLED | PERF_FORMAT_TOTAL_TIME_RUNNING;

    if (start_child(&child, argv[7])) {
        error = "could not stop benchmark at exec";
        goto out;
    }
    fd = open_counter(child, &attr, signo);
    if (fd < 0) {
        error = "could not open sampling event";
        goto out;
    }
    error = measure(child, fd, signo, attr.sample_period, &value, &ip);
    if (!error && value.count < attr.sample_period)
        error = "counter stopped below the requested period";
out:
    if (error) {
        fprintf(stderr, "%s", error);
        if (errno)
            fprintf(stderr, ": %s", strerror(errno));
        fputc('\n', stderr);
    }
    if (fd >= 0)
        close(fd);
    if (child > 0) {
        kill(child, SIGKILL);
        ptrace(PTRACE_CONT, child, NULL, SIGKILL);
        for (;;) {
            if (waitpid(child, &status, 0) < 0) {
                if (errno == EINTR)
                    continue;
                break;
            }
            if (WIFEXITED(status) || WIFSIGNALED(status))
                break;
            ptrace(PTRACE_CONT, child, NULL, SIGKILL);
        }
    }
    output = fopen(argv[6], "w");
    if (!output) {
        perror("could not write measurement");
        return 1;
    }
    if (error) {
        fprintf(output, "{\"error\":\"%s\"}\n", error);
    } else {
        fprintf(output, "{\"count\":%" PRIu64 ",\"skid\":%" PRIu64
                ",\"ip\":\"0x%" PRIx64 "\",\"enabled\":%" PRIu64
                ",\"running\":%" PRIu64 "}\n", value.count,
                (uint64_t)(attr.sample_period ? value.count - attr.sample_period : 0),
                ip, value.enabled, value.running);
    }
    if (fclose(output))
        return 1;
    return error ? 1 : 0;
}
