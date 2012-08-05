start:
	xor eax,eax
	rdtsc
	mov edx,eax
	xor eax,eax
	mov ax,dx
	sal eax,8
work:
	dec eax
	jnz work

	hlt
	jmp start	
		
	times 510-($-$$) db 0	;Fill rest of file with 0's
	dw 0xAA55		;Boot signature, indicating end of boot sector.
