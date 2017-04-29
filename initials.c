#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    //define var for string
    string input_name;
    do
    {
        //get string and put into var
        input_name = get_string();
    }
    while(input_name == NULL); //ensure it is not empty

    //define counting var
    int i = 0;
    while(input_name[i]!='\0') //run till the end of the string
    {
        if(i==0)//first char gets printed regardless, make that to upper initial
        {
            printf("%c",toupper(input_name[i]));
        }
        if(input_name[i]==' ')//get any following char after a space and transform into upper initial + print
        {
            printf("%c",toupper(input_name[i+1]));
        }
        
        i++;
    }
    printf("\n"); //make sure to start a new line
}