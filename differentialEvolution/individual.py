import random

import pygame
from typing import List, Optional, Set, Tuple

from chessset.field import Field
from chessset.utils import load_image

class Individual:
    def __init__(self, position, board_width, board_height) -> None:
        '''Initialize the knight with a position on the board'''
        self.image: Optional[pygame.Surface] = self._get_image()
        self.fitness = 0
        self.position: List[int] = position
        self.board_width: int = board_width
        self.board_height: int = board_height
        self.image: Optional[pygame.Surface] = self._get_image()
        self.visited_tiles = []
        self.visited_tiles.append(self.position)
        # List of movements
        self.knight_moves: List[Tuple[int, int]] = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        self.vector = []

    def move_for_show(self, dx, dy):
        '''Move the knight's move for show'''
        self.position[0] += dx
        self.position[1] += dy

    def draw_knight(self, screen: pygame.Surface) -> None:
        knight_x, knight_y = self.position
        screen.blit(self.image, (knight_x * 50, knight_y * 50))

    def move(self, board, steps) -> None:
        '''Move the knight by the specified steps in x and y direction'''

        for i in range(steps):
            rnd: int = random.randint(0, len(self.knight_moves) - 1)
            move_x = self.knight_moves[rnd][0]
            move_y = self.knight_moves[rnd][1]

            self.evaluate(board, move_x, move_y, rnd)

    def evaluate(self, board, move_x, move_y, rnd):
        new_position = self.position[0] + move_x, self.position[1] + move_y

        if 0 <= new_position[0] < self.board_width and 0 <= new_position[1] < self.board_height:
            is_valid_move = True
            self.position = new_position
        else:
            is_valid_move = False

        if is_valid_move:
            self.vector.append(rnd)
            board.matrix[self.position[1]][self.position[0]].has_knight = True

        # REWARDS
            self.fitness += 10
            # new tile visited
            if not new_position in self.visited_tiles:
                self.visited_tiles.append(new_position)
                self.fitness += 2

        # PUNISHMENTS
        # revisiting
            else:
                self.fitness -= 2
        # out of bounds
        if not is_valid_move:
            self.fitness -= 2
        # obstacle
        if is_valid_move:
            if board.matrix[self.position[1]][self.position[0]].is_obstacle:
                self.fitness -= 2



    def _get_image(self) -> Optional[pygame.Surface]:
        '''Load the knight image'''
        knight_image: Optional[pygame.Surface] = load_image("knight_image.png", (50, 50))
        if not knight_image:
            print("Failed to load knight image. Please ensure 'knight_image.png' exists.")
            return None
        return pygame.transform.scale(knight_image, (50, 50))