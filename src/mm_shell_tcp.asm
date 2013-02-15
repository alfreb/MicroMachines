init:	
	mov     dx, 0		;Select COM1:
prompt:	
	call 	write_prompt
        
        test    ah, 80h		;Check for error
        jnz     SerialError

	;; Read one byte
	call	read_al
		
	;; Increment - for fun
	inc 	al
	
	;; Write it back out
	call 	write_al
	
	;; Read another bytes - expecting a newline
	call 	read_al
	
	;; Write an exclamation mark
        mov     al, '!'		
	call 	write_al
	call 	write_newline	

	;; Repeat forever
	jmp	prompt

write_al:			;Send whatever is on al
	mov     ah, 1		
	int 	14h
	ret

write_newline:
	mov 	al, 0xA
	call 	write_al
	ret

write_prompt:
	mov	al, '$'
	call 	write_al
	mov 	al, '>'
	call 	write_al
	ret
	
read_al:			;Read a byte into al
	call	wait_for_data	
	mov 	ah, 2		;Opcode for reading from serial
	int 	14h		;Interrupt bios
	ret			;Else, return

	
wait_for_data:			;Wait until the Data-available-flag (bit 8) is set.
	mov 	ah,3
	mov 	al,0
	int 	14h	
	bt	ax,8		;copy bit-flag from ax to carry-flag
	jnc	sleep_wait
	ret

	
sleep_wait:
	mov 	eax,10
	call 	sleep
	jmp	wait_for_data

sleep:
	hlt
	dec eax
	jnz sleep
	ret
	
SerialError:
	mov 	eax,999
	
	times 510-($-$$) db 0	;
	dw 0xAA55