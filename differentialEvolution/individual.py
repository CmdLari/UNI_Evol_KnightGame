import pygame
from typing import List, Optional, Tuple
from chessset.utils import load_image

class Individual:
    def __init__(self, vector: List[float], starting_position: List[int], board_width: int, board_height: int) -> None:
        self.vector: List[float] = vector  # Float vector [0.0, 1.0]
        self.starting_position: List[int] = starting_position.copy()
        self.position: List[int] = starting_position.copy()
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.fitness: float = 0.0
        self.visited_tiles: List[List[int]] = [self.position.copy()]
        self.knight_moves: List[Tuple[int, int]] = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        self.image: Optional[pygame.Surface] = self._get_image()

    def evaluate(self, board) -> float:
        """Evaluate fitness by simulating knight moves from the vector."""
        self.fitness = 0
        self.position = self.starting_position.copy()
        self.visited_tiles = [self.position.copy()]

        for gene in self.vector:
            move_idx = int(gene * 8) % 8
            dx, dy = self.knight_moves[move_idx]
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy

            if 0 <= new_x < self.board_width and 0 <= new_y < self.board_height:
                self.position = [new_x, new_y]
                tile = board.matrix[new_y][new_x]

                if tile.is_obstacle:
                    self.fitness -= 2
                if self.position not in self.visited_tiles:
                    self.visited_tiles.append(self.position.copy())
                    self.fitness += 4
                else:
                    self.fitness -= 2
            else:
                self.fitness -= 4  # Strong penalty for going off board

        return self.fitness

    def move_for_show(self, dx, dy):
        '''Move the knight's move for show'''
        self.position[0] = dx
        self.position[1] = dy

    def _get_image(self) -> Optional[pygame.Surface]:
        knight_image: Optional[pygame.Surface] = load_image("knight_image.png", (50, 50))
        if not knight_image:
            print("Failed to load knight image.")
            return None
        return pygame.transform.scale(knight_image, (50, 50))

    def draw_knight(self, screen: pygame.Surface) -> None:
        x, y = self.position
        if self.image:
            screen.blit(self.image, (x * 50, y * 50))
