import tkinter as tk
from tkinter import messagebox
from board import Board
from yoshi import Yoshi
from minimax import Minimax

class YoshisZonesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yoshi's Zones")
        self.root.geometry("800x900")
        self.board = Board()
        self.minimax = None
        self.yoshi_green = None
        self.yoshi_red = None
        self.buttons = {}
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        title = tk.Label(self.root, text="Yoshi's Zones", font=("Arial", 30, "bold"), pady=20)
        title.pack()
        
        levels = ["Principiante (Profundidad 2)", "Amateur (Profundidad 4)", "Experto (Profundidad 6)"]
        for level, depth in zip(levels, [2, 4, 6]):
            btn = tk.Button(self.root, text=level, font=("Arial", 18), width=25,
                          command=lambda d=depth: self.start_game(d))
            btn.pack(pady=10)

    def start_game(self, depth):
        self.clear_window()
        self.minimax = Minimax(depth)
        self.yoshi_green = Yoshi("Verde", self.board.random_start_position())
        self.yoshi_red = Yoshi("Rojo", self.board.random_start_position(exclude=self.yoshi_green.position))
        self.create_board()
        self.machine_turn()

    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                color = self.get_cell_color((row, col))
                btn = tk.Button(self.board_frame, width=4, height=2, bg=color,
                              command=lambda r=row, c=col: self.player_turn(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[(row, col)] = btn
        self.update_scores()

    def get_cell_color(self, pos):
        if pos == self.yoshi_green.position:
            return "dark green"
        if pos == self.yoshi_red.position:
            return "dark red"
        if pos in self.board.painted_colors:
            return "light green" if self.board.painted_colors[pos] == "Verde" else "light pink"
        if self.board.is_zone_cell(pos):
            return "light gray"
        return "white"

    def update_display(self):
        for pos, btn in self.buttons.items():
            btn.config(bg=self.get_cell_color(pos))
        self.update_scores()

    def machine_turn(self):
        _, move = self.minimax.minimax(self.board, self.yoshi_green, self.yoshi_red, 
                                     self.minimax.depth, True, float('-inf'), float('inf'))
        if move:
            self.yoshi_green.move(move, self.board)
            self.update_display()
            if not self.board.all_zones_painted():
                
                self.root.after(1000, self.check_game_status)
        else:
            self.check_game_status()

    def player_turn(self, row, col):
        pos = (row, col)
        if pos in self.yoshi_red.valid_knight_moves(self.board.size, self.board):
            self.yoshi_red.move(pos, self.board)
            self.update_display()
            if not self.board.all_zones_painted():
                self.root.after(500, self.machine_turn)
            else:
                self.show_winner()

    def check_game_status(self):
        if self.board.all_zones_painted():
            self.show_winner()
        else:
            
            if not self.yoshi_red.valid_knight_moves(self.board.size, self.board):
                messagebox.showinfo("Juego Terminado", "¡No hay movimientos posibles!")
                self.create_main_menu()

    def update_scores(self):
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack()
        tk.Label(self.score_frame, 
                text=f"Verde: {self.board.get_score('Verde')} - Rojo: {self.board.get_score('Rojo')}",
                font=("Arial", 20)).pack()

    def show_winner(self):
        green = self.board.get_score("Verde")
        red = self.board.get_score("Rojo")
        if green > red:
            messagebox.showinfo("Ganador", "¡Yoshi Verde (Máquina) ganó!")
        elif red > green:
            messagebox.showinfo("Ganador", "¡Yoshi Rojo (Jugador) ganó!")
        else:
            messagebox.showinfo("Empate", "¡El juego terminó en empate!")
        
        self.root.after(2000, self.restart_game)
        
    def restart_game(self):
        """Reinicia el juego con la misma dificultad"""
        if hasattr(self, 'minimax'):
          
            depth = self.minimax.depth
            self.clear_window()
            self.board = Board() 
            self.yoshi_green = Yoshi("Verde", self.board.random_start_position())
            self.yoshi_red = Yoshi("Rojo", self.board.random_start_position(exclude=self.yoshi_green.position))
            self.minimax = Minimax(depth)
            self.create_board()
            self.machine_turn()
        else:
        
            self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = YoshisZonesApp(root)
    root.mainloop()