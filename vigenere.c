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
    //ensure alphabet is being taken, otherwise return error
    for(int a = 0; a < strlen(argv[1]);a++)
    {
        if(isalpha(argv[1][a])==0)
        {   
         printf("Usage: /home/cs50/pset2/caesar <key> must be alphabetical: A-Z or a-z\n");
         return(1);
        }
    }
    
    //pass on argument and dynamically assign size
    string key = argv[1];
    int kn = strlen(key);
    int key_array[kn];
    
    //transform key to lower, as only index from ABC matters
    int i = 0;
    while(key[i]!='\0')
    {
        key_array[i] =  tolower(key[i]);
        //printf("%c\n",key_array[i]);
        i++;
        
    }

    //get string and create variables & ABC indices
    printf("plaintext: ");
    string input_plaintext = get_string();
    int n  = strlen(input_plaintext);
    int array_plain[n];
    int array_cipher[n];
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
    
    //figure out ABC index of key
    for(i = 0; i < kn;i++){
        int x = 0;
        while(array_sml_alpha[x]!=key_array[i])
        {
             x++;
        }
        key_array[i] = x ;
        //printf("%i\n",key_array[i]);
    }
      
    i = 0;//counts through the plaintext
    int m = 0;//counts only when the plaintexts needs to be altered and never exceeds size of Key via mod operator
    printf("ciphertext: ");
    //iterate till the end of the string & store depending on char with or without shift
    while(input_plaintext[i]!='\0')
    {
        array_plain[i] = input_plaintext[i];
        
        //Use size of key and new var to create a base line, avoid 0 division by adding up a base line
        m = (kn + m) % kn; 
        
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
                
                array_cipher[i] = array_big_alpha[(x + key_array[m]) % 26];
                printf("%c",array_cipher[i]);
                m++; //count 1 + key
            } 
            else {
                //dito as with the big array (just for smaller)
                int x = 0;
                while(array_sml_alpha[x]!=array_plain[i])
                {
                    x++;
                }
                
                array_cipher[i] = array_sml_alpha[(x + key_array[m]) % 26];
                printf("%c",array_cipher[i]);
                m++; //dito
            }
        }
        else { 
            //when no case applies do not change the char, and leave as is and then print successfully
            array_cipher[i] = array_plain[i];
            printf("%c",array_cipher[i]);
        }
        i++; //count to next char
        
    }
    //don't forget to start a new line
    printf("\n");
        
            
}