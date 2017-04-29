#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    //ensure only argc of 2 is accepted, otherwise return error with 1
    if(argc != 2){
        
        printf("Usage: /home/cs50/pset2/caesar <key>\n");
        return(1);
    }
    
    //ensure received string is transformed to int
    int key = atoi(argv[1]);
    //print request statement & ask for string
        printf("plaintext: ");
        string input_plaintext = get_string();
        
        //make use of array to store variable, 
        int i = 0;
        //dynamically identify length of str to define array size
        int n  = strlen(input_plaintext);
        int array_plain[n];
        int array_cipher[n];
        
        //create arrays for alphabet indices
        int big_abc = 65;
        int sml_abc = 97;
        int array_big_alpha[26]; 
        int array_sml_alpha[26];
        
        while(big_abc<=90)
        {
            array_big_alpha[big_abc-65] = big_abc;
            big_abc++;    
        }
        
        while(sml_abc<=122)
        {
            array_sml_alpha[sml_abc-97] = sml_abc;
            sml_abc++;
        }

        //print out ciphertext output
        printf("ciphertext: ");
        
        //iterate till the end of the string & store depending on char with or without shift
        while(input_plaintext[i]!='\0')
        {
            array_plain[i] = input_plaintext[i];
            
            if(isalpha(array_plain[i]))
            {
                if(isupper(array_plain[i]))
                {
                    //identify with alphabet array for big letters the necessary shift and print successfully
                    int x = 0;
                    while(array_big_alpha[x]!=array_plain[i])
                    {
                        x++;
                    }
                    
                    array_cipher[i] = array_big_alpha[(x + key) % 26];
                    printf("%c",array_cipher[i]);

                } 
                else {
                    //dito as with the big array (just for smaller)
                    int x = 0;
                    while(array_sml_alpha[x]!=array_plain[i])
                    {
                        x++;
                    }
                    
                    array_cipher[i] = array_sml_alpha[(x + key) % 26];
                    printf("%c",array_cipher[i]);
                    
                }
            }
            else { 
                //when no case applies do not change the char, and leave as is and then print successfully
                array_cipher[i] = array_plain[i];
                printf("%c",array_cipher[i]);
            }
            i++;
            
        }
        //don't forget to start a new line
        printf("\n");
        
}