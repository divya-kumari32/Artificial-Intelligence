############################################################
# CIS 521: Uninformed Search Homework
############################################################

student_name = "Divya Kumari"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math as m
import random
import copy

############################################################
# Section 1: N-Queens
############################################################
def num_placements_all(n):
    #returning all combinations of n*nCn
    board = n*n
    num = m.factorial(board)
    den1 = m.factorial(n)
    den2 = m.factorial(board - n)
    res = num / (den1 * den2)
    return res

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):

    #looping through the board twice, the idea is fix ith queen and loop through other queens to check for validity of board
    for i in range(len(board)):
      if board.count(board[i]) > 1:
        return False
      for j in range(len(board)):
        if i != j :
          if abs(board[i]-board[j]) == abs(j-i):
            return False

    return True

def n_queens_helper(n, validSolutions, board):

    #if the len of the solutions board is equal to it's length, it means all queens have been placed
    if len(board) == n:
      validSolutions.append(board)
      return 
    
    #recursive function that passes a new board as an argument and checks it's validity each time and loops further if final state is not reached
    for i in range(n):
      newBoard = board + [i]
      if n_queens_valid(newBoard):
        n_queens_helper(n, validSolutions, newBoard)

    return validSolutions

def n_queens_solutions(n):
    validSolutions = []
    board = []
    n_queens_helper(n, validSolutions, board)  #helper function updates 'validSolutions' variable with all the possible solution boards
    return validSolutions

############################################################
# Section 2: Lights Out
############################################################
class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]

        #checks for values in the same column but row below/above and for same row but columns left/right
        if row-1>=0:
            self.board[row-1][col] = not self.board[row-1][col]
        if col-1>=0:
            self.board[row][col-1] = not self.board[row][col-1]
        if row+1<len(self.board):
            self.board[row+1][col] = not self.board[row+1][col]
        if col+1<len(self.board[0]):
            self.board[row][col+1] = not self.board[row][col+1]

    def scramble(self):

        #iterates through each value of matrix and decides through probability if move is to be performed or not
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        #board is solved if all values in the board are set to false
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] is True:
                    return False

        return True

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for i in range(len(self.board)):
          for j in range(len(self.board[0])):
            new_puzzle = self.copy()
            new_puzzle.perform_move(i, j)
            move = (i,j)
            yield (move, new_puzzle.copy())

    def backtrack(self, soln, checked):
        moves = []
        currVal = [soln, None]
        #backtrack thru the latest solution board to the initial board and add subsequent moves to list
        start = tuple(tuple(x) for x in self.board) 
        while currVal[0] != start:
            currVal = checked[currVal[0]]
            moves.append(currVal[1])

        return moves

    def find_solution(self):

      if self.is_solved():  #incase the initial state of the board is solved
        return []

      puzzle_queue = [] 
      start_board = LightsOutPuzzle(self.board)
      puzzle_queue.append(start_board)  #initializing queue with initial board
      startVal = tuple(tuple(x) for x in self.board)
      checked = {}  #dictionary that maintains visited boards and subsequent moves leading to that board as tuples
      checked[startVal] = (None, None)

      while puzzle_queue:

          #get first board out of the queue and make it the current board
          curr = puzzle_queue.pop(0)  
          currBoard = curr.get_board()
          currBoardVal = tuple(tuple(x) for x in currBoard)

          #look for all successors of current board
          for move, new_puzzle in curr.successors():
            newBoardVal = tuple(tuple(x) for x in new_puzzle.board)

            #if successive board not visited put it in checked and check if it's solvable
            if newBoardVal not in checked:
                checked[newBoardVal] = (currBoardVal, move)
                if new_puzzle.is_solved():
                    moves = self.backtrack(newBoardVal, checked)  #backtrack to get all moves associated with solution board 
                    return moves

                puzzle_queue.append(new_puzzle) #append to queue if new board successor is not the solution

      return None

def create_puzzle(rows, cols):
    arr = []
    for i in range(rows): 
        temp = []
        for j in range(cols): 
            temp.append(False)

        arr.append(temp)

    return LightsOutPuzzle(arr)

