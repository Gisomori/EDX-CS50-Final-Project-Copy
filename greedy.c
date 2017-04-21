#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

void pyramid(int input_pyramid_height);
int main(void)
{
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    float pay_in1;
    int coins_used = 0;
    int total_coins = 0;
    do
    {
         printf("O hai! How much change is owed?\n");
         pay_in1 = get_float();
    }
    while(pay_in1 < 0);
    int pay_in = roundf(pay_in1*100);
    
    if(pay_in >= quarter){ //
        coins_used = (pay_in / quarter);
        total_coins = coins_used + total_coins;
        pay_in = pay_in - (coins_used * quarter);
    }
    if(pay_in >= dime){ // 
        coins_used = (pay_in / dime);
        total_coins = coins_used + total_coins;
        pay_in = pay_in - (coins_used * dime); // 0.16 - 
    } 
    if(pay_in >= nickel){
        coins_used = (pay_in / nickel);
        total_coins = coins_used + total_coins;
        pay_in = pay_in - (coins_used * nickel);
    } 
    if(pay_in >= penny){
        coins_used = (pay_in / penny);
        total_coins = coins_used + total_coins;
        pay_in = pay_in - (coins_used * penny);
    }    
    int coins_output = total_coins;
    printf("%i\n",coins_output);
}