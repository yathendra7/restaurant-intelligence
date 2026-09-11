import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# LEVEL 2 - TASK 4: RESTAURANT CHAINS
# ============================================================

# File paths
input_file = r"data\Dataset.csv"
output_folder = r"Level_2\Task_4_Restaurant_Chains\output"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

print("=" * 60)
print("LEVEL 2 - TASK 4: RESTAURANT CHAINS")
print("=" * 60)

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(input_file)

print("Dataset loaded successfully.")
print(f"Total restaurants: {len(df)}")

# ============================================================
# 2. CHECK RESTAURANT NAMES
# ============================================================

print("\nAnalyzing restaurant names...")

# Remove missing restaurant names
df = df.dropna(subset=["Restaurant Name"]).copy()

# Count number of outlets for each restaurant name
chain_counts = (
    df.groupby("Restaurant Name")
    .size()
    .reset_index(name="Number of Outlets")
    .sort_values("Number of Outlets", ascending=False)
)

# ============================================================
# 3. IDENTIFY RESTAURANT CHAINS
# ============================================================

# A restaurant name appearing more than once is treated as a chain
chains = chain_counts[chain_counts["Number of Outlets"] > 1].copy()

print(f"\nUnique restaurant names: {len(chain_counts)}")
print(f"Restaurant chains identified: {len(chains)}")

print("\nTop 20 restaurant chains by number of outlets:")

print(
    chains.head(20).to_string(index=False)
)

# Save chain counts
chain_count_output = os.path.join(
    output_folder,
    "restaurant_chain_outlet_counts.csv"
)

chains.to_csv(chain_count_output, index=False)

print("\nChain outlet counts saved to:")
print(chain_count_output)

# ============================================================
# 4. ANALYZE RATINGS AND VOTES
# ============================================================

print("\nAnalyzing chain ratings and popularity...")

chain_analysis = (
    df.groupby("Restaurant Name")
    .agg(
        Number_of_Outlets=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean"),
        Total_Votes=("Votes", "sum"),
        Average_Votes=("Votes", "mean")
    )
    .reset_index()
)

# Keep only restaurant names appearing more than once
chain_analysis = chain_analysis[
    chain_analysis["Number_of_Outlets"] > 1
].copy()

# Round numerical values
chain_analysis["Average_Rating"] = chain_analysis[
    "Average_Rating"
].round(2)

chain_analysis["Average_Votes"] = chain_analysis[
    "Average_Votes"
].round(2)

# Sort by number of outlets
chain_analysis = chain_analysis.sort_values(
    "Number_of_Outlets",
    ascending=False
)

# Save complete chain analysis
chain_analysis_output = os.path.join(
    output_folder,
    "restaurant_chain_analysis.csv"
)

chain_analysis.to_csv(
    chain_analysis_output,
    index=False
)

print("\nComplete chain analysis saved to:")
print(chain_analysis_output)

# ============================================================
# 5. TOP CHAINS BY OUTLETS
# ============================================================

print("\n" + "=" * 60)
print("TOP CHAINS BY NUMBER OF OUTLETS")
print("=" * 60)

top_outlets = chain_analysis.head(15)

print(
    top_outlets[
        [
            "Restaurant Name",
            "Number_of_Outlets",
            "Average_Rating",
            "Total_Votes"
        ]
    ].to_string(index=False)
)

# ============================================================
# 6. TOP CHAINS BY AVERAGE RATING
# ============================================================

print("\n" + "=" * 60)
print("HIGHEST-RATED RESTAURANT CHAINS")
print("=" * 60)

# Require at least 3 outlets to make rating comparison more meaningful
high_rated_chains = chain_analysis[
    chain_analysis["Number_of_Outlets"] >= 3
].sort_values(
    "Average_Rating",
    ascending=False
)

print(
    high_rated_chains.head(15)[
        [
            "Restaurant Name",
            "Number_of_Outlets",
            "Average_Rating",
            "Total_Votes"
        ]
    ].to_string(index=False)
)

# Save highest-rated chains
rating_output = os.path.join(
    output_folder,
    "highest_rated_restaurant_chains.csv"
)

high_rated_chains.to_csv(
    rating_output,
    index=False
)

print("\nHighest-rated chain analysis saved to:")
print(rating_output)

# ============================================================
# 7. MOST POPULAR CHAINS BY TOTAL VOTES
# ============================================================

print("\n" + "=" * 60)
print("MOST POPULAR RESTAURANT CHAINS")
print("=" * 60)

