/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */
 
#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // TODO: If ./generate does not have at least 1 additional entries supplied, it will print out the below message, and exit with 1.
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

    // TODO: convert argv[1] from string (which is the necessary component "n") to an int
    int n = atoi(argv[1]);

    // TODO: if a second additional command is added to ./generate, execute the function srand which is an initialization function, but first convert argv[2] to a long int
    if (argc == 3)
    {
        srand48((long) atoi(argv[2]));
    }
    else
    {
        srand48((long) time(NULL));
    }

    // TODO: generate random numbers till n, with our without predefined seed. Use the upper limit to not exceed integer range. Then print the result via printf, and exit with 0.
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}
