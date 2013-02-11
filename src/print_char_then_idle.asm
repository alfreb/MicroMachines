boot:
	mov ah, 0Eh 		;0Eh -> Teletype output
	mov al, '!'
	int 10h		
	
run:				;Boot sequence done, do work
	hlt			;Here, just idle
	jmp run			;...forever

.done:
	ret
	
	times 510-($-$$) db 0	;
	dw 0xAA55