############################################################
# CIS 521: Sudoku Homework 
############################################################

student_name = "Divya Kumari, Renisa Pati"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import queue
import copy
import numpy as np

############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():

    cells = [(row, col) for row in range(9) for col in range(9)]

    return cells

def sudoku_arcs():
    
    cells = sudoku_cells()
    arcs = []
    for first_cell in cells:
        for second_cell in cells: 
            if first_cell != second_cell:
                if first_cell[0] == second_cell[0]:
                    arcs.append((first_cell, second_cell))
                    continue
                elif first_cell[1] == second_cell[1]:
                    arcs.append((first_cell, second_cell))
                    continue
                elif first_cell[0]//3 == second_cell[0]//3 and first_cell[1]//3 == second_cell[1]//3:
                    arcs.append((first_cell, second_cell))

    return arcs

def read_board(path):
    file = open(path)
    board = {}
    row = 0
    for line in file:
        for col in range(9):
            if line[col] == "*":
                board[(row, col)] = set(range(1, 10))
            else:
                board[(row, col)] = {int(line[col])}
        row+=1
            
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):

        cell1_set = self.board[cell1]
        cell2_set = self.board[cell2]
        if (cell1, cell2) in self.ARCS:
            if len(self.board[cell1]) != 1 and len(self.board[cell2]) == 1:
                if cell2_set.issubset(cell1_set):
                    s = list(self.board[cell2])
                    self.board[cell1].discard(s[0])
                    return True

        return False

    def infer_ac3(self):

        sudoku_queue = queue.Queue()
        for arc in self.ARCS:
            if len(self.board[arc[0]]) != 1 and len(self.board[arc[1]]) == 1:
                sudoku_queue.put(arc)
        
        while not sudoku_queue.empty():

            curr_arc = sudoku_queue.get()
            
            if self.remove_inconsistent_values(curr_arc[0], curr_arc[1]):
                if len(self.board[curr_arc[0]]) == 1:
                    for arc in self.ARCS:
                        if curr_arc[0] == arc[0] and curr_arc[1] != arc[1]:
                            sudoku_queue.put((arc[1], curr_arc[0]))

    def infer_improved(self):

        #flag to keep check if extra improvment is needed
        is_improved = True

        while is_improved:

            #for infer_ac3() to go as far as it can
            self.infer_ac3()

            #reset flag before starting inference
            is_improved = False

            #loop through each cell to check if they are unique or not 
            for cell in self.CELLS:

                #if cell has not been assigned a value yet 
                if len(self.board[cell]) > 1:

                    #loop through each value of the cell set
                    for value in self.board[cell]:

                        #another flag just to break incase value already exists in cell set, if true, set board cell value
                        flag = True         

                    #for all neighbours 

                        #ROW NEIGHBOURS
                        for row in range(9):
                            r_neighbour = (row, cell[1])  
                            if r_neighbour == cell:       
                                continue

                            #to check if value is unique,if not then break loop
                            if value in self.board[r_neighbour]:
                                flag = False   
                                break 

                        #sets the cell value if value not in row neighbours
                        if flag:
                            is_improved = True
                            self.board[cell] = set([value])
                            break

                        #COLUMN NIEGHBOURS
                        for col in range(9):
                            c_neighbour = (cell[0], col) 
                            if c_neighbour == cell:       
                                continue

                            #to check if value is unique,if not then break loop
                            if value in self.board[c_neighbour]:
                                flag = False     
                                break

                         #sets the cell value if value not in column neighbours
                        if flag:
                            is_improved = True
                            self.board[cell] = set([value])
                            break

                        #BLOCK NEIGHBOURS
                        curr_row = cell[0] // 3 * 3
                        curr_col = cell[1] // 3 * 3
                        for row in range(3):
                            for col in range(3):
                                block_neighbour = (curr_row + row, curr_col + col)
                                if block_neighbour == cell:   
                                    continue

                                #to check if value is unique,if not then break loop
                                if value in self.board[block_neighbour]:
                                    flag = False 
                                    break

                         #sets the cell value if value not in block neighbours
                        if flag:
                            is_improved = True
                            self.board[cell] = set([value])
                            break

    def infer_with_guessing(self):

        #if the board is solved, do nothing
        if self.is_solved():
            return self.board

        #for infer to go as far as possible
        self.infer_improved()

        for cell in self.CELLS:
                #if cell has not been assigned a value yet 
                if len(self.board[cell]) > 1:

                    #loop through each value of the cell set
                    for value in self.board[cell]:

                        #copy of the current board created
                        current_board = copy.deepcopy(self.board)

                        #current board's cell assigned with the value
                        self.board[cell] = {value}

                        #recursion call 
                        self.infer_with_guessing()

                        if self.is_solved():
                            break
                        else:       
                            self.board = current_board

                    return
    
    #method to check for solution state post recursive guessing
    def is_solved(self):
            
            #iterating through each cell, 
            #and returning False once a cell with undetermined value is encountered
            conditions = [[0 for x in range(9)] for y in range(27)]
            for cell in self.CELLS:
                if len(self.board[cell])!=1:
                    return False
                
                for value in self.board[cell]:
                    row_number = cell[0]
                    column_number = cell[1]
                    conditions[row_number][value-1] = 1
                    conditions[9+column_number][value-1] = 1
                    conditions[18+(row_number//3) * 3 + (column_number//3)][value-1] = 1
                
            for i in range(27):
                for j in range(9):
                    if (conditions[i][j] != 1):
                        return False

            return True
        
############################################################
# Section 2: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
the infer_gessuing part of the problem was a little confusing and was difficult to solve based on the pseudocode given in the book
"""

feedback_question_3 = """
infer_ac3 was fun to code and evaluating all test cases was interesting 
"""
