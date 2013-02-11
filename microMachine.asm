boot:
	mov     dx, 0	;Select COM1:
        mov     al, '!'	;Character to transmit
        mov     ah, 1	;Transmit opcode
        int     14h
        test    ah, 80h	;Check for error
        jnz     SerialError


	;; 	mov ah, 0Eh 		;0Eh -> Teletype output
	;; 	mov al, '?'
	;; 	int 10h		
	
run:				;Boot sequence done, do work
	hlt			;Here, just idle
	jmp run			;...forever

SerialError:
	
	
	times 510-($-$$) db 0	;
	dw 0xAA55