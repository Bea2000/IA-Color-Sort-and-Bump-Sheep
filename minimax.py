import copy
import math
import utils
import random

"""En este archivo se desarrolla el algoritmo minimax."""

def minimax(game, depth, alpha=(-math.inf), beta=(math.inf)):

    if depth == 0 or game.blanco.puntaje >= game.objetivo or game.negro.puntaje >= game.objetivo:
        
        # Función de score
        score = game.blanco.puntaje - game.negro.puntaje

        # Caso fin de recursión
        if depth == 0:
            return ((None, None), score)

        # Casos de término
        if game.blanco.puntaje >= game.objetivo and score > 0:
            return ((None, None), math.inf) # Gana blanco
        
        elif game.negro.puntaje >= game.objetivo and score < 0:
            return ((None, None), -math.inf) # Gana negro
        
        elif game.negro.puntaje >= game.objetivo and score == 0:
            return ((None, None), 0) # Empate


    # Se define si se maximiza o minimiza
    maximize = True if game.turno.color == "blanco" else False

    """
    Se deben obtener los posibles movimientos correspondientes a la jugada.
    Los posibles movimientos hay que dejarlos en una lista de tuplas llamada valid_moves.
    valid_moves tendrá elementos del tipo (oveja, fila)
    """
    valid_sheeps, valid_rows = utils.disponibilidades(game)
    valid_moves = [(sheep, row) for sheep in valid_sheeps for row in valid_rows]

    if maximize:
        # Maximizing player
        score = -math.inf
        best_move = ("0", "0")
        for move in valid_moves:
            # Se hace una copia del juego para simular jugadas sin afectar el juego actual
            game_copy = copy.deepcopy(game)

            """ 
            Aplicar el algoritmo en el caso de que se minimice.
            Se tiene que simular la jugada y llamar recursivamente a minimax, y comprobar si el 
            score mejora para encontrar el movimiento óptimo.
            Aquí también se debe implementar la poda alpha-beta.
            """
            # We simulate the next move
            utils.ejecutar_jugada(game_copy, move[0], move[1])
            # We evaluate that move recursively
            eval = minimax(game_copy, depth-1, alpha, beta)[1]
            # We check if the score of picking that move is better than the previous one
            if eval > score:
                # We update the best move and the score
                best_move = (move[0], move[1])
                score = eval
            # We check if the move gives us a bigger alpha
            alpha = max(alpha, eval)
            # We check if we can prune
            if beta <= alpha:
                break

    else:
        # Minimizing player
        score = math.inf
        best_move = ("0", "0")
        for move in valid_moves:
            # Se hace una copia del juego para simular jugadas sin afectar el juego actual
            game_copy = copy.deepcopy(game)

            """ 
            Aplicar el algoritmo en el caso de que se minimice.
            Se tiene que simular la jugada y llamar recursivamente a minimax, y comprobar si el 
            score mejora para encontrar el movimiento óptimo.
            Aquí también se debe implementar la poda alpha-beta.
            """
            # We simulate the next move
            utils.ejecutar_jugada(game_copy, move[0], move[1])
            # We evaluate that move recursively
            eval = minimax(game_copy, depth-1, alpha, beta)[1]
            # We check if the score of picking that move is better than the previous one
            if eval < score:
                # We update the best move and the score
                best_move = (move[0], move[1])
                score = eval
            # We check if the move gives us a smaller beta
            beta = min(beta, eval)
            # We check if we can prune
            if beta <= alpha:
                break
    
    return (best_move, score)