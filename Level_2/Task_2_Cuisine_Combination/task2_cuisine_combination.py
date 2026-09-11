import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# COGNIFYZ DATA ANALYSIS INTERNSHIP
# LEVEL 2 - TASK 2
# CUISINE COMBINATION ANALYSIS
# ============================================================

print("=" * 70)
print("COGNIFYZ DATA ANALYSIS INTERNSHIP")
print("LEVEL 2 - TASK 2: CUISINE COMBINATION")
print("=" * 70)

# ------------------------------------------------------------
# STEP 1: Find project directory
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# ------------------------------------------------------------
# STEP 2: Dataset path
# ------------------------------------------------------------

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Dataset.csv"
)

print("\nLoading dataset...")
print(f"Dataset path: {DATA_PATH}")

# ------------------------------------------------------------
# STEP 3: Load dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)

# ------------------------------------------------------------
# STEP 4: Check required columns
# ------------------------------------------------------------

print("\nRequired columns:")
print("- Cuisines")
print("- Aggregate rating")

# ------------------------------------------------------------
# STEP 5: Check missing cuisine values
# ------------------------------------------------------------

missing_cuisines = df["Cuisines"].isna().sum()

print("\nMissing Cuisine Values:")
print(missing_cuisines)

# ------------------------------------------------------------
# STEP 6: Remove restaurants without cuisine information
# ------------------------------------------------------------

cuisine_data = df.dropna(
    subset=["Cuisines"]
).copy()

# Remove leading/trailing spaces
cuisine_data["Cuisines"] = (
    cuisine_data["Cuisines"]
    .str.strip()
)

# ------------------------------------------------------------
# STEP 7: Find most common cuisine combinations
# ------------------------------------------------------------

cuisine_counts = (
    cuisine_data["Cuisines"]
    .value_counts()
)

print("\n" + "=" * 70)
print("TOP CUISINE COMBINATIONS")
print("=" * 70)

top_cuisines = cuisine_counts.head(10)

for cuisine, count in top_cuisines.items():

    print(f"\n{cuisine}")
    print(f"Number of Restaurants: {count}")

# ------------------------------------------------------------
# STEP 8: Calculate percentages
# ------------------------------------------------------------

total_cuisine_restaurants = len(cuisine_data)

top_cuisine_percentages = (
    top_cuisines / total_cuisine_restaurants
) * 100

# ------------------------------------------------------------
# STEP 9: Create top cuisine summary
# ------------------------------------------------------------

top_cuisine_summary = pd.DataFrame({
    "Cuisine Combination": top_cuisines.index,
    "Restaurant Count": top_cuisines.values,
    "Percentage": top_cuisine_percentages.values
})

print("\n" + "=" * 70)
print("TOP CUISINE COMBINATION SUMMARY")
print("=" * 70)

print(
    top_cuisine_summary.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 10: Calculate average rating for each cuisine
# ------------------------------------------------------------

cuisine_rating_analysis = (
    cuisine_data
    .groupby("Cuisines")
    .agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean")
    )
    .reset_index()
)

# ------------------------------------------------------------
# STEP 11: Remove cuisine combinations with very few
# restaurants for meaningful rating comparison
# ------------------------------------------------------------

minimum_restaurants = 5

rating_analysis_filtered = (
    cuisine_rating_analysis[
        cuisine_rating_analysis["Restaurant_Count"]
        >= minimum_restaurants
    ]
    .copy()
)

# ------------------------------------------------------------
# STEP 12: Sort by average rating
# ------------------------------------------------------------

highest_rated_combinations = (
    rating_analysis_filtered
    .sort_values(
        by="Average_Rating",
        ascending=False
    )
    .head(10)
)

# ------------------------------------------------------------
# STEP 13: Display highest rated combinations
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("HIGHEST RATED CUISINE COMBINATIONS")
print("=" * 70)

