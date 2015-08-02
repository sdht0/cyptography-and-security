Toddler's Bottle
================

Mommy, I wanna be a hacker!

Codes: https://gist.github.com/siddharthasahu/f46a965d7ce34a4b24cc

fd
--

A simple one.

* atoi(const char *str): Converts the char stream of digits to int 
* read(int fdes, void *buf, size_t nbyte): Reads `nbytes` bytes into `buf` variable from `fdes` file descriptor. [http://codewiki.wikidot.com/c:system-calls:read]

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
