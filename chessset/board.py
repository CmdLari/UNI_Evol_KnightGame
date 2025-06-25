import pygame
import random
from typing import List
from typing import Optional, Tuple, Set

from chessset.utils import load_image
from chessset.knight import Knight
from chessset.field import Field

class Board:
    def __init__(self, screen: pygame.Surface, width: int, height: int, starting_position: List[int], with_obstacles: bool = False) -> None:
        '''Initialize the board with given width and height'''
        self.width: int = width
        self.height: int = height
        self.screen: pygame.Surface = screen
        self.matrix: List[List[Field]] = [[0 for _ in range(width)] for _ in range(height)]
        self._create_fields(starting_position, with_obstacles)
        self.visited_positions: Set[Tuple[int, int]] = set()

        self.visited_image: Optional[pygame.Surface] = load_image("visited.png", (50, 50))
        self.obstacle_image: Optional[pygame.Surface] = load_image("obstacle_image.png", (50, 50))

    def draw_board(self, knight: Knight) -> None:
        '''Draw the board on the screen'''
        self.matrix[knight.position[1]][knight.position[0]].has_knight = True
        self.matrix[knight.position[1]][knight.position[0]].is_visited = True
        for row in range(self.height):
            for col in range(self.width):
                field_image = self.matrix[row][col].image
                if field_image:
                    self.screen.blit(field_image, (col * 50, row * 50))
                if self.matrix[row][col].is_obstacle:
                    obstacle_x, obstacle_y = col * 50, row * 50
                    if self.obstacle_image:
                        self.screen.blit(self.obstacle_image, (obstacle_x, obstacle_y))
                if self.matrix[row][col].is_visited:
                    visited_x, visited_y = col * 50, row * 50
                    if self.visited_image:
                        self.screen.blit(self.visited_image, (visited_x, visited_y))
                if self.matrix[row][col].has_knight:
                    knight_x, knight_y = knight.position
                    self.screen.blit(knight.image, (knight_x * 50, knight_y * 50))


    def _create_fields(self, knight_start: Tuple[int, int], with_obstacles: bool = False) -> None:
        '''Create fields for the board with randomized but usable obstacle layout'''
        for row in range(self.height):
            for col in range(self.width):
                is_light = (row + col) % 2 == 0
                field = Field(col, row, is_light)
                
                if with_obstacles:
                    if (col, row) != knight_start:
                        if random.random() < 0.07:  # ~7% chance
                            field.is_obstacle = True

                self.matrix[row][col] = field

