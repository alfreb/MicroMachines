repeat:
	hlt
	jmp repeat
	
	times 510-($-$$) db 0	;
	dw 0xAA55