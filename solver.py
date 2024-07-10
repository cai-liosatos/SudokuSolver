import pygame
from pygame.locals import *
import helper

def solver_handler(grid, untampered_grid, surface, inital_note):
    found_candidate = False
    #iterate over each row
    if inital_note:
        grid = note_taking(grid)
        helper.update_puzzle(grid, surface)
        return found_candidate, 0
    
    grid, found_candidate, total_found = naked_singles(grid)
    if found_candidate:
        helper.update_puzzle(grid, surface)
        return found_candidate, total_found


    grid, found_candidate, total_found = hidden_singles(grid)
    if found_candidate:
        helper.update_puzzle(grid, surface)
        return found_candidate, total_found

    return found_candidate, total_found

    #naked singles
    # grid = naked_singles(grid)
    # helper.update_puzzle(grid, surface)
    
    
def note_taking(grid):
    #grab each cell's info
    master_cell_list, cell_list_1, cell_list_2, cell_list_3 = [], [], [], []
    row_tracker = 0
    for row in grid:
        item_tracker = 0
        for item in row:
            if item > 0:
                if item_tracker < 3:
                    cell_list_1.append(item)
                elif item_tracker < 6:
                    cell_list_2.append(item)
                else:
                    cell_list_3.append(item)
            item_tracker += 1

        row_tracker += 1

        if (row_tracker) % 3 == 0:
            master_cell_list.append([cell_list_1] + [cell_list_2] + [cell_list_3])
            cell_list_1, cell_list_2, cell_list_3 = [], [], []
   
   #grabbing row and col info
    master_col_numbers = []
    cell_row_num = 0
    for r in range(0,9):
        cell_col_num = 0
        # grab row info
        row_grid = []
        row_numbers = [x for x in grid[r] if x > 0]
        for c in range(0,9):
            #check if col has been iterated through, if not pull that col's info
            col_numbers = []
            if len(master_col_numbers) == c:
                for col_num in range(0,9):
                    if isinstance(grid[col_num][c], int) and grid[col_num][c] > 0:
                        col_numbers.append(grid[col_num][c])   
                master_col_numbers.append(col_numbers) 
            else:
                col_numbers = [x for x in master_col_numbers[c]]

            # add that cell's info, depending on if its blank already or not
            if grid[r][c] == 0:
                non_candidates_set = set(list(col_numbers + row_numbers + master_cell_list[cell_row_num][cell_col_num]))
                candidates_list = [x for x in range(1,10) if x not in non_candidates_set]
                row_grid.append(candidates_list)
            else:
                row_grid.append(grid[r][c])
            
            if c > 0 and (c+1) % 3 == 0:
                cell_col_num += 1
        
        grid[r] = row_grid
        if r > 0 and (r+1) % 3 == 0:
            cell_row_num += 1

    return grid

def find_home_grid(row_index, row_cell_index):
    # [row start, row end, col start, col end]
    cell_list = [[[0, 2, 0, 2], [0, 2, 3, 5], [0, 2, 6, 8]], [[3, 5, 0, 2], [3, 5, 3, 5], [3, 5, 6, 8]], [[6, 8, 0, 2], [6, 8, 3, 5], [6, 8, 6, 8]]]
    if row_index < 3:
        row_cell_band = 0
    elif row_index < 6:
        row_cell_band = 1
    else:
        row_cell_band = 2

    if row_cell_index < 3:
        col_cell_band = 0
    elif row_cell_index < 6:
        col_cell_band = 1
    else:
        col_cell_band = 2
    return cell_list[row_cell_band][col_cell_band]

