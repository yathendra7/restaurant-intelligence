import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# COGNIFYZ DATA ANALYSIS INTERNSHIP
# LEVEL 2 - TASK 1
# RESTAURANT RATINGS ANALYSIS
# ============================================================

print("=" * 70)
print("COGNIFYZ DATA ANALYSIS INTERNSHIP")
print("LEVEL 2 - TASK 1: RESTAURANT RATINGS")
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
# STEP 4: Check Aggregate Rating column
# ------------------------------------------------------------

print("\nAggregate Rating column found successfully!")

print("\nAggregate Rating Values:")
print(
    df["Aggregate rating"]
    .value_counts()
    .sort_index()
)

# ------------------------------------------------------------
# STEP 5: Remove missing ratings
# ------------------------------------------------------------

rating_data = df.dropna(
    subset=["Aggregate rating"]
).copy()

# ------------------------------------------------------------
# STEP 6: Rating distribution
# ------------------------------------------------------------

rating_distribution = (
    rating_data["Aggregate rating"]
    .value_counts()
    .sort_index()
)

total_rated_restaurants = len(rating_data)

rating_percentages = (
    rating_distribution / total_rated_restaurants
) * 100

# ------------------------------------------------------------
# STEP 7: Display rating distribution
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AGGREGATE RATING DISTRIBUTION")
print("=" * 70)

for rating, count in rating_distribution.items():

    percentage = rating_percentages[rating]

    print(f"\nRating: {rating:.1f}")
    print(f"Number of Restaurants : {count}")
    print(f"Percentage            : {percentage:.2f}%")

# ------------------------------------------------------------
# STEP 8: Find most common rating
# ------------------------------------------------------------

most_common_rating = rating_distribution.idxmax()
most_common_count = rating_distribution.max()

most_common_percentage = (
    rating_percentages[most_common_rating]
)

print("\n" + "=" * 70)
print("MOST COMMON RATING")
print("=" * 70)

print(f"\nMost Common Rating       : {most_common_rating:.1f}")
print(f"Number of Restaurants   : {most_common_count}")
print(f"Percentage              : {most_common_percentage:.2f}%")

# ------------------------------------------------------------
# STEP 9: Calculate rating ranges
# ------------------------------------------------------------

def get_rating_range(rating):

    if rating == 0:
        return "0.0"

    elif rating < 1.0:
        return "0.1 - 0.9"

    elif rating < 2.0:
        return "1.0 - 1.9"

    elif rating < 3.0:
        return "2.0 - 2.9"

    elif rating < 4.0:
        return "3.0 - 3.9"

    else:
        return "4.0 - 5.0"


rating_data["Rating Range"] = (
    rating_data["Aggregate rating"]
    .apply(get_rating_range)
)

rating_range_distribution = (
    rating_data["Rating Range"]
    .value_counts()
)

range_order = [
    "0.0",
    "0.1 - 0.9",
    "1.0 - 1.9",
    "2.0 - 2.9",
    "3.0 - 3.9",
    "4.0 - 5.0"
]

rating_range_distribution = (
    rating_range_distribution
    .reindex(range_order)
    .fillna(0)
)

rating_range_percentages = (
    rating_range_distribution /
    total_rated_restaurants
) * 100

# ------------------------------------------------------------
# STEP 10: Display rating range analysis
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RATING RANGE DISTRIBUTION")
print("=" * 70)

for rating_range, count in rating_range_distribution.items():

    percentage = rating_range_percentages[rating_range]

    print(f"\nRating Range: {rating_range}")
    print(f"Number of Restaurants : {int(count)}")
    print(f"Percentage            : {percentage:.2f}%")

# ------------------------------------------------------------
# STEP 11: Find most common rating range
# ------------------------------------------------------------

most_common_range = (
    rating_range_distribution.idxmax()
)

most_common_range_count = (
    rating_range_distribution.max()
)

most_common_range_percentage = (
    rating_range_percentages[most_common_range]
)

print("\n" + "=" * 70)
print("MOST COMMON RATING RANGE")
print("=" * 70)

