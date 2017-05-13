/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>
#include <math.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    //define vars to loop through, create dummy var which runs endlessly   
    int infinite = 1;
    int left = 0;
    int right = n-1;
    //divide to find the middle 
    int middle = (left+right)/2;
    
    
    do
    {
        //every time after restart of loop define a new the middle, make left + 1 to ensure a 0 can be reached
        middle = ((left+1)+right)/2;
        
        //if middle reaches at any time 0, return false
        if(middle ==0){
            return false;
        }

            //check whether the middle, left or right are the values we are looking for,if yes return true, otherwise keep going
            if(values[middle]==value || values[left]==value || values[right] == value)
            {
                return true;
            }
            else {
                //if middle is lower than the value we are looking for , search in the right part of the array
                if(values[middle]<value)
                {
                    //ignoring the left part of the array
                    left = middle +1;

                    //exit if over time the left and right overlap
                    if(left > right){
                        return false;
                    }
                    //restart loop
                    continue;
                }
                //search in the left part of the array
                else {
                    //ignoring the right part of the array
                    right = middle -1;
                    //exit if over time the left and right overlap
                    if(right < left){
                        return false;
                    }
                    //restart loop
                    continue;
                }
            }
                
        
    }
    //count endlessly
    while(infinite>0);
    //to ensure compiler knows the function can reach an end.
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    //set swap counter to start repeat until loop
    int swap_counter = -1; 
    //set iterator of array and use mod n to make it endless
    int i = n;
    //define variable for intermediary storage during sort
    int storage;
    
    //initiate repeat until loop with if condition, and continue statement
    do
    {
        //reset swap counter to 0
        swap_counter =0;
        for(i = 0;i < n-1;i++){
            
            //if [i] of array is smaller than next element [i+1] do nothing, else swap them 
            if(values[i] < values [(i+1)])
            {
                
            }
            else {
                //swap elements of array when above condition turns into else
                swap_counter = swap_counter + 1;
                storage = values[i];
                values[i] = values[(i+1)];
                values[(i+1)] = storage;
            }
        }
        //decrease array size, as the last item is always sorted, hence it can be ignored
         n--;
         if(swap_counter != 0) 
         {
             //ensure continuation of the loop
             continue;
         }
    }
    //if not true, continue until it is
    while(swap_counter!=0);
    return;
}