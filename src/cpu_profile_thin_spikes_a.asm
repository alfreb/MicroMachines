repeat:				;Just a label
	xor eax,eax
	dec ax
	shl eax,14
	call work

	rdtsc
	mov edx,eax
	xor eax,eax
	mov ax,dx
	shr ax,8
	call sleep

	jmp repeat		;Jump to label

sleep:
	hlt
	dec eax
	jnz sleep
	ret

work:
	dec eax
	jnz work
	ret
		
	times 510-($-$$) db 0	;Fill rest of file with 0's
	dw 0xAA55		;Boot signature, indicating end of boot sector.
