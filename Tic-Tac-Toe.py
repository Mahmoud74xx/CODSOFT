import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")

        
        self.button_color = "#ededed"
        self.font_color = "black"                    # Color of the buttons
        self.button_hover_color = "#f3f6f4"

        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('Arial', 20, 'bold'), width=6, height=2,
                                               bg=self.button_color, fg=self.font_color,
                                               activebackground=self.button_hover_color,
                                               command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        self.reset_button = tk.Button(master, text='Reset', font=('Arial', 12, 'bold'), bg="#6fa8dc", fg="white",
                                      activebackground="#ff3333", command=self.reset_board)
        self.reset_button.grid(row=3, columnspan=3, pady=10)

        self.reset_board()

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text='', state=tk.NORMAL, bg=self.button_color)  # Reset button colors

        self.turn = 'X' if random.choice([True, False]) else 'O'
        if self.turn == 'X':
            self.ai_make_move()

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', state=tk.DISABLED)
            if not self.check_game_over():
                self.turn = 'X'
                self.ai_make_move()

    def ai_make_move(self):
        best_move = self.get_best_move()
        if best_move:
            row, col = best_move
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X', state=tk.DISABLED)
            self.check_game_over()
            self.turn = 'O'

    def get_best_move(self):
        best_val = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in self.get_empty_cells():
            self.board[move[0]][move[1]] = 'X'
            move_val = self.minimax(0, False, alpha, beta)
            self.board[move[0]][move[1]] = ' '

            if move_val > best_val:
                best_val = move_val
                best_move = move

            alpha = max(alpha, best_val)
            if alpha >= beta:
                break

        return best_move

    def minimax(self, depth, is_maximizing, alpha, beta):
        scores = {'X': 1, 'O': -1, 'Tie': 0}

        winner = self.check_winner()
        if winner is not None:
            return scores[winner]

        if self.is_board_full():
            return scores['Tie']

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_empty_cells():
                self.board[move[0]][move[1]] = 'X'
                eval = self.minimax(depth + 1, False, alpha, beta)
                self.board[move[0]][move[1]] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_empty_cells():
                self.board[move[0]][move[1]] = 'O'
                eval = self.minimax(depth + 1, True, alpha, beta)
                self.board[move[0]][move[1]] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return min_eval

    def check_winner(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != ' ':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            return self.board[0][2]

        return None

    def is_board_full(self):
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def get_empty_cells(self):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            winning_combination = None
            if winner in ['X', 'O']:
                if winner in self.board[0]:
                    winning_combination = [(0, i) for i in range(3) if self.board[0][i] == winner]  
                for col in range(3):
                    if all(row[col] == winner for row in self.board):
                        winning_combination = [(i, col) for i in range(3) if self.board[i][col] == winner]  
                if all(self.board[i][i] == winner for i in range(3)):
                    winning_combination = [(i, i) for i in range(3) if self.board[i][i] == winner]  
                if all(self.board[i][2 - i] == winner for i in range(3)):
                    winning_combination = [(i, 2 - i) for i in range(3) if self.board[i][2 - i] == winner]  

                if winning_combination:
                    for row, col in winning_combination:
                        self.buttons[row][col].config(bg="#acfba0")  

                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.reset_board()
                return True
        
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_board()
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
