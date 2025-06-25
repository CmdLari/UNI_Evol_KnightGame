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
