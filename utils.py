import pygame
import json
import os
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

def save_results_to_json(filename: str, new_result: Dict[str, float]) -> None:
    """Append a result dict to a JSON file using the next available integer key."""
    results_path = "results"
    os.makedirs(results_path, exist_ok=True)
    full_path = os.path.join(results_path, filename)

    data = {}

    # Load existing data if file exists
    if os.path.exists(full_path):
        try:
            with open(full_path, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Couldn't read existing file, starting fresh: {e}")

    # Find next available integer key as a string
    next_key = str(max(map(int, data.keys()), default=0) + 1)
    data[next_key] = new_result

    # Save updated data
    try:
        with open(full_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Result saved under key '{next_key}' in {full_path}")
    except IOError as e:
        print(f"Error saving results to {full_path}: {e}")