print(f"\nMost Common Rating Range : {most_common_range}")
print(
    f"Number of Restaurants    : "
    f"{int(most_common_range_count)}"
)
print(
    f"Percentage               : "
    f"{most_common_range_percentage:.2f}%"
)

# ------------------------------------------------------------
# STEP 12: Calculate average number of votes
# ------------------------------------------------------------

average_votes = df["Votes"].mean()

print("\n" + "=" * 70)
print("AVERAGE NUMBER OF VOTES")
print("=" * 70)

print(f"\nAverage Votes per Restaurant: {average_votes:.2f}")

# ------------------------------------------------------------
# STEP 13: Create rating summary table
# ------------------------------------------------------------

rating_summary = pd.DataFrame({
    "Aggregate Rating": rating_distribution.index,
    "Restaurant Count": rating_distribution.values,
    "Percentage": rating_percentages.values
})

print("\n" + "=" * 70)
print("RATING SUMMARY TABLE")
print("=" * 70)

print(
    rating_summary.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 14: Create rating range summary
# ------------------------------------------------------------

rating_range_summary = pd.DataFrame({
    "Rating Range": rating_range_distribution.index,
    "Restaurant Count": (
        rating_range_distribution.values.astype(int)
    ),
    "Percentage": rating_range_percentages.values
})

print("\n" + "=" * 70)
print("RATING RANGE SUMMARY TABLE")
print("=" * 70)

print(
    rating_range_summary.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 15: Create output folder
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
# STEP 16: Save rating distribution CSV
# ------------------------------------------------------------

rating_csv_path = os.path.join(
    OUTPUT_DIR,
    "restaurant_rating_distribution.csv"
)

rating_summary.to_csv(
    rating_csv_path,
    index=False
)

print("\nRating distribution CSV created!")
print(rating_csv_path)

# ------------------------------------------------------------
# STEP 17: Save rating range CSV
# ------------------------------------------------------------

range_csv_path = os.path.join(
    OUTPUT_DIR,
    "restaurant_rating_ranges.csv"
)

rating_range_summary.to_csv(
    range_csv_path,
    index=False
)

print("\nRating range CSV created!")
print(range_csv_path)

# ------------------------------------------------------------
# STEP 18: Create rating distribution chart
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    rating_distribution.index.astype(str),
    rating_distribution.values
)

plt.xlabel("Aggregate Rating")
plt.ylabel("Number of Restaurants")

plt.title(
    "Distribution of Restaurant Aggregate Ratings"
)

plt.tight_layout()

rating_chart_path = os.path.join(
    OUTPUT_DIR,
    "restaurant_rating_distribution.png"
)

plt.savefig(
    rating_chart_path,
    dpi=300
)

plt.close()

print("\nRating distribution chart created!")
print(rating_chart_path)

# ------------------------------------------------------------
# STEP 19: Create rating range chart
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    rating_range_distribution.index,
    rating_range_distribution.values
)

plt.xlabel("Rating Range")
plt.ylabel("Number of Restaurants")

plt.title(
    "Restaurant Rating Range Distribution"
)

plt.xticks(rotation=30)

plt.tight_layout()

range_chart_path = os.path.join(
    OUTPUT_DIR,
    "restaurant_rating_range_distribution.png"
)

plt.savefig(
    range_chart_path,
    dpi=300
)

plt.close()

print("\nRating range chart created!")
print(range_chart_path)

# ------------------------------------------------------------
# STEP 20: Final conclusion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TASK 1 CONCLUSION")
print("=" * 70)

print(
    f"\nThe most common aggregate rating is "
    f"{most_common_rating:.1f}, with "
    f"{most_common_count} restaurants."
)

print(
    f"The most common rating range is "
    f"{most_common_range}, containing "
    f"{int(most_common_range_count)} restaurants."
)

print(
    f"The average number of votes per restaurant "
    f"is {average_votes:.2f}."
)

# ------------------------------------------------------------
# TASK COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LEVEL 2 - TASK 1 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created inside the output folder:")
print("1. restaurant_rating_distribution.csv")
print("2. restaurant_rating_ranges.csv")
print("3. restaurant_rating_distribution.png")
print("4. restaurant_rating_range_distribution.png")

print("\nYou can use these files in your internship submission/report.")