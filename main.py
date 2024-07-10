#  1. Fill the pg window with Sudoku Board i.e., Construct a 9×9 grid. 
# 2. Fill the board with default numbers. 
# 3. Assign a specific key for each operations and listen it. 
# 4. Integrate the backtracking algorithm into it. 
# 5. Use set of colors to visualize auto solving.
import button
import helper
import solver
import pygame as pg
import sudokum


"""
improvements
in hidden single, if i find a HS on a row, why am i checking col+cell? maybe have a shared list that is checked for len(1) -> stripping, or if not, refresh as i check other avenues
when logic is applied, have text saying which logic and where
"""

#import grid
grid = sudokum.generate(mask_rate=0.6)
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
print(grid)
grid = [[0, 0, 2, 0, 8, 0, 5, 1, 6], [4, 0, 0, 0, 1, 0, 8, 0, 0], [7, 0, 8, 0, 0, 0, 9, 0, 3], [0, 5, 0, 0, 0, 0, 3, 8, 9], [0, 4, 0, 5, 0, 3, 0, 0, 0], [0, 0, 0, 0, 9, 0, 7, 5, 0], [0, 0, 6, 7, 0, 0, 0, 3, 0], [1, 0, 3, 9, 0, 0, 0, 0, 0], [5, 7, 0, 6, 3, 0, 0, 9, 0]]
#set up main variables
pg.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
main_font = pg.font.Font(None, 72)

def import_sudoku():
    row = 0

#buttons
solve_button = button.Button(800, 100, "Solve!", 100, 50)

helper.update_puzzle(grid, screen)
run = True
take_notes = True
while run:
    found_candidate = False
    total_found = 0
    #bring total found to viewable 
    #add text to show which technique used
    import_sudoku()
    if solve_button.draw(screen):
        found_candidate, total_found = solver.solver_handler(grid, grid_original, screen, take_notes)
        take_notes = False

    # to handle quitting
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    # Update the game state
    pg.display.update()
pg.quit()

