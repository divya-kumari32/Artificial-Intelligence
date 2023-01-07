############################################################
# CIS 521: adversarial_search
############################################################

student_name = "Divya Kumari"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
import random
import math

############################################################
# Section 1: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):

    #create board for dominoes game
    board = []
    for row in range(rows):
      temp = []
      for col in range(cols):
          temp.append(False)
    
      board.append(temp)
    
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    def __init__(self, board):

        #declares board and limit, best move and leaf nodes for keeping track for th parent board
        self.board = board
        self.limit = None
        self.best_Move = ()
        self.leaf_nodes = 0

    def get_board(self):
        return self.board

    def reset(self):

        #resets the board row-major order 
        for row in range(len(self.board)):
          for col in range(len(self.board[0])):
            if self.board[row][col] == True:
              self.board[row][col] = False
        
        return self.board

    def is_legal_move(self, row, col, vertical):

        #checks if the move is vertical and then checks if the next row is occupied
        if vertical:
          if row+1<len(self.board):
            if self.board[row][col] == self.board[row+1][col]:
              if self.board[row][col] != True:
                return True
        else:
          #checks if the move is not vertical, then checks if the next column is occupied
          if col+1<len(self.board[0]):
            if self.board[row][col] == self.board[row][col+1]:
              if self.board[row][col] != True:
                return True
        
        return False

    def legal_moves(self, vertical):
        #yield moves that can be made on the current board
        for i in range(len(self.board)):
          for j in range(len(self.board[0])):
              if self.is_legal_move(i, j, vertical):
                yield (i, j)

    def perform_move(self, row, col, vertical):

        #performs moves on the respective board given that the moves are legal
        if self.is_legal_move(row, col, vertical):
          if vertical:
            self.board[row][col] = True
            self.board[row+1][col] = True
          else:
            self.board[row][col] = True
            self.board[row][col+1] = True

    def game_over(self, vertical):
        
        #checks if no more legal moves are possible, then returns true if yes
        moves = list(self.legal_moves(vertical))
        if len(moves) == 0:
          return True
        else:
          return False
        
    def copy(self):
        return DominoesGame(copy.deepcopy(self.board))

    def successors(self, vertical):

        #provides successors for the current board row-major order by checking if the provided move is legal and if yes then performs the required change and returns the updated board 
        for i in range(len(self.board)):
          for j in range(len(self.board[0])):
            if self.is_legal_move(i, j, vertical):
              new_board = self.copy()
              new_board.perform_move(i, j, vertical)
              move = (i, j)
              yield (move, new_board)

    def get_random_move(self, vertical):
        seq = list(self.is_legal_move(vertical))
        return random.choice(seq)

    def evaluation_function(self, vertical):

        #utility function for the game
        max_moves = list(self.legal_moves(vertical))
        min_moves = list(self.legal_moves(not vertical))
        fn_value = len(max_moves) - len(min_moves)
        return fn_value

    def min_value(self, game, depth, alpha, beta, vertical):

        #if depth is equal to limit or game is over, it checks the number of nodes visited and return utility value of the board
        if depth > self.limit or game.game_over(vertical):
            self.leaf_nodes +=1
            return game.evaluation_function(not vertical)

        #initialising value for the current board state
        value = math.inf

        #checks for successors
        for move, new_board in game.successors(vertical):
            #calculates the move for the next player with new vertical 
            new_value = self.max_value(new_board, depth+1, alpha, beta, not vertical)
            #if new_value is less than the previous value, copy the new_value to the old value and evaluate beta
            if new_value < value:
                value = new_value
                # self.best_Move = move
                beta = min(beta, value)
            #if max node value is found stop searching through more nodes 
            if alpha >= value:
                return value

        return value

    def max_value(self, game, depth, alpha, beta, vertical):
      
        #if depth is equal to limit or game is over, it checks the number of nodes visited and return utility value of the board
        if depth > self.limit or game.game_over(vertical):
            self.leaf_nodes +=1
            return game.evaluation_function(vertical)

        #initialising value for the current board state
        value = -math.inf

        #checks for successors
        for move, new_board in game.successors(vertical):
            #calculates the move for the next player with new vertical 
            new_value = self.min_value(new_board, depth+1, alpha, beta, not vertical)
            #if new_value is less than the previous value, copy the new_value to the old value and evaluate alpha
            if new_value > value:
                value = new_value
                alpha = max(alpha, value)

                #only calculates best move if the node is at depth = 1 where max is the current player
                if depth == 1:
                    self.best_Move = move

            #if min node value is found stop searching through more nodes
            if beta <= value:
                return value
            
        return value
      
    def alpha_beta_search(self, game, vertical):

        #initialise alpha beta for pruning
        alpha = -math.inf
        beta = math.inf
        #start game
        value = self.max_value(game, 1, alpha, beta, vertical)
        return value

    # Required
    def get_best_move(self, vertical, limit):

        #initialise limit and 
        self.limit = limit
        #call alpha-beta-search to start game
        value = self.alpha_beta_search(self.copy(), vertical)
        return (self.best_Move, value, self.leaf_nodes)

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 12

feedback_question_2 = """
Writing the max_value and min_value function with respect to the dominoes game was the most difficult because there was less understanding of the game.
"""

feedback_question_3 = """
Writing the code for the game once I undertsood it was the most amazing aspect. It was challenging because you need to cover all scenarios.
"""
