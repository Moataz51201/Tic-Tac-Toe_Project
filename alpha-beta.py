import tkinter as tk
from tkinter import messagebox
import random

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

class TicTacToeAI:
    def __init__(self):
        self.board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
        self.current_player = random.choice([PLAYER_X, PLAYER_O])

    def minimax(self, depth, alpha, beta, maximizing_player):
         if self.check_winner() == PLAYER_X:
             return -1
         elif self.check_winner() == PLAYER_O:
             return 1
         elif self.is_board_full():
             return 0

         if maximizing_player:
            max_eval = float('-inf')
            for i in range(3):
               for j in range(3):
                   if self.board[i][j] == EMPTY:
                       self.board[i][j] = PLAYER_O
                       eval = self.minimax(depth + 1, alpha, beta, False)
                       self.board[i][j] = EMPTY
                       max_eval = max(max_eval, eval)
                       alpha = max(alpha, eval)
                       if beta <= alpha:
                           break
            return max_eval
         else:
            min_eval = float('inf')
            for i in range(3):
               for j in range(3):
                  if self.board[i][j] == EMPTY:
                      self.board[i][j] = PLAYER_X
                      eval = self.minimax(depth + 1, alpha, beta, True)
                      self.board[i][j] = EMPTY
                      min_eval = min(min_eval, eval)
                      beta = min(beta, eval)
                      if beta <= alpha:
                          break
            return min_eval


    def best_move(self):
        best_val = float('-inf')
        best_move = (-1, -1)
        for i in range(3):
            for j in range(3):
               if self.board[i][j] == EMPTY:
                   self.board[i][j] = PLAYER_O
                   eval = self.minimax(0, float('-inf'), float('inf'), False)
                   self.board[i][j] = EMPTY
                   if eval > best_val:
                       best_move = (i, j)
                       best_val = eval
        return best_move

    def make_computer_move(self):
        if self.current_player == PLAYER_O:
            row, col = self.best_move()
            self.board[row][col] = PLAYER_O
            return row, col
        return None

    def check_winner(self):
        for i in range(3):
            if all(self.board[i][j] == PLAYER_X for j in range(3)) or \
                    all(self.board[j][i] == PLAYER_X for j in range(3)):
                return PLAYER_X
        if all(self.board[i][i] == PLAYER_X for i in range(3)) or \
                all(self.board[i][2 - i] == PLAYER_X for i in range(3)):
            return PLAYER_X

        for i in range(3):
            if all(self.board[i][j] == PLAYER_O for j in range(3)) or \
                    all(self.board[j][i] == PLAYER_O for j in range(3)):
                return PLAYER_O
        if all(self.board[i][i] == PLAYER_O for i in range(3)) or \
                all(self.board[i][2 - i] == PLAYER_O for i in range(3)):
            return PLAYER_O
        return None

    def is_board_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.ai = TicTacToeAI()
        self.buttons = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
        self.create_board_buttons()

    def create_board_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text='', font=('normal', 20), width=8, height=4,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_button_click(self, row, col):
        if self.ai.board[row][col] == EMPTY:
            self.ai.board[row][col] = PLAYER_X
            self.buttons[row][col].config(text=PLAYER_X, state=tk.DISABLED)
            if self.ai.check_winner() == PLAYER_X:
                messagebox.showinfo("Game Over", "You win!")
                self.reset_game()
            elif self.ai.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.ai.current_player = PLAYER_O
                self.make_computer_move()

    def make_computer_move(self):
        if self.ai.current_player == PLAYER_O:
            row, col = self.ai.make_computer_move()
            self.buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)
            if self.ai.check_winner() == PLAYER_O:
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_game()

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state=tk.NORMAL)
        self.ai = TicTacToeAI()
        self.make_computer_move()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    tic_tac_toe = TicTacToeGUI()
    tic_tac_toe.run()
