import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# LEVEL 3 - TASK 2: VOTES ANALYSIS
# ============================================================

input_file = r"data\Dataset.csv"
output_folder = r"Level_3\Task_2_Votes_Analysis\output"

os.makedirs(output_folder, exist_ok=True)

print("=" * 65)
print("LEVEL 3 - TASK 2: VOTES ANALYSIS")
print("=" * 65)

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(input_file)

print(f"Dataset loaded successfully.")
print(f"Total restaurants: {len(df)}")

# ============================================================
# 2. CHECK AND CLEAN VOTES DATA
# ============================================================

print("\nChecking Votes data...")

df["Votes"] = pd.to_numeric(
    df["Votes"],
    errors="coerce"
)

df["Aggregate rating"] = pd.to_numeric(
    df["Aggregate rating"],
    errors="coerce"
)

valid_votes = df.dropna(
    subset=["Votes", "Aggregate rating"]
).copy()

print(f"Valid vote/rating records: {len(valid_votes)}")
print(f"Missing vote/rating records: {len(df) - len(valid_votes)}")

# ============================================================
# 3. BASIC VOTE STATISTICS
# ============================================================

print("\nCalculating vote statistics...")

print(f"Minimum votes: {valid_votes['Votes'].min()}")
print(f"Maximum votes: {valid_votes['Votes'].max()}")
print(f"Average votes: {valid_votes['Votes'].mean():.2f}")
print(f"Median votes: {valid_votes['Votes'].median():.2f}")

# ============================================================
# 4. TOP 10 RESTAURANTS BY VOTES
# ============================================================

print("\n" + "=" * 65)
print("TOP 10 RESTAURANTS BY NUMBER OF VOTES")
print("=" * 65)

highest_votes = valid_votes.sort_values(
    "Votes",
    ascending=False
).head(10)

print(
    highest_votes[
        [
            "Restaurant Name",
            "City",
            "Votes",
            "Aggregate rating",
            "Cuisines"
        ]
    ].to_string(index=False)
)

highest_votes_output = os.path.join(
    output_folder,
    "top_10_restaurants_by_votes.csv"
)

highest_votes[
    [
        "Restaurant Name",
        "City",
        "Votes",
        "Aggregate rating",
        "Cuisines"
    ]
].to_csv(
    highest_votes_output,
    index=False
)

print("\nSaved:")
print(highest_votes_output)

# ============================================================
# 5. LOWEST VOTE RESTAURANTS
# ============================================================

print("\n" + "=" * 65)
print("RESTAURANTS WITH LOWEST NUMBER OF VOTES")
print("=" * 65)

lowest_votes = valid_votes.sort_values(
    "Votes",
    ascending=True
).head(10)

print(
    lowest_votes[
        [
            "Restaurant Name",
            "City",
            "Votes",
            "Aggregate rating",
            "Cuisines"
        ]
    ].to_string(index=False)
)

lowest_votes_output = os.path.join(
    output_folder,
    "lowest_10_restaurants_by_votes.csv"
)

lowest_votes[
    [
        "Restaurant Name",
        "City",
        "Votes",
        "Aggregate rating",
        "Cuisines"
    ]
].to_csv(
    lowest_votes_output,
    index=False
)

print("\nSaved:")
print(lowest_votes_output)

# ============================================================
# 6. VOTES VS RATING CORRELATION
# ============================================================

print("\n" + "=" * 65)
print("VOTES VS AGGREGATE RATING CORRELATION")
print("=" * 65)

correlation = valid_votes[
    ["Votes", "Aggregate rating"]
].corr().loc[
    "Votes",
    "Aggregate rating"
]

print(
    f"\nCorrelation coefficient: {correlation:.4f}"
)

# Interpret correlation
if correlation > 0.7:
    interpretation = "Strong positive correlation"

elif correlation > 0.3:
    interpretation = "Moderate positive correlation"

elif correlation > 0:
    interpretation = "Weak positive correlation"

elif correlation < -0.7:
    interpretation = "Strong negative correlation"

elif correlation < -0.3:
    interpretation = "Moderate negative correlation"

