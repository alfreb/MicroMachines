repeat:				;Just a label
	xor eax,eax
	mov ax 0xffff
	call work
	rdtsc
	mov edx,eax
	xor eax,eax
	mov dx,ax
	rol ax
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
