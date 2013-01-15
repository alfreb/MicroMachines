@ECHO OFF

qemu\qemu-system-x86_64.exe -L qemu\ -m 128 -hda BareMetal.img -soundhw pcspk -rtc base=localtime -M pc -smp 8 -name "BareMetal OS"
