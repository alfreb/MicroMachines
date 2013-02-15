boot:
	mov ah, 1 		;1 -> Serial write
	mov al, '!'
	int 14h			;14h-> Bios Serial port subsystem
	
run:				;Boot sequence done, do work
	hlt			;Here, just idle
	jmp run			;...forever

.done:
	ret
	
	times 510-($-$$) db 0	;
	dw 0xAA55