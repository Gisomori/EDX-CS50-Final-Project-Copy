/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


#define alpha_size (27)

// Trie node for dictionary
typedef struct dnode
{
     struct dnode *letter[alpha_size];
     // isLeaf is true if the node represents
     // end of a word
     bool isLeaf;
}
dnode;

// create dictionary node root
dnode * root ;

// count dictionary nodes/entries
int dnode_counter = 0;

// create recursive trie unloader function

void dnode_unload(dnode * trav)
{
    for(int y = 0; y < alpha_size; y++)
    {
        if(trav -> letter[y] != NULL)
        {
            dnode_unload(trav -> letter[y]);
        }
    }
    free(trav);
    return;
}


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    //set traversing node to the beginning
    dnode * trav = root;
    
    //loop through each char
    for(int x = 0;word[x] != '\0';x++)
    {
        char c = word[x];
        
        //if char is apostrophe handle it to position to 26
        if(c == '\'')
        {
           c = 123;
        }
        //if char leaf is non existent return false
        if(trav->letter[tolower(c) - 'a'] == NULL)
        {
            return false;
        }
        // continue deeper
        trav = trav->letter[tolower(c) - 'a'];
    }
    
    //if leaf is true , return true
    if(trav->isLeaf==true)
    {
        return true;
    }
    //otherwise don't 
    else
    {
        
        return false;
    }
    //return false
    return false;
}





//spawn new dnode for dictionary

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // TODO
    
    //initialize root and give it memory
    root = calloc(1,sizeof(dnode));
    
    //let it start off from root and traverse.
    dnode * trav = root;
    FILE *dict = fopen(dictionary,"r");
        if(dict== NULL)
    {
        printf("Dictionary empty \n");
        fclose(dict);
    }
    
    
    for(int c = fgetc(dict);c != EOF; c = fgetc(dict))
    {
        //coerce any char to lowercase
        c = tolower(c);
        //printf("%c: %i\n",c ,c);
        
        //check if char is in alphabet range
        if(c > 96 && c < 123){
            
            //check if char exists, if not 
            if(trav -> letter[c - 'a'] == NULL)
            {
                //create new node
                trav ->letter[c - 'a'] = calloc(1,sizeof(dnode));
                
            }
            
        trav = trav->letter[c - 'a'];
            
        }
        
        //any apostrophe in it ? 
        if(c == '\'')
        {
            if(trav -> letter[26] == NULL)
            {
                //create new node
                trav ->letter[26] = calloc(1,sizeof(dnode));
                
            }
            trav = trav->letter[26];
        }
        
        

        //did we find end of the line ? 
        if(c =='\n')
        {
            //set end of word 
            trav->isLeaf = true;
            
            dnode_counter++;
            //move back to the root
            trav = root;
        }

        
    }
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{

   return(dnode_counter);
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    dnode_unload(root);
    if(root->isLeaf==0)
    {
        return true;       
    }
    else 
    {
        return false;
    }
}
