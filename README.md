# Yoshi's Zones - Inteligencia Artificial con Minimax

## 🎮 Descripción del Juego
**Yoshi's Zones** es un juego estratégico para dos jugadores donde cada uno controla un Yoshi (verde/rojo) en un tablero de ajedrez. El objetivo es controlar la mayoría de las casillas en las **4 zonas especiales** del tablero.

## 🤖 Algoritmo Minimax Implementado
El sistema IA utiliza **Minimax con poda alfa-beta** para tomar decisiones óptimas.

### Función de Evaluación Heurística (`evaluate()`)
```python
def evaluate(self, board, green, red):
    # 1. Puntuación base por zonas ganadas
    score = 15 * (board.get_score("Verde") - board.get_score("Rojo"))
    
    # 2. Control de zonas no decididas
    for zone, cells in board.original_zones.items():
        green_cells = sum(1 for c in cells if board.painted_colors.get(c) == "Verde")
        red_cells = sum(1 for c in cells if board.painted_colors.get(c) == "Rojo")
        
        if green_cells + red_cells < 5:  # Zona no completada
            if green_cells >= 3: score += 5
            if red_cells >= 3: score -= 10
    
    # 3. Movilidad (diferencial de movimientos posibles)
    score += 0.7 * (len(green.valid_knight_moves()) - len(red.valid_knight_moves()))
    
    # 4. Proximidad a zonas no completadas
    score += 0.5 * (self.zone_proximity(red) - self.zone_proximity(green))
    
    return score
```
# Explicación de la Función Heurística

## 📊 Objetivo Principal
La función heurística `evaluate()` en `minimax.py` **cuantifica qué tan favorable es un estado del juego** para la IA (Yoshi verde), considerando:

```python
def evaluate(self, board, green, red):
    [implementación]
    return score  # Valor numérico (+ = favorable a la IA, - = favorable al jugador)
