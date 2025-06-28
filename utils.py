import pygame
import json
import os
from typing import Optional, Tuple, Dict
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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
    results_path = f"results/gen_doc/{datetime.now().date()}"
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

def document_generation_in_json(filename:str, best_fitness:int, worst_fitness:int, average_fitness:float, best_attempted_moves:int) -> None:
    """Document the parameters of the generation in a JSON file."""
    results_path = f"results/gen_doc/{datetime.now().date()}"
    os.makedirs(results_path, exist_ok=True)
    full_path = os.path.join(results_path, filename)

    data = {}

    if os.path.exists(full_path):
        try:
            with open(full_path, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Couldn't read existing file, starting fresh: {e}")

    next_key = str(max(map(int, data.keys()), default=0) + 1)
    new_entry = {
        "best_fitness": best_fitness,
        "worst_fitness": worst_fitness,
        "average_fitness": average_fitness,
        "best_attempted_moves": best_attempted_moves
    }

    data[next_key] = new_entry
    
    try:
        with open(full_path, "w") as file:
            json.dump(data, file, indent=4)
        # print(f"Generation documented in {full_path}")
    except IOError as e:
        print(f"Error saving generation documentation to {full_path}: {e}")

def plot_fitness_over_generations(filename: str, diff_evolution) -> None:
    """Plot fitness over generations from a JSON file."""
    results_path = f"results/gen_doc/{datetime.now().date()}"
    full_path = os.path.join(results_path, filename)

    if not os.path.exists(full_path):
        print(f"File {full_path} does not exist.")
        return

    with open(full_path, "r") as file:
        data = json.load(file)

    generations = list(map(int, data.keys()))
    best_fitness = [entry["best_fitness"] for entry in data.values()]
    worst_fitness = [entry["worst_fitness"] for entry in data.values()]
    average_fitness = [entry["average_fitness"] for entry in data.values()]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, label='Best Fitness', marker='o')
    plt.plot(generations, worst_fitness, label='Worst Fitness', marker='x')
    plt.plot(generations, average_fitness, label='Average Fitness', marker='s')

    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title(f'FITNESS OVER GENERATIONS \n({diff_evolution.board.width}x{diff_evolution.board.height} Board, Obstacles: {diff_evolution.board.obstacles}, Population: {diff_evolution.pop_size}, Generations: {diff_evolution.generations}, Stepsize: {diff_evolution.stepsize_param}, Crossover Rate: {diff_evolution.crossover_rate}, Steps: {diff_evolution.steps})')
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(results_path, f"{filename}.png"))
    # plt.show()