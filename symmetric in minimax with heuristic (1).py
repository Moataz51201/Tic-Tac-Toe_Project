import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
    
    def is_winner(self, player):
        for i in range(3):
            if all(self.board[i * 3 + j] == player for j in range(3)) or \
               all(self.board[i + j * 3] == player for j in range(3)):
                return True
        if all(self.board[i] == player for i in [0, 4, 8]) or \
           all(self.board[i] == player for i in [2, 4, 6]):
            return True
        return False
    
    def is_board_full(self):
        return ' ' not in self.board
    
    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_board_full()
    
    def get_available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']
    
    def make_move(self, move):
        if self.board[move] == ' ':
            self.board[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def undo_move(self, move):
        self.board[move] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'

def heuristic_evaluation(board, maximizing_player):
    # A heuristic: prioritize AI victories and block player victories.
    if maximizing_player and board.is_winner('O'):
        return 1
    elif not maximizing_player and board.is_winner('X'):
        return -1
    elif maximizing_player and board.is_winner('X'):
        return -1
    else:
        return 0

def generate_symmetric_states(board):
    # Generate symmetric states based on reflection and rotation.
    symmetric_states = [board]
    symmetric_states.append(board[::-1])  # Horizontal reflection
    symmetric_states.append([board[i * 3 + j] for j in range(3) for i in range(3)])  # Vertical reflection
    symmetric_states.append([board[2 - i * 3 + j] for j in range(3) for i in range(3)])  # Diagonal reflection

    return symmetric_states

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        
        self.game = TicTacToe()
        self.buttons = [None] * 9

        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                button = tk.Button(root, text='', font=('normal', 20), width=6, height=2,
                                   command=lambda idx=index: self.make_move(idx))
                button.grid(row=i, column=j)
                self.buttons[index] = button

    def make_move(self, index):
        if self.game.board[index] == ' ' and not self.game.is_game_over():
            self.game.make_move(index)
            self.update_board()
            if not self.game.is_game_over() and self.game.current_player == 'O':
                self.make_computer_move()
    
    def make_computer_move(self):
        move = get_best_move(self.game)
        self.game.make_move(move)
        self.update_board()

    def update_board(self):
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button['text'] = self.game.board[i]
            button['state'] = tk.DISABLED if self.game.board[i] != ' ' or self.game.is_game_over() else tk.NORMAL

        if self.game.is_game_over():
            self.display_result()

    def display_result(self):
        result = "It's a draw!"
        if self.game.is_winner('X'):
            result = "You win!"
        elif self.game.is_winner('O'):
            result = "You lose!"
        messagebox.showinfo("Game Over", result)
        self.root.quit()

def get_best_move(board):
    best_val = -math.inf
    best_move = -1
    for move in board.get_available_moves():
        board.make_move(move)
        move_val = minimax(board, 0, False)
        board.undo_move(move)
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

def minimax(board, depth, maximizing_player):
    if board.is_winner('X') or board.is_winner('O') or board.is_board_full():
        return heuristic_evaluation(board, maximizing_player)

    symmetric_states = generate_symmetric_states(board.board)
    if not maximizing_player:
        # Filtering Symmetric States Based on Piece Count:
        symmetric_states = [board for board in symmetric_states if maximizing_player == (board.count('O') > board.count('X'))]
    
    if maximizing_player:
        max_eval = -math.inf
        for move in board.get_available_moves():
            board.make_move(move)
            eval = minimax(board, depth - 1, False)
            max_eval = max(max_eval, eval)
            board.undo_move(move)
        return max_eval
    else:
        min_eval = math.inf
        for move in board.get_available_moves():
            board.make_move(move)
            eval = minimax(board, depth - 1, True)
            min_eval = min(min_eval, eval)
            board.undo_move(move)
        return min_eval

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
