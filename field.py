import pygame
from typing import Optional, Tuple
from utils import load_image

class Field:
    '''Field represents each square on the board'''

    def __init__(self, position_x: int, position_y: int, is_light: bool) -> None:
        self.position_x = position_x
        self.y = position_y
        self.is_light = is_light  # Move this line up
        self.name = self._get_name()
        self.image = self._get_image()
        self.is_obstacle = False
        self.is_visited = False
        self.has_knight = False

    def _get_name(self) -> str:
        '''Generate a name for the field based on its position'''
        return f"[{self.position_x}, {self.y}]"
    
    def _get_image(self) -> Tuple[Optional[pygame.Surface], Optional[pygame.Surface], Optional[pygame.Surface]]:
        '''Load the board images'''
        if self.is_light:
            image = "field_light.png"
        else:
            image = "field_dark.png"
        field_image = load_image(image, (50, 50))
        if not field_image:
            print(f"Failed to load field image '{image}'. Please ensure it exists.")
            return None, None, None 
        return pygame.transform.scale(field_image, (50, 50)) if field_image else None