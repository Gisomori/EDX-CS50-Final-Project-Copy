#include <stdio.h>
#include <cs50.h>
#include <string.h>

void pyramid(int input_pyramid_height);
int main(void)
{
    int input_pyramid_height;
    do
    {
        //  printf("Please enter fitting integer: ");
         printf("Height: ");
         input_pyramid_height = get_int();
    }
    while(input_pyramid_height < 0 || input_pyramid_height > 23);
    if(input_pyramid_height >= 0 && input_pyramid_height < 24)
    {
        pyramid(input_pyramid_height);
    }
}
void pyramid(int input_pyramid_height)
{

    string spaces = " ";
    string hashes = "#";
    for(int i = 1; i <= input_pyramid_height; i++)
        {
            
            
            int x = input_pyramid_height-i-1; 
            for(int space_generator = x ; space_generator>=0;space_generator--)
            {
                printf("%s",spaces);
            }
            for(int hash_generator = input_pyramid_height; hash_generator > x ;  hash_generator--)
            {
                printf("%s",hashes);
            }
            
            printf("\n");
        }
    
    
}