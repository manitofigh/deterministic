.ifndef ITERATIONS
.set ITERATIONS, 1
.endif

.if (ITERATIONS != 1) && (ITERATIONS != 2)
.error "ITERATIONS must be 1 or 2"
.endif

.text
.globl _start
_start:
    # eax stays zero so test sets zf=1 on each pass
    xor %eax, %eax
    mov $ITERATIONS, %ecx

counted_setup_loop:
    # test checks eax without changing it; the nop keeps test and jnz separate
    # https://stackoverflow.com/questions/33721204/test-whether-a-register-is-zero-with-cmp-reg-0-vs-or-reg-reg
    test %eax, %eax
    nop
    .rept 31                    # emit 31 conditional branches per pass
        jnz 1f                  # zf=1, so this branch is not taken
        nop
1:                              # 1f above means the next 1: label
    .endr
    dec %ecx
    jnz counted_setup_loop      # the 32nd branch repeats the loop when ecx is nonzero

    # exit directly so no other user-space conditional branches are counted
    xor %edi, %edi
    mov $60, %eax
    syscall

.section .note.GNU-stack,"",@progbits
