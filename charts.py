import matplotlib.pyplot as plt
from case import df, h1_results, opportunities

# --- CHART 1: Hypothesis 1 (Minimalist & Spaced Style)---

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left plot: Average Rating
axes[0].bar(
    h1_results.index,
    h1_results["Avg_Rating"],
    width=0.45,
    color="#5C89B5",
    alpha=0.9
)
axes[0].set_title("Avg Rating by Runtime Category", fontsize=12, fontweight="bold", pad=15)
axes[0].set_ylabel("Average Rating (1-10)", fontsize=10)
axes[0].set_ylim(0, 10)

# Right plot: Average Votes
axes[1].bar(
    h1_results.index,
    h1_results["Avg_Votes"],
    width=0.45,
    color="#E89B54",
    alpha=0.9
)
axes[1].set_title("Avg Votes (Engagement) by Runtime Category", fontsize=12, fontweight="bold", pad=15)
axes[1].set_ylabel("Average Votes", fontsize=10)

# Apply delicate/minimalist styling to both charts at once
for ax in axes:
    ax.tick_params(axis="x", rotation=18, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)  # Keeps grid lines behind the bars

# Increase horizontal space between the two plots
plt.tight_layout(w_pad=5)
plt.savefig("chart1_hypothesis1_runtime.png", dpi=300)
plt.show()

# --- CHART 2: Hypothesis 2 (Votes vs. Metascore against Revenue) ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left plot: Votes vs. Revenue
axes[0].scatter(
    df["Votes"],
    df["Revenue (Millions)"],
    s=28,
    alpha=0.45,
    color="#4A9B9B",
    edgecolors="none"
)
axes[0].set_title("Audience Engagement (Votes) vs. Revenue", fontsize=12, fontweight="bold", pad=15)
axes[0].set_xlabel("Votes", fontsize=10)
axes[0].set_ylabel("Revenue (Millions $)", fontsize=10)

# Right plot: Metascore vs. Revenue
axes[1].scatter(
    df["Metascore"],
    df["Revenue (Millions)"],
    s=28,
    alpha=0.45,
    color="#D96B6B",
    edgecolors="none"
)
axes[1].set_title("Critic Score (Metascore) vs. Revenue", fontsize=12, fontweight="bold", pad=15)
axes[1].set_xlabel("Metascore (0-100)", fontsize=10)
axes[1].set_ylabel("Revenue (Millions $)", fontsize=10)

# Apply minimalist styling to both scatter plots
for ax in axes:
    ax.tick_params(labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)

plt.tight_layout(w_pad=5)
plt.savefig("chart2_hypothesis2_correlation.png", dpi=300)
plt.show()

# --- CHART 3: Main Question (Top 10 Market Opportunities) ---
top10 = opportunities.head(10).reset_index()
top10["Niche"] = top10["Genre"] + "  |  " + top10["Runtime_Category"]
top10 = top10.iloc[::-1]  # Reverse order so #1 appears at the top

fig, ax = plt.subplots(figsize=(12.5, 6))

bars = ax.barh(
    top10["Niche"],
    top10["Avg_Revenue"],
    height=0.52,
    color="#5FA884",
    alpha=0.9
)

ax.set_title("Top 10 Market Opportunities (Avg Revenue, Supply & Rating)", fontsize=12, fontweight="bold", pad=15)
ax.set_xlabel("Average Revenue (Millions $)", fontsize=10)
ax.set_xlim(0, top10["Avg_Revenue"].max() * 1.42)
ax.tick_params(labelsize=9)

# Minimalist styling
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")
ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

# Clean labels next to each bar
for bar, (_, row) in zip(bars, top10.iterrows()):
    label = f"${row['Avg_Revenue']:.1f}M  |  {int(row['Movie_Supply'])} movies  |  Rating: {row['Avg_Rating']}"
    ax.text(
        bar.get_width() + 5,
        bar.get_y() + bar.get_height() / 2,
        label,
        va="center",
        fontsize=9,
        color="#333333"
    )

plt.tight_layout()
plt.savefig("chart3_main_opportunities.png", dpi=300)
plt.show()