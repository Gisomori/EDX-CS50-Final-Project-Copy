#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>




int main(int argc, char *argv[])
{
    //ensure only 1 argument is accepted, if more return error.
    if(argc != 2)
    {
        fprintf(stderr,"Usage: ./recover infile \n");
        return 1;
    }
    //Open input file, make space for address of file
    char *infile = argv[1];
    FILE * inptr = fopen(infile,"r");
    
    //ensure that file is not empty if it is, return error.
    if(inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n",infile);
        fclose(inptr);
        return 2;
    }
    
    //counts number file naming 
    int file_counter = 0;
    //keeps track whether initial file is detected
    int checker = 0;
    //create storage array
    uint8_t buffer[512];
    char filename[sizeof "100.jpg"];
    FILE * outptr = NULL;
    
    //iterate until file is finished
    do 
    {
        //read 512 blocks into buffer and store their size dynamically, til the end.
        int size_checker = fread(&buffer, 1, 512, inptr);
        
            //found beginning of a jpeg ? 
             if(buffer[0] == 0xff &&
                buffer[1] == 0xd8 &&
                buffer[2] == 0xff &&
                (buffer[3] == 0xe0 || buffer[3] == 0xe1))
            {  
                //found beginning
                
                // if first time, open file  
                if(checker==0)
                {
                    //set identifier to file open
                    checker = 1;
                    //create file name 
                    sprintf(filename, "%03d.jpg", file_counter);
                    //count file name +1
                    file_counter++;
                    //create file connection
                    outptr = fopen(filename,"w");
                    //write bytes
                    fwrite(&buffer, 1,size_checker,outptr);
                }
                //close file first, cause new jpeg found, then open file
                else {
                    //close previous writing file
                    fclose(outptr);
                    //reopen new writing connection with new file name and count +1
                    sprintf(filename, "%03d.jpg", file_counter);
                    file_counter++;
                    outptr = fopen(filename,"w");
                    fwrite(&buffer, 1,size_checker,outptr);
                }
            }
            else
            {   //check whether a file signature has been found beforehand, write then, as we are in the middle of the jpeg.
                if(checker==1)
                {
                     fwrite(&buffer, 1,size_checker,outptr);
                }
            }
        
}
while(!feof(inptr));
    

    fclose(inptr);
    fclose(outptr);
    return 0;
}

