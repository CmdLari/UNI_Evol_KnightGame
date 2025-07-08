import csv
import subprocess

CSV_PATH = 'BatchConditions.csv'
RUN_ONLY_NON_OBSTACLE_CASES = True  # Set to False to only run entries where obstacles is True

def parse_value(val: str, board_size: int) -> int | float | bool:
    val = val.strip().upper()
    if "BS" in val:
        val = val.replace("BS", str(board_size))
    if "*" in val:
        return eval(val)
    if val in {"TRUE", "FALSE"}:
        return val == "TRUE"
    try:
        return int(val)
    except ValueError:
        return float(val)

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Extract headers and data rows
headers = rows[2]
data_rows = [row for row in rows[3:] if any(cell.strip() for cell in row)]

for row in data_rows:
    board_size = parse_value(row[0], 0)
    pop_size = parse_value(row[1], board_size)
    generations = parse_value(row[2], board_size)
    crossover = parse_value(row[3], board_size)
    stepsize = parse_value(row[4], board_size)
    steps = parse_value(row[5], board_size)
    obstacles = parse_value(row[6], board_size)
    elitism = parse_value(row[7], board_size)
    elitism_rate = parse_value(row[8], board_size)

    # Conditional skip based on obstacle switch
    if RUN_ONLY_NON_OBSTACLE_CASES and obstacles:
        continue
    if not RUN_ONLY_NON_OBSTACLE_CASES and not obstacles:
        continue

    cmd = [
        'python', 'main.py',
        '--BOARD_SIZE', str(board_size),
        '--POPULATION_SIZE', str(pop_size),
        '--GENERATIONS', str(generations),
        '--CROSSOVER_RATE', str(crossover),
        '--STEPSIZE_PARAM', str(stepsize),
        '--STEPS', str(steps),
        '--OBSTACLES', str(obstacles),
        '--ELITISM', str(elitism),
        '--ELITISM_RATE', str(elitism_rate),
        '--NUMBER_OF_RUNS', '20',
        '--DOCUMENT_GENERATIONS', 'False',
        '--SHOW_PONY', 'False'
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)