# grid=grid, 
# number=number to remove 
# row=row the found candidate was on
# row_index=the row num within grid 
# row_cell_index=the column within the cell (0-8) the number was found in
def trim_duplicate_candidates(grid, number, row, row_index, row_cell_index):
    #row
    for row_candidate_number_idx in range(9):
        if isinstance(row[row_candidate_number_idx], list) and number in row[row_candidate_number_idx]:
            row[row_candidate_number_idx].remove(number)

    #col
    for r in grid:
        if isinstance(r[row_cell_index], list) and number in r[row_cell_index]:
            r[row_cell_index].remove(number)
    
    #cell
    found_cell = find_home_grid(row_index, row_cell_index)
    for row_idx in range(found_cell[0], found_cell[1]+1):
        for col_idx in range(found_cell[2], found_cell[3]+1):
            if isinstance(grid[row_idx][col_idx], list) and number in grid[row_idx][col_idx]:
                grid[row_idx][col_idx].remove(number)

    return grid

def naked_singles(grid):
    identified_candidate = False
    total_found = 0
    for row_number in range(9):
        for candidates_idx in range(9):
            if isinstance(grid[row_number][candidates_idx], list) and len(grid[row_number][candidates_idx]) == 1:
                identified_candidate = True
                total_found += 1
                grid[row_number][candidates_idx] = grid[row_number][candidates_idx][0]
                #remove other candidates of same value in row
                grid = trim_duplicate_candidates(grid, grid[row_number][candidates_idx], grid[row_number], row_number, candidates_idx)

    return grid, identified_candidate, total_found

# grid=grid, 
# number=number to remove 
# row=row the found candidate was on
# row_index=the row num within grid 
# row_cell_index=the column within the cell (0-8) the number was found in
def candidate_strip(grid, master_candidates, row, row_index, row_cell_index):
    #row
    row_master_candidate = list(master_candidates)
    col_master_candidates = list(master_candidates)
    cell_master_candidates = list(master_candidates)
    found_candidate = False
    for row_candidate_number_idx in range(9):
        if isinstance(row[row_candidate_number_idx], list) and row_candidate_number_idx != row_cell_index:
            for candidate in row[row_candidate_number_idx]:
                if candidate in row_master_candidate:
                    row_master_candidate.remove(candidate)

    #col
    for r in range(9):
        if isinstance(grid[r][row_cell_index], list) and r != row_index:
            for candidate in grid[r][row_cell_index]:
                if candidate in col_master_candidates:
                    col_master_candidates.remove(candidate)
        
    #cell
    found_cell = find_home_grid(row_index, row_cell_index)
    for row_idx in range(found_cell[0], found_cell[1]+1):
        for col_idx in range(found_cell[2], found_cell[3]+1):
            if isinstance(grid[row_idx][col_idx], list) and not (row_idx == row_index and col_idx == row_cell_index):
                for candidate in grid[row_idx][col_idx]:
                    if candidate in cell_master_candidates:
                        cell_master_candidates.remove(candidate)
    
    value_to_trim = 0
    if len(row_master_candidate) == 1:
        grid[row_index][row_cell_index] = row_master_candidate[0]
        value_to_trim = row_master_candidate[0]
        found_candidate = True
    elif len(col_master_candidates) == 1:
        grid[row_index][row_cell_index] = col_master_candidates[0]
        value_to_trim = col_master_candidates[0]
        found_candidate = True
    elif len(cell_master_candidates) == 1:
        grid[row_index][row_cell_index] = cell_master_candidates[0]
        value_to_trim = cell_master_candidates[0]
        found_candidate = True

    if found_candidate:
        grid = trim_duplicate_candidates(grid, value_to_trim, grid[row_index], row_index, row_cell_index)
    return grid, found_candidate
                

def hidden_singles(grid):
    identified_candidate = False
    total_found = 0
    for row_number in range(9):
        for candidate_idx in range(9):
            if isinstance(grid[row_number][candidate_idx], list) and len(grid[row_number][candidate_idx]) > 1:
                grid, found_candidate = candidate_strip(grid, set(grid[row_number][candidate_idx]), grid[row_number], row_number, candidate_idx)
                if found_candidate:
                    identified_candidate = True
                    total_found += 1

    return grid, identified_candidate, total_found
















