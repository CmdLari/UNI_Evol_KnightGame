import pygame

image_cache = {}

def load_image(image_path, size=None):
    """Load an image from the given path and optionally resize it."""
    image_path = f"assets/{image_path}"  # Normalize the path to lower case
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