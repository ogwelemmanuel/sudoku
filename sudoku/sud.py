import copy, sys, random

EMPTY_SPACE = '.'
GRID_LENGTH = 9
BOX_LENGTH = 3
FULL_GRId_SIZE = GRID_LENGTH * GRID_LENGTH

class SudokuGrid:
    def __init__(self, originalSetup):
        # original setup is a string of 81 characters of the puzzle
        # setup with numbers and periods (for the blank spaces).
        # see https://inventwithpython.com/sudokupuzzles.txt

        self.originalSetup = originalSetup
        # the state of the original sudoku is represented  by a dictionary
        # with (x,y) values of the number (as a string) at that same space.
        self.grid = {}
        self.resetGrid() #set the grid state to its original setup.
        self.moves = []

    def resetGrid(self):
        """Reset the state of the grid, tracked by self.grid,
        to the state in self.originalSetup"""
        for x in range(1, GRID_LENGTH):
            for y in range(1, GRID_LENGTH + 1):
                self.grid[(x,y)] = EMPTY_SPACE

        assert len(self.originalSetup) == FULL_GRId_SIZE
        i = 0 # i gose from 0 to 80
        y = 0 # y gose from 0 to 80
        while i < FULL_GRId_SIZE:
            for x in range(GRID_LENGTH):
                self.grid[(x,y)] = self.originalSetup[i]
                i += 1
            y += 1
        
    def makeMove(self, column, raw, number):
        """Place the number at the column (a letter fromAto I) and row
        (an integer from 1 to 9)on the grid."""
        x = 'ABCDEFGHI'.find(column) # Convert this to an integer
        y = int(row) - 1

        #check if the move is being made oon a given number:
        if self.originalSetup[y * GRID_LENGTH + x] != EMPTY_SPACE:
            return False
        
        self.grid[(x, y)] = number # Place this number on the grid.
        #we need to store a separate copy of the dictionary object:
        self.moves.append(copy.copy(self.grid))
        return True
    
    def undo(self):
        """set the current grid state to the previouse state
          in the self.moves list"""
        if self.moves == []:
            return #No state in the self.move so do nothing.
        
        self.moves.pop() # Remove the current state.

        if self.moves == []:
            self.resetGrid()
        else:
            #set the grid to the last move.
            self.grid = copy.copy(self.moves[-1])

    def display(self):
        """Display the current state of the grid on the screen."""
        #check each row:
        print(' A B C  D E F  G H I')#Display colum labels.
        for y in range(GRID_LENGTH):
            for x in range(GRID_LENGTH):
                if x == 0:
 
                    #Display row lable.
                    print(str(y + 1) + ' ', end='')

                print(self.grid[(x, y)] + ' ', end='')
                if x == 2 or x == 5:
                    #Display a vertical line.
                    print('| ', end='')
            print() #print a new line.
            
            if y == 2 or y == 5:
                #display a horizontal line;
                print('  -----+------+------')

    def isCompletSetOfNumbers(self, numbers):
        """return true if numbers contains the digits 1 through 9."""
        return sorted(numbers) == list('123456789')
    
    def isSolved(self):
        """Returns True is the curent grid is in solved state."""
        #Check each row:
        for row in range(GRID_LENGTH):
            rowNumbers = []
            for x in range(GRID_LENGTH):
                number = self.grid[(x, row)]
                rowNumbers.append(number)
            if not self.isCompletSetOfNumbers(rowNumbers):
                return False
            
        #check for column.
        for column in range(GRID_LENGTH):
            columnNumers = []
            for Y in range(GRID_LENGTH):
                number = self.grid[(column, y)]
                columnNumers.append(number)
            if not self.isCompletSetOfNumbers(columnNumers):
                return False
        #check each box:
        for boxx in (0, 3, 6):
            for boxy in (0, 3, 6):
                boxNumber = []
                for x in range(BOX_LENGTH):
                    for y in range(BOX_LENGTH):
                        number = self.grid[(boxx + x, boxy + y)]
                        boxNumber.append(number)
                if not self.isCompletSetOfNumbers(boxNumber):
                    return False
        return True

print('''Sudoku Puzzle, by Ogwel
      
Sudoku is a number placement logic puzzle game. A Sudoku grid is a 9x9 
grid of numbers. Try to place numbers in the grid such that every row,
column, and 3x3 box has the numbers 1 through 9 once and only once.

For example, here is a starting Sudoku grid and its solved form:

        5 3 . | . 7 . | . . .     5 3 4 | 6 7 8 | 9 1 2
        6 . . | 1 9 5 | . . .     6 7 2 | 1 9 5 | 3 4 8
        . 9 8 | . . . | . 6 .     1 9 8 | 3 4 2 | 5 6 7
        ------+-------+------     ------+-------+------
        8 . . | . 6 . | . . 3     8 5 9 | 7 6 1 | 4 2 3
        4 . . | 8 . 3 | . . 1 --> 4 2 6 | 8 5 3 | 7 9 1
        7 . . | . 2 . | . . 6     7 1 3 | 9 2 4 | 8 5 6
        ------+-------+------     ------+-------+------
        . 6 . | . . . | 2 8 .     9 6 1 | 5 3 7 | 2 8 4
        . . . | 4 1 9 | . . 5     2 8 7 | 4 1 9 | 6 3 5
        . . . | . 8 . | . 7 9     3 4 5 | 2 8 6 | 1 7 9
      ''')
input('press enter to begin...')

#Load the sudoku pazzle.txt file:
with open('sudokupuzzle.txt') as puzzleFile:
    puzzles = puzzleFile.readlines()
#remove the new lines at the end of each puzzle:
for i, puzzle in enumerate(puzzles):
    puzzles[i] = puzzle.strip()

grid = SudokuGrid(random.choice(puzzles))

while True:
    #Main game loop.
    grid.display()

    #check is puzzle is solved.
    if grid.isSolved():
        print('Congratulations! You solved the puzzle')
        print('Thank you for playing!')
        sys.exit()

    #Get the players action:
    while True: # keep asking untill a player enters a valid action
        print()# print a new line.
        print('Enter a move, or RESET, NEW, UNDO, ORIGINAL, or QUIT:')
        print('(for example, a move looks like "B4 9".)')

        action = input('>').upper().strip()

        if len(action) > 0 and action[0] in ('R', 'N', 'U', 'O', 'Q'):
            #player entered a valid action.
            break
        if len(action.split()) ==2:
            space, number = action.split()
            if len(space) != 2:
                continue
            column, row = space
            if column not in list('ABCDEFGHI'):
                print('There is no column', column)
                continue
            if not row.isdecimal() or not(1 <= int(row) <= 9):
                print('Ther is no row')
                continue
            if not (1 <= int(number) <= 9):
                print('select a number from 1 to 9, not ', number)
                continue
            break
    print()# print a newline.

    if action.startswith('R'):
        grid.resetGrid()
        continue
    if action.startswith('N'):
        #Get a new puzzle:
        grid = SudokuGrid(random.choice(puzzle))
        continue
    if action.startswith('U'):
        #Undo the last move.
        grid.undo()
        continue
    
    if action.startswith('O'):
        #View the original numbers:
        originalGrid = SudokuGrid(grid.originalSetup)
        print('The original grid looked like this:')
        originalGrid.display()
        input('Press enter to continue...')
    
    if action.startswith('Q'):
        #Quit the game.
        print('Thank you for playing!')
        sys.exit()

    #Handle the moves the players selected.
    if grid.makeMove(column, row, number) == False:
        print('You cannot overwrite the original grid\'s numbers.')
        print('Enter ORIGINAL to view the original grid.')
        input('press Enter to continue...')