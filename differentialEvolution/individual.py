import pygame
from typing import List, Optional

from chessset.utils import load_image

class Individual:
    def __init__(self, vector, position: List[int] = [0, 0], board_width: int = 8, board_height: int = 8) -> None:
        '''Initialize the knight with a position on the board'''
        self.vector = vector
        self.fitness = None
        self.position: List[int] = position
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.image: Optional[pygame.Surface] = self._get_image()

    def evaluate(self, problem):
        self.fitness = problem.evaluate(self.vector)

    def move(self, steps_x: int, steps_y: int, board) -> None:
        '''Move the knight by the specified steps in x and y direction'''
        board.visited_positions.add(tuple(self.position))
        if self._move_is_valid(steps_x, steps_y, board):
            self.position[0] += steps_x
            self.position[1] += steps_y

    def _move_is_valid(self, steps_x: int, steps_y: int, board) -> bool:
        '''Check if the move is valid for a knight'''
        if (abs(steps_x) == 2 and abs(steps_y) == 1) or (abs(steps_x) == 1 and abs(steps_y) == 2):
            new_x = self.position[0] + steps_x
            new_y = self.position[1] + steps_y
            if 0 <= new_x < self.board_width and 0 <= new_y < self.board_height:
                return True
        return False

    def _get_image(self) -> Optional[pygame.Surface]:
        '''Load the knight image'''
        knight_image: Optional[pygame.Surface] = load_image("knight_image.png", (50, 50))
        if not knight_image:
            print("Failed to load knight image. Please ensure 'knight_image.png' exists.")
            return None
        return pygame.transform.scale(knight_image, (50, 50))