popular_chains = chain_analysis.sort_values(
    "Total_Votes",
    ascending=False
)

print(
    popular_chains.head(15)[
        [
            "Restaurant Name",
            "Number_of_Outlets",
            "Average_Rating",
            "Total_Votes"
        ]
    ].to_string(index=False)
)

# Save popularity analysis
popularity_output = os.path.join(
    output_folder,
    "most_popular_restaurant_chains.csv"
)

popular_chains.to_csv(
    popularity_output,
    index=False
)

print("\nPopular chain analysis saved to:")
print(popularity_output)

# ============================================================
# 8. CHART - TOP CHAINS BY OUTLETS
# ============================================================

print("\nCreating restaurant chain outlet chart...")

top_outlets_chart = chain_analysis.head(15).sort_values(
    "Number_of_Outlets",
    ascending=True
)

plt.figure(figsize=(12, 8))

plt.barh(
    top_outlets_chart["Restaurant Name"],
    top_outlets_chart["Number_of_Outlets"]
)

plt.title(
    "Top 15 Restaurant Chains by Number of Outlets",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Outlets")
plt.ylabel("Restaurant Chain")

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()

outlet_chart = os.path.join(
    output_folder,
    "top_restaurant_chains_by_outlets.png"
)

plt.savefig(outlet_chart, dpi=300)
plt.close()

print("Outlet chart saved to:")
print(outlet_chart)

# ============================================================
# 9. CHART - TOP CHAINS BY RATING
# ============================================================

print("\nCreating restaurant chain rating chart...")

top_rating_chart = high_rated_chains.head(10).sort_values(
    "Average_Rating",
    ascending=True
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_rating_chart["Restaurant Name"],
    top_rating_chart["Average_Rating"]
)

plt.title(
    "Top 10 Restaurant Chains by Average Rating",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Average Rating")
plt.ylabel("Restaurant Chain")

plt.xlim(0, 5)

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()

rating_chart = os.path.join(
    output_folder,
    "top_restaurant_chains_by_rating.png"
)

plt.savefig(rating_chart, dpi=300)
plt.close()

print("Rating chart saved to:")
print(rating_chart)

# ============================================================
# 10. CHART - MOST POPULAR CHAINS
# ============================================================

print("\nCreating restaurant chain popularity chart...")

top_popular_chart = popular_chains.head(10).sort_values(
    "Total_Votes",
    ascending=True
)

plt.figure(figsize=(12, 7))

plt.barh(
    top_popular_chart["Restaurant Name"],
    top_popular_chart["Total_Votes"]
)

plt.title(
    "Top 10 Most Popular Restaurant Chains by Total Votes",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Total Votes")
plt.ylabel("Restaurant Chain")

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()

popularity_chart = os.path.join(
    output_folder,
    "top_restaurant_chains_by_votes.png"
)

plt.savefig(popularity_chart, dpi=300)
plt.close()

print("Popularity chart saved to:")
print(popularity_chart)

# ============================================================
# 11. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("RESTAURANT CHAIN ANALYSIS SUMMARY")
print("=" * 60)

if len(chain_analysis) > 0:

    top_chain = chain_analysis.iloc[0]

    print(
        f"\nChain with the most outlets: "
        f"{top_chain['Restaurant Name']}"
    )

    print(
        f"Number of outlets: "
        f"{int(top_chain['Number_of_Outlets'])}"
    )

    best_rated = high_rated_chains.iloc[0]

    print(
        f"\nHighest-rated chain (minimum 3 outlets): "
        f"{best_rated['Restaurant Name']}"
    )

    print(
        f"Average rating: "
        f"{best_rated['Average_Rating']:.2f}"
    )

    most_popular = popular_chains.iloc[0]

    print(
        f"\nMost popular chain by total votes: "
        f"{most_popular['Restaurant Name']}"
    )

    print(
        f"Total votes: "
        f"{int(most_popular['Total_Votes'])}"
    )

print("\n" + "=" * 60)
print("TASK 4 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGenerated files:")

print("1. restaurant_chain_outlet_counts.csv")
print("2. restaurant_chain_analysis.csv")
print("3. highest_rated_restaurant_chains.csv")
print("4. most_popular_restaurant_chains.csv")
print("5. top_restaurant_chains_by_outlets.png")
print("6. top_restaurant_chains_by_rating.png")
print("7. top_restaurant_chains_by_votes.png")