import random

class Board:
    def __init__(self, size=8):
        self.size = size
        self.original_zones = self.create_zones()
        self.zones = self.create_zones()
        self.painted_cells = set()
        self.painted_colors = {}

    def create_zones(self):
        return {
            "top_left": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
            "top_right": [(0, 7), (0, 6), (1, 7), (1, 6), (2, 7)],
            "bottom_left": [(7, 0), (7, 1), (6, 0), (6, 1), (5, 0)],
            "bottom_right": [(7, 7), (7, 6), (6, 7), (6, 6), (5, 7)]
        }

    def is_zone_cell(self, position):
        for zone, cells in self.original_zones.items():
            if position in cells:
                return True
        return False

    def paint_cell(self, position, color):
        if self.is_zone_cell(position) and position not in self.painted_cells:
            self.painted_cells.add(position)
            self.painted_colors[position] = color
            for zone, cells in self.zones.items():
                if position in cells:
                    cells.remove(position)
            return True
        return False

    def random_start_position(self, exclude=None):
        while True:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if (pos not in self.painted_cells and 
                not self.is_zone_cell(pos) and 
                pos != exclude):
                return pos

    def all_zones_painted(self):
        return all(len(cells) == 0 for cells in self.zones.values())

    def get_score(self, color):
        score = 0
        for zone, cells in self.original_zones.items():
            green = sum(1 for cell in cells if cell in self.painted_colors and self.painted_colors[cell] == "Verde")
            red = sum(1 for cell in cells if cell in self.painted_colors and self.painted_colors[cell] == "Rojo")
            total_painted = green + red
            if total_painted >= 3:  # Solo considerar zonas con al menos 3 celdas pintadas
                if color == "Verde" and green > red:
                    score += 1
                elif color == "Rojo" and red > green:
                    score += 1
        return score