elif correlation < 0:
    interpretation = "Weak negative correlation"

else:
    interpretation = "No significant linear correlation"

print(f"Interpretation: {interpretation}")

# Save correlation result
correlation_output = os.path.join(
    output_folder,
    "votes_rating_correlation.csv"
)

correlation_df = pd.DataFrame({
    "Metric": [
        "Correlation between Votes and Aggregate Rating"
    ],
    "Correlation Coefficient": [
        round(correlation, 4)
    ],
    "Interpretation": [
        interpretation
    ]
})

correlation_df.to_csv(
    correlation_output,
    index=False
)

print("\nSaved:")
print(correlation_output)

# ============================================================
# 7. VOTE DISTRIBUTION
# ============================================================

print("\nCreating vote distribution chart...")

plt.figure(figsize=(10, 6))

plt.hist(
    valid_votes["Votes"],
    bins=50,
    alpha=0.7
)

plt.title(
    "Distribution of Restaurant Votes",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Votes")
plt.ylabel("Number of Restaurants")

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

vote_distribution_chart = os.path.join(
    output_folder,
    "vote_distribution.png"
)

plt.savefig(
    vote_distribution_chart,
    dpi=300
)

plt.close()

print("Saved:")
print(vote_distribution_chart)

# ============================================================
# 8. VOTES VS RATING SCATTER PLOT
# ============================================================

print("\nCreating Votes vs Rating scatter plot...")

plt.figure(figsize=(10, 7))

plt.scatter(
    valid_votes["Votes"],
    valid_votes["Aggregate rating"],
    s=12,
    alpha=0.4
)

plt.title(
    "Relationship Between Votes and Aggregate Rating",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Votes")
plt.ylabel("Aggregate Rating")

plt.grid(
    alpha=0.3
)

plt.tight_layout()

scatter_output = os.path.join(
    output_folder,
    "votes_vs_rating_scatter.png"
)

plt.savefig(
    scatter_output,
    dpi=300
)

plt.close()

print("Saved:")
print(scatter_output)

# ============================================================
# 9. TOP 10 VOTED RESTAURANT CHART
# ============================================================

print("\nCreating top voted restaurants chart...")

top_chart = highest_votes.sort_values(
    "Votes",
    ascending=True
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_chart["Restaurant Name"],
    top_chart["Votes"]
)

plt.title(
    "Top 10 Restaurants by Number of Votes",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Votes")
plt.ylabel("Restaurant")

plt.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

top_votes_chart = os.path.join(
    output_folder,
    "top_10_restaurants_by_votes.png"
)

plt.savefig(
    top_votes_chart,
    dpi=300
)

plt.close()

print("Saved:")
print(top_votes_chart)

# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("VOTES ANALYSIS SUMMARY")
print("=" * 65)

top_restaurant = highest_votes.iloc[0]

print(
    f"\nRestaurant with highest votes: "
    f"{top_restaurant['Restaurant Name']}"
)

print(
    f"City: {top_restaurant['City']}"
)

print(
    f"Votes: {int(top_restaurant['Votes'])}"
)

print(
    f"Aggregate rating: "
    f"{top_restaurant['Aggregate rating']:.2f}"
)

lowest_restaurant = lowest_votes.iloc[0]

print(
    f"\nRestaurant with lowest votes: "
    f"{lowest_restaurant['Restaurant Name']}"
)

print(
    f"City: {lowest_restaurant['City']}"
)

print(
    f"Votes: {int(lowest_restaurant['Votes'])}"
)

print(
    f"Aggregate rating: "
    f"{lowest_restaurant['Aggregate rating']:.2f}"
)

print(
    f"\nVotes-Rating correlation: "
    f"{correlation:.4f}"
)

print(
    f"Interpretation: {interpretation}"
)

print("\n" + "=" * 65)
print("TASK 2 COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nGenerated files:")

print("1. top_10_restaurants_by_votes.csv")
print("2. lowest_10_restaurants_by_votes.csv")
print("3. votes_rating_correlation.csv")
print("4. vote_distribution.png")
print("5. votes_vs_rating_scatter.png")
print("6. top_10_restaurants_by_votes.png")