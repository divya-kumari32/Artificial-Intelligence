############################################################
# CIS 521: Informed Search Homework
############################################################

student_name = "Divya Kumari"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import queue
import math
############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):

    #initialising the puzzle
    puzzle = []
    count = 1
    for i in range(rows):
        temp = []
        for j in range(cols):
            temp.append(count)
            count+=1

        puzzle.append(temp)

    puzzle[rows-1][cols-1] = 0
    return TilePuzzle(puzzle)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board   #returns board

    def perform_move(self, direction):

        for x in range(len(self.board)):
            if 0 in self.board[x]:
                row = x
                col = self.board[x].index(0)
        
        #if the move is in the upwards direction
        if direction == "up":
            if (row-1)>=0:
                temp = self.board[row-1][col]
                self.board[row-1][col] = self.board[row][col]
                self.board[row][col] = temp
                return True

        #if the move is in the downwards direction
        if direction == "down":
            if (row+1)<len(self.board):
                temp = self.board[row+1][col]
                self.board[row+1][col] = self.board[row][col]
                self.board[row][col] = temp
                return True
        
        #if the move is in the left direction
        if direction == "left":
            if (col-1)>=0:
                temp = self.board[row][col-1]
                self.board[row][col-1] = self.board[row][col]
                self.board[row][col] = temp
                return True

        #if the move is in the right direction
        if direction == "right":
            if (col+1)<len(self.board[0]):
                temp = self.board[row][col+1]
                self.board[row][col+1] = self.board[row][col]
                self.board[row][col] = temp
                return True

        return False

    def scramble(self, num_moves):
        
        #perform move randomly
        seq = ["up", "down", "left", "right"]
        for move in num_moves:
            dir = random.choice(seq)
            self.perform_move(dir)

    def is_solved(self):
        count = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if i is len(self.board)-1 and j is len(self.board[0])-1:    #first checks if the 0 is at the last row and column
                    if self.board[i][j] !=0:
                        return False
                    break
                if self.board[i][j] is not count:   #second, checks if all other tiles are placed correctly and have reached goal state
                    return False
                
                count+=1
        return True
                

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        seq = ["up", "down", "left", "right"]
        for move in seq:                            #performs moves in a sequence on the tile to produce children boards
            new_puzzle = self.copy()
            new_puzzle.perform_move(move)
            if new_puzzle.board != self.board:      #checks if the new board is not equivalent to the parent board
                yield (move, new_puzzle)

    # Required
    def iddfs_helper(self, depth, checked, moves):
        if depth is 0:
            return
        else:
            if self.is_solved():        #checks if base case
                yield moves

            if len(moves) < depth:          #as mentioned in the assignment question, checking that moves iteration doesn't get more than the reached depth

                for (move, new_puzzle) in self.successors():
                    newBoardVal = tuple(tuple(x) for x in new_puzzle.board)
                    if newBoardVal not in checked:          #checks if new board is not already checked
                        sub_checked = copy.copy(checked)
                        sub_moves = copy.copy(moves)
                        sub_checked.add(newBoardVal)
                        sub_moves.append(move)
                        if new_puzzle.iddfs_helper(depth, sub_checked, sub_moves):      #only goes inside if helper function it is yielding
                            solns = list(new_puzzle.iddfs_helper(depth, sub_checked, sub_moves))        #store solutions inside a list and go through it to yield each one by one
                            for step in solns:
                                yield step

    def find_solutions_iddfs(self):
        solutions = []
        depth = 0
        checked = set(tuple(tuple(x) for x in self.board))  

        while not solutions:
            solutions = list(self.iddfs_helper(depth, checked, [])) #call helper function to trigger the iddfs and get solutions
            depth += 1      #keep increasing depth until you find solution

        for solution in solutions:
            yield solution
        
    # Required
    def manhattan_distance_heuristic(self):
        heuristic = 0
        len_row = len(self.board)
        len_col = len(self.board[0])
        for i in range(len_row):            #calculate manhattan distance for each tile element from it's position
            for j in range(len_col):
                if self.board[i][j] != 0:
                    dr = (self.board[i][j] - 1) / len_col
                    dc = (self.board[i][j] - 1) % len_col
                    heuristic += abs(i - dr) + abs(j - dc)
        return heuristic

    def find_solution_a_star(self):
        pqueue = queue.PriorityQueue()          #declare priority queue that will sort your queue according to your fn_value
        fn_value = self.manhattan_distance_heuristic()
        puzzleArr = [[], self]                  #list to store moves and the board together to keep track of what moves happened on what board
        pqueue.put((fn_value, 0, puzzleArr))    #priority queue initialisation
        checked = {self}              
        while pqueue:       #while queue exists

            curr = pqueue.get()  

            currBoard = tuple(tuple(x) for x in curr[2][1].board)

            if curr[2][1].is_solved():          #check for base case
                return curr[2][0]

            if currBoard in checked:            #if board present in checked, forgo further steps
                continue
            else:
                checked.add(currBoard)          #if not in checked add it to the board
            
            for (move, new_puzzle) in curr[2][1].successors():
                newBoardVal = tuple(tuple(x) for x in new_puzzle.board)
                if newBoardVal not in checked:          #if the child successor is not in checked, evaluate heuristic value and cost to reach that child
                    fn_value = curr[1] + 1 + new_puzzle.manhattan_distance_heuristic()  #f(n) = g(n) + h(n)
                    cost = curr[1] + 1
                    moves = curr[2][0] + [move]
                    newPuzzleArr = [moves,new_puzzle]
                    pqueue.put((fn_value, cost, newPuzzleArr))       #add to queue

        return None

