import pygame
import random
from typing import List
from typing import Optional, Tuple

from utils import load_image
from chessset.field import Field

class Board:
    def __init__(self, width: int, height: int, starting_position: List[int], with_obstacles: bool = False) -> None:
        '''Initialize the board with given width and height'''
        self.width: int = width
        self.height: int = height
        self.matrix: List[List[Field]] = [[None for _ in range(width)] for _ in range(height)]
        self._create_fields(starting_position, with_obstacles)
        self.visited_image: Optional[pygame.Surface] = load_image("visited.png", (50, 50))
        self.obstacle_image: Optional[pygame.Surface] = load_image("obstacle_image.png", (50, 50))

        self.visited_tiles = []

    def _create_fields(self, knight_start: Tuple[int, int], with_obstacles: bool = False) -> None:
        '''Create fields for the board with randomized but usable obstacle layout'''
        for row in range(self.height):
            for col in range(self.width):
                is_light = (col + row) % 2 == 0
                field = Field(col, row, is_light)
                
                if with_obstacles:
                    if (col, row) != knight_start:
                        if random.random() < 0.07:  # ~7% chance
                            field.is_obstacle = True

                self.matrix[row][col] = field