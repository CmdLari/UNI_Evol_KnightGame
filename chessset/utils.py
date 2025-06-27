import pygame
from typing import Optional, Tuple, Dict

image_cache: Dict[str, pygame.Surface] = {}

def load_image(image_path: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
    """Load an image from the given path and optionally resize it."""
    image_path = f"assets/{image_path}"
    if image_path in image_cache:
        return image_cache[image_path]

    try:
        image = pygame.image.load(image_path)
        if size:
            image = pygame.transform.scale(image, size)
        image_cache[image_path] = image
        return image
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def draw_board(screen, board, knight, ctr) -> None:
    '''Draw the board on the screen'''
    
    for row in range(board.height):
        for col in range(board.width):
            field_image = board.matrix[row][col].image
            if field_image:
                screen.blit(field_image, (col * 50, row * 50))
            if board.matrix[row][col].is_obstacle:
                obstacle_x, obstacle_y = col * 50, row * 50
                if board.obstacle_image:
                    screen.blit(board.obstacle_image, (obstacle_x, obstacle_y))
            if [board.matrix[row][col].position_x, board.matrix[row][col].position_y] in board.visited_tiles:
                visited_x, visited_y = col * 50, row * 50
                if board.visited_image:
                    screen.blit(board.visited_image, (visited_x, visited_y))
    board.visited_tiles.append(knight.visited_tiles[ctr])
    knight.draw_knight(screen)