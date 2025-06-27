from typing import List, Tuple
from chessset.board import Board
import copy

from differentialEvolution.individual import Individual


class KnightTourProblem:
    def __init__(self, board: Board, knight: Individual, max_steps: int = 100):
        self.board = board
        self.knight = knight
        self.vector_length = max_steps
        self.bounds = [(0.0, 1.0)] * max_steps 

        # possible knight moves
        self.knight_moves: List[Tuple[int, int]] = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]

    def evaluate(self, vector: List[float]) -> float:
        # Clone only the knight's position
        position = self.knight.position.copy()
        visited = {tuple(position)}

        print(f"Start position: {position}")

        ## TODO: This should relate to the knight's move logic
        for gene in vector:
            move_idx = int(gene * len(self.knight_moves)) % 8
            dx, dy = self.knight_moves[move_idx]

            new_x = position[0] + dx
            new_y = position[1] + dy

            # Bounds and obstacle check
            if (
                0 <= new_x < self.board.width and
                0 <= new_y < self.board.height and
                not self.board.matrix[new_y][new_x].is_obstacle and
                (new_x, new_y) not in visited
            ):
                position = [new_x, new_y]
                visited.add(tuple(position))
                #print(f"Moved to: {position}, visited count: {len(visited)}")
            else:
                pass
                #print(f"Move blocked or revisited at: {(new_x, new_y)}")

        print(f"Final visited count: {len(visited)}")
        return -len(visited)  # more visited cells = better fitness
    
    def decode_vector_to_moves(self, vector: List[float]) -> List[Tuple[int, int]]:
        """Convert a DE vector into a sequence of knight move steps."""
        moves = []
        for gene in vector:
            move_idx = int(gene * len(self.knight_moves)) % 8
            moves.append(self.knight_moves[move_idx])
        return moves
