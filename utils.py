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

    return full_path

def document_generation_in_json(filename:str, best_fitness:int, worst_fitness:int, average_fitness:float, best_attempted_moves:int, steps:int) -> None:
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
        "best_fitness_per_step": best_fitness / steps,
        "worst_fitness": worst_fitness,
        "worst_fitness_per_step": worst_fitness / steps,
        "average_fitness": average_fitness,
        "average_fitness_per_step": average_fitness / steps,
        "best_attempted_moves_nr": best_attempted_moves
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
    best_fitness_per_step = [entry["best_fitness_per_step"] for entry in data.values()]
    worst_fitness = [entry["worst_fitness"] for entry in data.values()]
    worst_fitness_per_step = [entry["worst_fitness_per_step"] for entry in data.values()]
    average_fitness = [entry["average_fitness"] for entry in data.values()]
    average_fitness_per_step = [entry["average_fitness_per_step"] for entry in data.values()]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, label='Best Fitness', marker='o', color='gold')
    plt.plot(generations, average_fitness, label='Average Fitness', linestyle='--', color='teal')
    plt.plot(generations, worst_fitness, label='Worst Fitness', marker='x', color='salmon')


    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title(f'FITNESS OVER GENERATIONS \n({diff_evolution.board.width}x{diff_evolution.board.height} Board, Obstacles: {diff_evolution.board.obstacles}, Population: {diff_evolution.pop_size}, Generations: {diff_evolution.generations}, Stepsize: {diff_evolution.stepsize_param}, Crossover Rate: {diff_evolution.crossover_rate}, Steps: {diff_evolution.steps})')
    plt.legend()
    plt.grid()
    plt.ylim(min(worst_fitness) - 1000, max(best_fitness) + 1000)
    plt.savefig(os.path.join(results_path, f"{filename}.png"))
    # plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness_per_step, label='Best Fitness per Step', marker='o', color='gold')
    plt.plot(generations, average_fitness_per_step, label='Average Fitness per Step', linestyle='--', color='teal')
    plt.plot(generations, worst_fitness_per_step, label='Worst Fitness per Step', marker='x', color='salmon')

    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title(f'AVG FITNESS / STEP OVER GENERATIONS \n({diff_evolution.board.width}x{diff_evolution.board.height} Board, Obstacles: {diff_evolution.board.obstacles}, Population: {diff_evolution.pop_size}, Generations: {diff_evolution.generations}, Stepsize: {diff_evolution.stepsize_param}, Crossover Rate: {diff_evolution.crossover_rate}, Steps: {diff_evolution.steps})')
    plt.legend()
    plt.grid()
    plt.ylim(min(worst_fitness_per_step) - 50, max(best_fitness_per_step) + 50)
    plt.savefig(os.path.join(results_path, f"{filename}_avgs.png"))
    # plt.show()


def process_accumulated_runs(full_path: str = "results/gen_doc/2025-06-28/2025-06-28_BOARD_64-OBSTACLES_True-POP_64-GEN_640-STEPSIZE_0.5-CR_0.9-STEPS_320.json"):
    """Process all runs in a result.json and save aggregate statistics."""
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return {}

    with open(full_path, "r") as file:
        data = json.load(file)

    keys_to_average = [
        "best_fitness", "worst_fitness", "average_fitness",
        "best_fitness_per_step", "worst_fitness_per_step",
        "average_fitness_per_step", "best_attempted_moves"
    ]

    accumulator = {key: 0.0 for key in keys_to_average}
    count = len(data)

    for run in data.values():
        for key in keys_to_average:
            accumulator[key] += run.get(key, 0.0)

    averaged_results = {key: value / count for key, value in accumulator.items()}

    # Save .avg file
    avg_dir = "results/avg"
    os.makedirs(avg_dir, exist_ok=True)

    base_filename = os.path.basename(full_path).replace(".json", ".avg.json")
    avg_file = os.path.join(avg_dir, base_filename)
    with open(avg_file, "w") as outfile:
        json.dump(averaged_results, outfile, indent=4)
    print(f"Averages saved to {avg_file}")

    # Visualization
    plt.figure(figsize=(10, 6))
    keys_to_plot = ["best_fitness_per_step", "average_fitness_per_step", "worst_fitness_per_step"]
    values = [averaged_results[k] for k in keys_to_plot]
    plt.bar(keys_to_plot, values, color=['gold', 'teal', 'salmon'])
    plt.title("Average Fitness per Step Across Runs")
    plt.ylabel("Fitness per Step")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(avg_file.replace('.json', '_fitness_per_step_plot.png'))
    print(f"Plot saved to {full_path.replace('.json', '_fitness_per_step_plot.png')}")

    return averaged_results
