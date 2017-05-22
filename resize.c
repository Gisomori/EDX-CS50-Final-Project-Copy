/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    //ASK FOR N  modifier
    // ensure proper usage
    
    // remember n to shift and check if program satisfies all conditions
    
    int n = atoi(argv[1]);
    if (argc != 4|| n <= 0 || n > 100)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }


    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf_old;
    BITMAPFILEHEADER bf_new;
    fread(&bf_old, sizeof(BITMAPFILEHEADER), 1, inptr);

    bf_new = bf_old;
    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi_old;
    BITMAPINFOHEADER bi_new;
    fread(&bi_old, sizeof(BITMAPINFOHEADER), 1, inptr);

    bi_new = bi_old;
    
    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf_old.bfType != 0x4d42 || bf_old.bfOffBits != 54 || bi_old.biSize != 40 || 
        bi_old.biBitCount != 24 || bi_old.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    //redefine and update headers
    bi_new.biWidth *= n;
    bi_new.biHeight *= n;
    
    //define padding for old and new. Old ones and new ones ARE NOT THE SAME
    int old_padding = (4 - (bi_old.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (bi_new.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // define proper headers for new file
    bi_new.biSizeImage = (sizeof(RGBTRIPLE) * bi_new.biWidth  + new_padding) * abs(bi_new.biHeight);
    bf_new.bfSize = bi_new.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    
    fwrite(&bf_new, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    
    fwrite(&bi_new, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // write long for offset later in the fseek function, to repeat rows multiple times 
    long offset_var = bi_old.biWidth * sizeof(RGBTRIPLE);

    // iterate over infile's scanlines but repeat processes by N times to scale vertically.
    for (int i = 0, biHeight = abs(bi_old.biHeight); i < biHeight; i++)
    {
        
        // repeat n times to scale vertically properly
        for(int y = 0; y < n; y++)
        {
        
            // iterate over pixels in scanline
            for (int j = 0; j < bi_old.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
    
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
    
                // write RGB triple to outfile
                for(int x = 0; x < n;x++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
    
            // add padding to the new written line 
            for (int k = 0; k < new_padding; k++)
            {
                fputc(0x00, outptr);
            }
            
            //repeat n - 1 to go back to the beginning of the row in the infile
            if ((n - 1) > y )
            {
                fseek(inptr,-offset_var , SEEK_CUR);
            }
        }
        // skip over padding in infile, if any
        fseek(inptr, old_padding, SEEK_CUR);
    
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
