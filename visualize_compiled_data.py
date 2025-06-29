import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your data
df = pd.read_csv("results/compiled/compiled_results.csv")

# Create a label including all key parameters
df["label"] = (
    "BS=" + df["BOARD SIZE"].astype(str)
    + " | POP=" + df["POP SIZE"].astype(str)
    + " | GEN=" + df["GENERATIONS"].astype(str)
    + " | CR=" + df["CR"].astype(str)
    + " | STPSIZE=" + df["STEPSIZE"].astype(str)
    + " | STPS=" + df["STEPS"].astype(str)
    + " | OBS=" + df["OBSTACLES"].astype(str)
    + " | ELIT=" + df["ELITISM"].astype(str)
    + " | ELR=" + df["ELITISM RATE"].astype(str)
)

# Sort and select top 10 by best fitness per step
df_sorted = df.sort_values(by="BF / STEP", ascending=False).head(10)

# Define bar colors
bar_colors = df_sorted["SOLVED"].map({True: "teal", False: "salmon"})

# Plotting
plt.figure(figsize=(14, 6))
bars = plt.bar(df_sorted["label"], df_sorted["BF / STEP"], color=bar_colors)

plt.xticks(rotation=45, ha="right", fontsize=8)
plt.ylabel("Best Fitness per Step")
plt.title("Top 10 Parameter Combinations by Best Fitness per Step")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='teal', label='Solved'),
    mpatches.Patch(facecolor='salmon', label='Not Solved')
]
plt.legend(handles=legend_elements, title="Outcome")

plt.tight_layout()
plt.savefig("results/compiled/top10_results_barplot.png")
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your data
df = pd.read_csv("results/compiled/compiled_results.csv")

# Create a label including all key parameters
df["label"] = (
    "BS=" + df["BOARD SIZE"].astype(str)
    + " | POP=" + df["POP SIZE"].astype(str)
    + " | GEN=" + df["GENERATIONS"].astype(str)
    + " | CR=" + df["CR"].astype(str)
    + " | STPSIZE=" + df["STEPSIZE"].astype(str)
    + " | STPS=" + df["STEPS"].astype(str)
    + " | ELIT=" + df["ELITISM"].astype(str)
    + " | ELR=" + df["ELITISM RATE"].astype(str)
)

# Sort and select top 10 by best fitness per step
df_sorted = df.sort_values(by="BF / STEP", ascending=False).head(10)

# Define bar colors
bar_colors = df_sorted["SOLVED"].map({True: "teal", False: "salmon"})

# Plotting
plt.figure(figsize=(14, 6))
bars = plt.bar(df_sorted["label"], df_sorted["BF / STEP"], color=bar_colors)

plt.xticks(rotation=45, ha="right", fontsize=8)
plt.ylabel("Best Fitness per Step")
plt.title("Top 10 Parameter Combinations by Best Fitness per Step")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='teal', label='Solved'),
    mpatches.Patch(facecolor='salmon', label='Not Solved')
]
plt.legend(handles=legend_elements, title="Outcome")

plt.tight_layout()
plt.savefig("results/compiled/top10_results_barplot.png")
plt.show()
