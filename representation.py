import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

# Load scores
with open(os.path.join(output_dir, 'wallet_scores.json'), 'r') as f:
    wallet_scores = json.load(f)

scores = list(wallet_scores.values())

# Create bins
bin_width = 2
max_score = max(scores)
bins = list(range(0, max_score + bin_width, bin_width))

# Histogram
counts, bin_edges = np.histogram(scores, bins=bins)
bin_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1]-1)}" for i in range(len(bin_edges)-1)]

# Plot
plt.figure(figsize=(9, 3.5))
bars = plt.bar(bin_labels, counts, color='cornflowerblue', edgecolor='black')

plt.xlabel("Credit Score Range", fontsize=12)
plt.ylabel("Number of Wallets", fontsize=12)
plt.title("Wallet Credit Score Distribution", fontsize=14)
plt.grid(axis='y', alpha=0.7)
plt.ylim(0, max(counts) * 1.15)

# Show only every 5th x label
for i, label in enumerate(plt.gca().xaxis.get_ticklabels()):
    if i % 5 != 0:
        label.set_visible(False)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save figure in output folder
output_path = os.path.join(output_dir, "credit_score_distribution.png")
plt.savefig(output_path, dpi=120)
plt.show()
