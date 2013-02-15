boot:
	mov dx, 0		;Select COM1
	mov ah, 1 		;1 -> Serial print
	mov al, '!'
	int 14h		
	
run:				;Boot sequence done, do work
	hlt			;Here, just idle
	jmp run			;...forever

.done:
	ret
	
	times 510-($-$$) db 0	;
	dw 0xAA55