/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        
       for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);
        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    //initialize board
    int n = (d*d) - 1;
        
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                //only swap the second last and third last value if d is even, to give chance of winning
                if((d % 2== 0) && (n == 2))
                {
                    board[i][j] = 1;
                } 
                else if((d % 2 == 0) && (n == 1)) 
                {
                    board[i][j] = 2;
                }
                //keep iterating
                else 
                {
                    board[i][j] = n;
                }
                //decrease number iterator, to ensure highest to lowest
                n--;
            }
                
        }

}


/**
 * Prints the board in its current state.
 */
void draw(void)
{
    //draw board after each change
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                // 0 is my placeholder value, it is expressed as underscore.
                if(board[i][j]==0)
                {
                    printf(" _");
                    if (j < d - 1)
                    {
                        //put always between numbers a pipe
                        printf("|");
                    }
                }
                else
                {
                    //print all numbers with 2 spaces, to make it look good.
                    printf("%2i", board[i][j]);
                    if (j < d - 1)
                    {
                        //put always between numbers a pipe
                        printf("|");
                    }
                }
            }
            //make a new line, as the row is finished
            printf("\n");
        }
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    //search underscore tile, identify options , check if options have been selected via input, if not illegal, otherwise swap.
    
    //define underscore value, mine is 0, track its row and col location. Also allocate vars for row and col.
    int uc_tile = 0;
    int uc_tile_row;
    int uc_tile_col;
    
    //iterate through 2d array to find the location of the underscore variable. store the location when found.
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        if(board[i][j]==uc_tile){
            uc_tile_row = i;
            uc_tile_col = j;
        }
    }
    
    //generate options
    int valid_left = board[uc_tile_row][uc_tile_col-1];
    int valid_right = board[uc_tile_row][uc_tile_col+1];
    int valid_bottom = board[uc_tile_row+1][uc_tile_col];
    int valid_upper = board[uc_tile_row-1][uc_tile_col];
    
    //check if options have been set as input, if yes swap and return true, otherwise return false.
    if(tile == valid_left)
    {
        board[uc_tile_row][uc_tile_col-1] = uc_tile;
        board[uc_tile_row][uc_tile_col] = tile;
        return true;
        
    }
    else if(tile == valid_right)
    {
        board[uc_tile_row][uc_tile_col+1] = uc_tile;
        board[uc_tile_row][uc_tile_col] = tile;
        return true;
    }
    else if(tile == valid_upper)
    {
        board[uc_tile_row-1][uc_tile_col] = uc_tile;
        board[uc_tile_row][uc_tile_col] = tile;
        return true;
    }
    else if(tile == valid_bottom)
    {
        board[uc_tile_row+1][uc_tile_col] = uc_tile;
        board[uc_tile_row][uc_tile_col] = tile;
        return true;
    }
    else
    {
        return false;
    }
    //to ensure compiler that there is an end
    return false;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    //initialize winning configuration, first allocate space for array.
    int counter[(d*d)];
    
    //iterate to create winning configuration.
    for(int x = 0;x < (d*d) ;x++)
    {
        counter[x] = x+1;
    }
    //swap last value in array to 0.
    counter[(d*d)-1] = 0;
    
    //provide another counter for looping.
    int x = 0;
    //iterate through 2d array together with another counter and check if values are indeed in increasing order
    for(int i = 0; i < d; i++)
    {
        for(int j = 0; j < d; j++)
        {
            
            if(board[i][j] == counter[x])
            {
                x++;
            }
            //if at any stage the board configuration and winning configuration don't find, return false.
            else
            {
                return false;
            }
        }
    }
    //check if last value truly is 0, if yes return true, otherwise false.
    if(board[d][d]==0)
    {
        return true;
    }
    return false;
}
