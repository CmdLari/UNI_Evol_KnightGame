import os
import json
import re
import pandas as pd

# Folder containing JSON files
folder_path = "results/avgs"

# Regex pattern updated to ignore date
filename_pattern = re.compile(
    r"BOARD_(?P<BOARD>\d+)-OBSTACLES_(?P<OBSTACLES>\w+)-POP_(?P<POP>\d+)"
    r"-GEN_(?P<GEN>\d+)-STEPSIZE_(?P<STEPSIZE>[\d.]+)-CR_(?P<CR>[\d.]+)"
    r"-STEPS_(?P<STEPS>\d+)-ELITISM_(?P<ELITISM>\w+)-ELITISM_RATE_(?P<ELITISM_RATE>[\d.]+)"
)

records = []

for filename in os.listdir(folder_path):
    if not filename.endswith(".json"):
        continue

    match = filename_pattern.search(filename)
    if not match:
        print(f"Skipped (no match): {filename}")
        continue

    params = match.groupdict()
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'r') as f:
        metrics = json.load(f)

    # Combine parameters and metrics into one record
    record = {
        "BOARD SIZE": f"{params['BOARD']} x {params['BOARD']}",
        "POP SIZE": params["POP"],
        "GENERATIONS": params["GEN"],
        "CR": float(params["CR"]),
        "STEPSIZE": float(params["STEPSIZE"]),
        "STEPS": params["STEPS"],
        "OBSTACLES": params["OBSTACLES"],
        "ELITISM": params["ELITISM"],
        "ELITISM RATE": params["ELITISM_RATE"],
        "BEST FITNESS": metrics.get("best_fitness"),
        "WORST FITNESS": metrics.get("worst_fitness"),
        "AVG FITNESS": metrics.get("average_fitness"),
        "BF / STEP": metrics.get("best_fitness_per_step"),
        "WF / STEP": metrics.get("worst_fitness_per_step"),
        "AF / STEP": metrics.get("average_fitness_per_step"),
    }

    records.append(record)

# Convert to DataFrame and save
df = pd.DataFrame(records)
df.to_csv("compiled_results.csv", index=False)
print("Results saved to compiled_results.csv")
