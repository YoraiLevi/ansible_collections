// ansible -m example_c localhost
// gcc example_c_src.c -o example_c
#include <stdio.h>

int main() {
    // Write C code here
    printf("{\"changed\": false}");

    return 0;
}