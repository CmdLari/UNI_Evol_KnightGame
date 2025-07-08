import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your data
df = pd.read_csv("results/compiled/144_noElitism_compiled_results.csv")

# Create a label including all key parameters
df["label"] = (
    "BS=" + df["BOARD SIZE"].astype(str)
    + " | POP=" + df["POP SIZE"].astype(str)
    + " | GEN=" + df["GENERATIONS"].astype(str)
    + " | CR=" + df["CR"].astype(str)
    + " \nSTPSIZE=" + df["STEPSIZE"].astype(str)
    + " | STPS=" + df["STEPS"].astype(str)
    + " \nOBSTACLES=" + df["OBSTACLES"].astype(str)
    + " \nELITISM=" + df["ELITISM"].astype(str)
    + " | ELITISM RATE=" + df["ELITISM RATE"].astype(str)
)

# Select top 3 and worst 3 by best fitness per step
top_3 = df.sort_values(by="BF / STEP", ascending=False).head(3)
bottom_3 = df.sort_values(by="BF / STEP", ascending=True).head(3)
df_combined = pd.concat([top_3, bottom_3])

# Assign colors
colors = ["teal"] * 3 + ["salmon"] * 3

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.barh(df_combined["label"], df_combined["BF / STEP"], color=colors)

# Add text labels to bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
             f"{width:.2f}", va='center', fontsize=8)

plt.yticks(fontsize=8)
plt.xlabel("Best Fitness per Step")
plt.title("Top and Bottom 3 Parameter Combinations by Best Fitness per Step")
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='teal', label='Top 3'),
    mpatches.Patch(facecolor='salmon', label='Bottom 3')
]
plt.legend(handles=legend_elements, title="Performance")

plt.tight_layout()
plt.savefig("results/compiled/top_and_bottom_results_plot.png")
plt.show()
