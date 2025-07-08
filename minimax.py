import copy
import hashlib

class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.visited_states = set()

    def minimax(self, board, green, red, depth, is_max, alpha, beta):
        state_hash = self.hash_board_state(board, green, red)
        if depth == 0 or board.all_zones_painted() or state_hash in self.visited_states:
            return self.evaluate(board, green, red), None

        self.visited_states.add(state_hash)

        current_yoshi = green if is_max else red
        best_move = None
        best_val = float('-inf') if is_max else float('inf')

        for move in current_yoshi.valid_knight_moves(board.size, board):
            new_board = copy.deepcopy(board)
            new_green = copy.deepcopy(green)
            new_red = copy.deepcopy(red)

            if is_max:
                new_green.move(move, new_board)
            else:
                new_red.move(move, new_board)

            val, _ = self.minimax(new_board, new_green, new_red, depth-1, not is_max, alpha, beta)

            if is_max:
                if val > best_val:
                    best_val = val
                    best_move = move
                alpha = max(alpha, best_val)
            else:
                if val < best_val:
                    best_val = val
                    best_move = move
                beta = min(beta, best_val)

            if beta <= alpha:
                break

        return best_val, best_move

    def evaluate(self, board, green, red):
        # Puntuación base por zonas ganadas
        green_score = board.get_score("Verde")
        red_score = board.get_score("Rojo")
        score = 15 * (green_score - red_score)  # Peso alto para zonas ganadas

        # Celdas pintadas en zonas no decididas
        for zone, cells in board.original_zones.items():
            green_cells = sum(1 for cell in cells if board.painted_colors.get(cell) == "Verde")
            red_cells = sum(1 for cell in cells if board.painted_colors.get(cell) == "Rojo")
            total_painted = green_cells + red_cells
            
            if total_painted < 5:  # Zona no completada
                # Bonus por progreso en zona
                score += 2 * (green_cells - red_cells)
                
                # Urgencia: si el oponente está cerca de ganar
                if red_cells >= 3:
                    score -= 10
                elif green_cells >= 3:
                    score += 5

        # Movilidad
        green_moves = len(green.valid_knight_moves(board.size, board))
        red_moves = len(red.valid_knight_moves(board.size, board))
        score += 0.7 * (green_moves - red_moves)

        # Proximidad a zonas no completadas
        def zone_proximity(yoshi):
            zones = [cell for zone in board.zones.values() for cell in zone]
            if not zones:
                return 0
            return min(abs(cell[0]-yoshi.position[0]) + abs(cell[1]-yoshi.position[1]) for cell in zones)

        score += 0.5 * (zone_proximity(red) - zone_proximity(green))

        return score

    def hash_board_state(self, board, green, red):
        painted = tuple(sorted((pos, board.painted_colors[pos]) for pos in board.painted_cells))
        return hashlib.md5(str((painted, green.position, red.position)).encode()).hexdigest()