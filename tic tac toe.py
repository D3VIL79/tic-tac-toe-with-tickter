import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.board = [None] * 9
        self.buttons = []
        self.mode = None
        self.ai_difficulty = 'easy'
        
        # Ask for game mode and difficulty
        self.ask_game_mode()
    
    def ask_game_mode(self):
        mode = simpledialog.askstring("Game Mode", "Choose game mode: 1 for Two-player, 2 for Single-player")
        if mode == '1':
            self.mode = 'two_player'
            self.create_widgets()
        elif mode == '2':
            difficulty = simpledialog.askstring("AI Difficulty", "Choose AI difficulty: easy, medium, hard")
            if difficulty not in ['easy', 'medium', 'hard']:
                difficulty = 'easy'
            self.ai_difficulty = difficulty
            self.mode = 'single_player'
            self.create_widgets()
        else:
            messagebox.showinfo("Invalid Input", "Invalid selection. Exiting.")
            self.root.quit()
    
    def create_widgets(self):
        for i in range(9):
            button = tk.Button(self.root, text='', font=('Arial', 24), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
    
    def on_button_click(self, index):
        if self.board[index] is None and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif None not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                if self.mode == 'single_player' and self.current_player == 'X':
                    # Schedule AI move after 1 second
                    self.root.after(1000, self.ai_move)
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_winner(self):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
            (0, 4, 8), (2, 4, 6) # Diagonals
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] is not None:
                return True
        return False

    def reset_game(self):
        for i in range(9):
            self.board[i] = None
            self.buttons[i].config(text='')
        self.current_player = 'X'
        if self.mode == 'single_player' and self.current_player == 'O':
            # Schedule AI move if AI should start first
            self.root.after(1000, self.ai_move)
    
    def ai_move(self):
        move = self.choose_ai_move()
        if move is not None:
            self.board[move] = 'O'
            self.buttons[move].config(text='O')
            if self.check_winner():
                messagebox.showinfo("Game Over", "Player O wins!")
                self.reset_game()
            elif None not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = 'X'
    
    def choose_ai_move(self):
        if self.ai_difficulty == 'easy':
            return self.easy_ai_move()
        elif self.ai_difficulty == 'medium':
            return self.medium_ai_move()
        elif self.ai_difficulty == 'hard':
            return self.hard_ai_move()
    
    def easy_ai_move(self):
        return random.choice(self.get_available_moves())
    
    def medium_ai_move(self):
        # Blocking opponent's winning move
        opponent = 'X'
        for move in self.get_available_moves():
            self.board[move] = opponent
            if self.check_winner():
                self.board[move] = ' '
                return move
            self.board[move] = ' '
        # If no blocking move, take a random move
        return self.easy_ai_move()
    
    def minimax(self, depth, is_maximizing):
        if self.check_winner():
            return -10 if is_maximizing else 10
        if None not in self.board:
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def hard_ai_move(self):
        best_move = None
        best_score = -float('inf')
        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    
    def get_available_moves(self):
        return [i for i, space in enumerate(self.board) if space is None]

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
