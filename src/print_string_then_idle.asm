start:
	mov ax, 07C0h		; Set up 4K stack space after this bootloader
	add ax, 288		; (4096 + 512) / 16 bytes per paragraph
	mov ss, ax
	mov sp, 4096

	mov ax, 07C0h		; Set data segment to where we're loaded
	mov ds, ax


	mov si, text_string	; Put string position into SI
	call print_string	; Call our string-printing routine

run:				; Done printing
	hlt			; Do actions: here, just halt
	jmp run			; ...for ever


	text_string db '* MicroMachine Running! *', 0


print_string:			; Routine: output string in SI to screen
	mov ah, 0Eh		; int 10h 'print char' function

	.repeat:
	lodsb			; Get character from string
	cmp al, 0		; If null-byte found,
	je .done		; ...end of string
	int 10h			; Otherwise, print it
	jmp .repeat

	.done:
	ret


	times 510-($-$$) db 0	; Pad remainder of boot sector with 0s
	dw 0xAA55		; The standard PC boot signature