############################################################
# Section 3: Linear Disk Movement
############################################################
class linearDisk(object):

    def __init__(self, length, n, grid):
      self.length = length
      self.n = n
      #initialise grid with disks and put 0 incase disk ont present at grid position
      if grid is 0 or len(grid) is 0:
        self.grid = [0]*length
        for i in range(n):
          self.grid[i] = i+1
      elif len(grid) is length:
        self.grid = grid
      else:
        return 

    def is_identical_solved(self):
      
      #loop through the first (length - n) positions to see if a disk is present
      for i in range(self.length-self.n):
        if self.grid[i] is not 0:
          return False
      
      return True

    def is_distinct_solved(self):
      
      #loop through the (length - n) positions to see if a disk is present
      for i in range(self.length-self.n, self.length):
        if self.grid[i] != (self.length - i):
          return False
      
      return True

    def copy(self):
      return linearDisk(copy.deepcopy(self.length), copy.deepcopy(self.n), copy.deepcopy(self.grid))

    def perform_move(self, i, add):
      if (i+add) >= self.length or (i+add)<0:
        return

      self.grid[i+add] = self.grid[i]
      self.grid[i]=0
    
    def successors(self):
      for i in range(self.length):
        #if disk is present in the next position
        if self.grid[i] is not 0 and (i+1) < self.length and self.grid[i+1] is 0:
          new_grid = self.copy()
          new_grid.perform_move(i,1)
          move = (i,i+1)
          yield (move, new_grid)

        #if disk is present in the next to next position
        if self.grid[i] is not 0 and (i+2) < self.length and self.grid[i+1] is not 0 and self.grid[i+2] is 0:
          new_grid = self.copy()
          new_grid.perform_move(i,2)
          move = (i,i+2)
          yield (move, new_grid)

        #if disk is present in the previous position
        if self.grid[i] is not 0 and (i-1) >= 0 and self.grid[i-1] is 0:
          new_grid = self.copy()
          new_grid.perform_move(i,-1)
          move = (i,i-1)
          yield (move, new_grid)

        #if disk is present in the revious to previous position
        if self.grid[i] is not 0 and (i-2) >= 0 and self.grid[i-1] is not 0 and self.grid[i-2] is 0:
          new_grid = self.copy()
          new_grid.perform_move(i,-2)
          move = (i,i-2)
          yield (move, new_grid)

    def backtrack(self, soln, checked):
      moves = []
      currVal = [soln, None]
      #backtrack thru the latest solution grid to the initial grid and add subsequent moves to list
      start = tuple(self.grid)
      while currVal[0] != start:
        currVal = checked[currVal[0]]
        moves.append(currVal[1])

      return moves

def solve_identical_disks(length, n):

    grid_queue = []
    disks = linearDisk(length, n, 0)
    grid_queue.append(disks)  #create queue and append initial grid to queue
    startGridVal = tuple(disks.grid)
    checked = {}
    checked[startGridVal] = (None,None) #dict to store visiting grid as key and subsequent moves for the said grid as values in tuples

    while grid_queue:

      #pop first grid from queue and make it current grid
      curr = grid_queue.pop(0)
      currGridVal = tuple(curr.grid)

      if curr.is_identical_solved():
        return []

      #find successors for current grid
      for move, new_grid in curr.successors():
        newGridVal = tuple(new_grid.grid)

        #if grid is not visited, add to checked and check if valid solution
        if newGridVal not in checked:
          checked[newGridVal] = (currGridVal, move)
          if new_grid.is_identical_solved():
            moves = disks.backtrack(newGridVal, checked)
            moves.reverse()
            return moves  #return moves which is the valid solution

          grid_queue.append(new_grid) #append to queue if grid not visited and not valid solution

    return None


def solve_distinct_disks(length, n):

    #code is reused from the identical function 
    grid_queue = []
    disks = linearDisk(length, n, 0)
    grid_queue.append(disks)
    startGridVal = tuple(disks.grid)
    checked = {}
    checked[startGridVal] = (None,None)

    while grid_queue:

      curr = grid_queue.pop(0)
      currGridVal = tuple(curr.grid)

      if curr.is_distinct_solved():
        return []

      for move, new_grid in curr.successors():
        newGridVal = tuple(new_grid.grid)

        if newGridVal not in checked:
          checked[newGridVal] = (currGridVal, move)
          #check if solved distinctly
          if new_grid.is_distinct_solved():
            moves = disks.backtrack(newGridVal, checked)
            moves.reverse()
            return moves

          grid_queue.append(new_grid)

    return None


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
4 days
"""

feedback_question_2 = """
The 15 mark questions were extremely challenging and took the most time.
"""

feedback_question_3 = """
The assignnment had difficult questions that required using dynamic programming which is a very difficult area of programming. Wouldn't have changed anything. 
"""
