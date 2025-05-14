import copy

class Minimax:
    def __init__(self, depth):
        self.depth = depth

    def minimax(self, board, green, red, depth, is_max, alpha, beta):
        if depth == 0 or board.all_zones_painted():
            return self.evaluate(board, green, red), None

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
        return board.get_score("Verde") - board.get_score("Rojo")