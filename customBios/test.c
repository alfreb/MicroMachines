#include <unistd.h>
#include <stdio.h>


int 
testAsm(void){

  int syscallNr=20;
  int toEbx=1;
  int toEcx=9;
  int toEdx=19;
  int result=0;

  asm volatile(
	       "mov %[syscall], %%eax;"
	       "mov %[ebxVal], %%ebx;"
	       "mov %[ecxVal], %%ecx;"
	       "mov %[edxVal], %%edx;"
	       "int $0x80;"
	       "mov %%eax, %[res];"
	       :[res] "=r" (result)
	       :[syscall] "r" (syscallNr),[ebxVal] "r" (toEbx),[ecxVal] "r" (toEcx),[edxVal] "r" (toEdx)
	       : "%eax","%ebx"
	       );

  printf("PID: %d\n\n", result);
  
  int a=39, b;
  asm ("movl %1, %%eax;"       
       "addl $3, %%eax;"
       "movl %%eax, %0;"
       :"=r"(b)        // output
       :"r"(a)         // input
       :"%eax"         // clobbered register
       );       
  
  return b;

}


int main(){
  return testAsm();
}