############################################################
# Section 2: Grid Navigation
############################################################

class GridNavigation(object):

    def __init__(self, start, goal, scene):
        #initialising the arguments
        self.location = start
        self.goal = goal
        self.scene = scene

    def perform_move(self, move):       

        #perform movin the grid according to argument passed 
        if move == "up" and self.location[0] > 0 and self.scene[self.location[0] - 1][self.location[1]] is False:
            self.location = (self.location[0] - 1, self.location[1])
            return True
        elif move == "down" and self.location[0] < len(self.scene) - 1 and self.scene[self.location[0] + 1][self.location[1]] is False:
            self.location = (self.location[0] + 1, self.location[1])
            return True
        elif move == "left" and self.location[1] > 0 and self.scene[self.location[0]][self.location[1] - 1] is False:
            self.location = (self.location[0], self.location[1] - 1)
            return True
        elif move == "right" and self.location[1] < len(self.scene[0]) - 1 and self.scene[self.location[0]][self.location[1] + 1] is False:
            self.location = (self.location[0], self.location[1] + 1)
            return True
        elif move == "up-left" and self.location[0] > 0 and self.location[1] > 0 and self.scene[self.location[0] - 1][self.location[1] - 1] is False:
            self.location = (self.location[0] - 1, self.location[1] - 1)
            return True
        elif move == "up-right" and self.location[0] > 0 and self.location[1] < len(self.scene[0]) - 1 and self.scene[self.location[0] - 1][self.location[1] + 1] is False:
            self.location = (self.location[0] - 1, self.location[1] + 1)
            return True
        elif move == "down-left" and self.location[0] < len(self.scene) - 1 and self.location[1] > 0 and self.scene[self.location[0] + 1][self.location[1] - 1] is False:
            self.location = (self.location[0] + 1, self.location[1] - 1)
            return True
        elif move == "down-right" and self.location[0] < len(self.scene) - 1 and self.location[1] < len(self.scene[0]) - 1 and self.scene[self.location[0] + 1][self.location[1] + 1] is False:
            self.location = (self.location[0] + 1, self.location[1] + 1)
            return True        

        return False

    def is_solved(self):
        if self.location == self.goal:  #check if current location equals goal
            return True

        return False

    def copy(self):
        return GridNavigation(copy.copy(self.location), self.goal, self.scene)

    def successors(self):
        seq = ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]
        for move in seq:        #performs moves in a sequence on the grid to produce children 
            new_scene = self.copy()
            if new_scene.perform_move(move):    #check if perform move is possible for the new scene and yield it if it is
                yield (move, new_scene.location, new_scene)

    def euclidean_distance_heuristic(self):
        heuristic = 0
        dx = (self.location[0] - self.goal[0])
        dy = (self.location[1] - self.goal[1])
        heuristic = math.sqrt( dx ** 2 + dy ** 2)    #calculate euclidean distance for each the current location from the goal location
        return heuristic

    def find_Astar(self):
        
        pqueue = queue.PriorityQueue()              #declare priority queue that will sort your queue according to your fn_value
        fn_value = self.euclidean_distance_heuristic()
        pqueue.put((fn_value, 0, [self.location], self))       #priority queue initialisation
        checked = {self}   

        while not pqueue.empty():   #check while your queue never gets empty

            curr = pqueue.get()  
            currGridVal = curr[3].location

            if curr[3].is_solved():     #checks base case
                return curr[2]

            if currGridVal in checked:   #checks if current grid's location is visited
                continue
            else:
                checked.add(currGridVal)    #if not visited, add it to checked
                 
            for (move, new_loc, new_scene) in curr[3].successors():
                if new_loc not in checked:      #if the new location (child) passed is not visited
                    seq = ["up", "down", "left", "right"]
                    moves = curr[2] + [new_loc]     #calculate moves by adding the parent ones with the new one
                    if move not in seq:
                        fn_value = curr[1] + math.sqrt(2) + new_scene.euclidean_distance_heuristic()    #f(n) = g(n) + h(n) -> for diagonals
                        cost = curr[1] + math.sqrt(2)
                        pqueue.put((fn_value, cost, moves, new_scene)) 
                    else:        
                        fn_value = curr[1] + 1 + new_scene.euclidean_distance_heuristic()       #f(n) = g(n) + h(n) -> for straight moves
                        cost = curr[1] + 1
                        pqueue.put((fn_value, cost, moves, new_scene))      #add to queue 

        return None

