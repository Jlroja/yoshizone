class Yoshi:
    def __init__(self, color, start_pos):
        self.color = color
        self.position = start_pos
        self.opponent = None  # Se asignará después

    def move(self, new_pos, board):
        """Mueve al Yoshi y pinta la celda si es zona especial"""
        self.position = new_pos
        if board.is_zone_cell(new_pos):
            board.paint_cell(new_pos, self.color)
        return True

    def valid_knight_moves(self, board_size, board):
        """Calcula movimientos válidos de caballo"""
        r, c = self.position
        moves = []
        for dr, dc in [(2,1),(1,2),(-2,1),(-1,2),(2,-1),(1,-2),(-2,-1),(-1,-2)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < board_size and 0 <= nc < board_size:
                pos = (nr, nc)
                if (pos not in board.painted_cells and 
                    pos != self.opponent.position):  # Evitar posición del oponente
                    moves.append(pos)
        return moves

    def __repr__(self):
        return f"Yoshi({self.color}, {self.position})"