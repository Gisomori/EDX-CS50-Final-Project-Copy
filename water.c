#include <stdio.h>
#include <cs50.h>


int main(void)
{
    printf("Hi, what is the duration of you showering in minutes?\n");
    int input_shower_duration = get_int();
    printf("You have inserted: %i minutes \n"
    "That equals to %i Bottles of water, shame on you!\n"
    ,input_shower_duration, input_shower_duration * 12);
    
    
}