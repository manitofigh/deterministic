# counted setup branches followed by a long branch sled.
# the skid helper starts counting at this executable's entry, before _start runs.

.ifndef SETUP_ITERATIONS
.set SETUP_ITERATIONS, 3125
.endif
.ifndef SLED_PASSES
.set SLED_PASSES, 2000
.endif
.ifndef BRANCHES_PER_SLED_PASS
.set BRANCHES_PER_SLED_PASS, 64
.endif
.ifndef REPEATED_BRANCHES_TAKEN
.set REPEATED_BRANCHES_TAKEN, 0
.endif

.if SETUP_ITERATIONS < 1
.error "SETUP_ITERATIONS must be positive"
.endif
.if SLED_PASSES < 1
.error "SLED_PASSES must be positive"
.endif
.if BRANCHES_PER_SLED_PASS < 1
.error "BRANCHES_PER_SLED_PASS must be positive"
.endif
.if (REPEATED_BRANCHES_TAKEN != 0) && (REPEATED_BRANCHES_TAKEN != 1)
.error "REPEATED_BRANCHES_TAKEN must be 0 or 1"
.endif

.text
.p2align 5
.globl _start
_start:
    # keep eax at zero so each repeated branch has the same outcome.
    xor %eax, %eax
    # each setup iteration retires 31 repeated branches and one loop branch.
    mov $SETUP_ITERATIONS, %ecx

counted_setup_loop:
    # eax is zero, so zf becomes one and every repeated jnz falls through.
    test %eax, %eax
    nop                         # keep test separate from the first jnz.
    .rept 31
        jnz 1f                  # 1f is the next 1: label; zf=1, so execute the nop.
        nop
1:
    .endr
    # dec sets zf for the loop branch; the next test restores zf for the repeated branches.
    dec %ecx
    jnz counted_setup_loop      # this branch counts once per setup iteration.

    # with 3125 setup iterations, exactly 100000 conditional branches have retired.
    mov $SLED_PASSES, %edx

sled_loop:
    # reset zf because the preceding dec changed it at the end of the last pass.
    test %eax, %eax
    nop                         # keep test separate from the first sled branch.
first_sled_branch:
    # threshold 100001 targets this branch on the first pass.
    # later retired branches increase the count before the overflow signal stops the process.
    .rept BRANCHES_PER_SLED_PASS
        .if REPEATED_BRANCHES_TAKEN
            jz 1f               # zf=1: jump to the next 1: label and skip the nop.
        .else
            jnz 1f              # zf=1: fall through and execute the nop.
        .endif
        nop
1:
    .endr
    dec %edx
    jnz sled_loop               # add one counted loop branch to each sled pass.

    # exit with status zero if the benchmark finishes without an overflow stop.
    xor %edi, %edi
    mov $60, %eax
    syscall

.section .note.GNU-stack,"",@progbits