def find_path(start, goal, scene):
    grid = GridNavigation(start, goal, scene)
    return grid.find_Astar()

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class linearDisk(object):

    def __init__(self, length, n, grid):    

        #initialise grid and other values passed as arguments
        self.length = length
        self.n = n
        
        if grid is 0 or len(grid) is 0:
            self.grid = [0]*length
            for i in range(n):
                self.grid[i] = i+1
        elif len(grid) is length:
                self.grid = grid
        else:
            return 

    def perform_move(self, i, add):
        if (i+add) >= self.length or (i+add)<0:     #check if the additional steps are not out of bound
            return

        self.grid[i+add] = self.grid[i]             #exchange values 
        self.grid[i] = 0

    def is_distinct_solved(self):

        for i in range(self.length - self.n):       #check the starting of the grid for 0 values (null disks)
            if self.grid[i] != 0:
                return False

        for i in range(self.length-self.n, self.length):        #checks if the disks are distinctly passed
            if self.grid[i] != (self.length - i):
                return False

        return True

    def copy(self):
        return linearDisk(self.length, self.n, copy.copy(self.grid))

    def successors(self):

        for i in range(self.length):

            if self.grid[i] is not 0 and (i+1) < self.length and self.grid[i+1] is 0:       #check for the grid location immediately next to the current one
                new_grid = self.copy()
                new_grid.perform_move(i,1)
                move = (i,i+1)
                yield (move, new_grid)

            if self.grid[i] is not 0 and (i+2) < self.length and self.grid[i+1] is not 0 and self.grid[i+2] is 0:       #check for the grid location two disks away in the forward direction
                new_grid = self.copy()
                new_grid.perform_move(i,2)
                move = (i,i+2)
                yield (move, new_grid)

            if self.grid[i] is not 0 and (i-1) >= 0 and self.grid[i-1] is 0:            #check for the grid location immediately previous to the current one
                new_grid = self.copy()
                new_grid.perform_move(i,-1)
                move = (i,i-1)
                yield (move, new_grid)

            if self.grid[i] is not 0 and (i-2) >= 0 and self.grid[i-1] is not 0 and self.grid[i-2] is 0:        #check for the grid location two disks away in the reverse direction
                new_grid = self.copy()
                new_grid.perform_move(i,-2)
                move = (i,i-2)
                yield (move, new_grid)

    def heuristic(self):
        heuristic = 0
        for i in range(self.length):
            if self.grid[i] != 0:
                heuristic += abs(self.length - self.grid[i] - i - 1)        #calculate heuristic according to disks position on the grid
        return heuristic

    def find_Astar(self):
        gqueue = queue.PriorityQueue()          #declare priority queue that will sort your queue according to your fn_value
        fn_value = self.heuristic()             #calculate heuristic for base case
        diskArr = [[], self]                    #list to store moves and the board together to keep track of what moves happened on what board
        gqueue.put((fn_value, 0, diskArr))      #priority queue initialisation
        checked = {self}               

        while gqueue:                           #checks while your queue exists
            
            curr = gqueue.get()    
            currGrid = tuple(curr[2][1].grid)

            if curr[2][1].is_distinct_solved():         #checks if current popped of grid is solved
                return curr[2][0]     

            if currGrid in checked:                     #check if grid has been visited
                continue
            else:
                checked.add(currGrid)                   #add if grid has not been visited
            
            for (move, new_grid) in curr[2][1].successors():        #calculate child nodes
                newGridVal = tuple(new_grid.grid)                   
                if newGridVal not in checked:                       #if new grid is not visited calculate heuristic and cost
                    fn_value = curr[1] + 1 + new_grid.heuristic()   #f(n) = g(n) + h (n)
                    cost = curr[1] + 1
                    moves = curr[2][0] + [move]
                    gqueue.put((fn_value, cost, [moves, new_grid]))     #add to queue 

        return None

def solve_distinct_disks(length, n):
    p = linearDisk(length, n, 0)
    return p.find_Astar()

############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 3

feedback_question_2 = """
Iterative-deepening depth first search was the most challenging.
"""

feedback_question_3 = """
I had a lot of fun coding for A* algorithm questions. I wish we were provided more reading material on IDDFS.
"""