print(
    highest_rated_combinations.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 14: Find ratings of most common combinations
# ------------------------------------------------------------

top_cuisine_rating_analysis = (
    cuisine_rating_analysis[
        cuisine_rating_analysis["Cuisines"]
        .isin(top_cuisines.index)
    ]
    .sort_values(
        by="Average_Rating",
        ascending=False
    )
)

print("\n" + "=" * 70)
print("RATINGS OF MOST COMMON CUISINE COMBINATIONS")
print("=" * 70)

print(
    top_cuisine_rating_analysis.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 15: Identify highest rated cuisine combination
# ------------------------------------------------------------

highest_rated_cuisine = (
    highest_rated_combinations.iloc[0]
)

print("\n" + "=" * 70)
print("HIGHEST RATED CUISINE FINDING")
print("=" * 70)

print(
    f"\nCuisine Combination: "
    f"{highest_rated_cuisine['Cuisines']}"
)

print(
    f"Number of Restaurants: "
    f"{int(highest_rated_cuisine['Restaurant_Count'])}"
)

print(
    f"Average Rating: "
    f"{highest_rated_cuisine['Average_Rating']:.2f}"
)

# ------------------------------------------------------------
# STEP 16: Create output folder
# ------------------------------------------------------------

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "output"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ------------------------------------------------------------
# STEP 17: Save top cuisine combinations
# ------------------------------------------------------------

top_cuisine_csv = os.path.join(
    OUTPUT_DIR,
    "top_cuisine_combinations.csv"
)

top_cuisine_summary.to_csv(
    top_cuisine_csv,
    index=False
)

print("\nTop cuisine combinations CSV created!")
print(top_cuisine_csv)

# ------------------------------------------------------------
# STEP 18: Save cuisine rating analysis
# ------------------------------------------------------------

rating_csv = os.path.join(
    OUTPUT_DIR,
    "cuisine_rating_analysis.csv"
)

cuisine_rating_analysis.sort_values(
    by="Average_Rating",
    ascending=False
).to_csv(
    rating_csv,
    index=False
)

print("\nCuisine rating analysis CSV created!")
print(rating_csv)

# ------------------------------------------------------------
# STEP 19: Create chart for most common combinations
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.bar(
    top_cuisine_summary["Cuisine Combination"],
    top_cuisine_summary["Restaurant Count"]
)

plt.xlabel("Cuisine Combination")
plt.ylabel("Number of Restaurants")

plt.title(
    "Top 10 Most Common Cuisine Combinations"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

count_chart_path = os.path.join(
    OUTPUT_DIR,
    "top_cuisine_combinations.png"
)

plt.savefig(
    count_chart_path,
    dpi=300
)

plt.close()

print("\nCuisine combination chart created!")
print(count_chart_path)

# ------------------------------------------------------------
# STEP 20: Create chart for highest rated combinations
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.bar(
    highest_rated_combinations["Cuisines"],
    highest_rated_combinations["Average_Rating"]
)

plt.xlabel("Cuisine Combination")
plt.ylabel("Average Rating")

plt.title(
    "Highest Rated Cuisine Combinations"
)

plt.ylim(0, 5)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

rating_chart_path = os.path.join(
    OUTPUT_DIR,
    "highest_rated_cuisine_combinations.png"
)

plt.savefig(
    rating_chart_path,
    dpi=300
)

plt.close()

print("\nHighest rated cuisine chart created!")
print(rating_chart_path)

# ------------------------------------------------------------
# STEP 21: Final conclusion
# ------------------------------------------------------------

most_common_cuisine = top_cuisine_summary.iloc[0]

print("\n" + "=" * 70)
print("TASK 2 CONCLUSION")
print("=" * 70)

print(
    f"\nThe most common cuisine combination is "
    f"'{most_common_cuisine['Cuisine Combination']}', "
    f"with {int(most_common_cuisine['Restaurant Count'])} "
    f"restaurants."
)

print(
    f"The highest-rated cuisine combination among "
    f"combinations with at least {minimum_restaurants} "
    f"restaurants is "
    f"'{highest_rated_cuisine['Cuisines']}', "
    f"with an average rating of "
    f"{highest_rated_cuisine['Average_Rating']:.2f}."
)

print(
    "\nThis analysis helps identify both popular cuisine "
    "combinations and combinations associated with higher "
    "customer ratings."
)

# ------------------------------------------------------------
# TASK COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LEVEL 2 - TASK 2 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created inside the output folder:")
print("1. top_cuisine_combinations.csv")
print("2. cuisine_rating_analysis.csv")
print("3. top_cuisine_combinations.png")
print("4. highest_rated_cuisine_combinations.png")

print("\nYou can use these files in your internship submission/report.")