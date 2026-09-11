import pandas as pd
import os

# ============================================================
# COGNIFYZ DATA ANALYSIS INTERNSHIP
# LEVEL 1 - TASK 2: CITY ANALYSIS
# ============================================================

print("=" * 70)
print("COGNIFYZ DATA ANALYSIS INTERNSHIP")
print("LEVEL 1 - TASK 2: CITY ANALYSIS")
print("=" * 70)


# ============================================================
# STEP 1: FIND THE PROJECT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ============================================================
# STEP 2: DEFINE DATASET PATH
# ============================================================

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Dataset.csv"
)


# ============================================================
# STEP 3: LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)


print("\nDataset loaded successfully!")


# ============================================================
# STEP 4: DISPLAY BASIC DATASET INFORMATION
# ============================================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# TASK 2 - PART 1
# CITY WITH HIGHEST NUMBER OF RESTAURANTS
# ============================================================

print("\n")
print("=" * 70)
print("PART 1: CITY WITH HIGHEST NUMBER OF RESTAURANTS")
print("=" * 70)


# Remove rows where City is missing

city_data = df.dropna(
    subset=["City"]
)


# Count restaurants in each city

city_restaurant_counts = (
    city_data["City"]
    .value_counts()
)


# Find the city with the highest number of restaurants

highest_restaurant_city = (
    city_restaurant_counts.idxmax()
)

highest_restaurant_count = (
    city_restaurant_counts.max()
)


print(
    f"\nCity with the highest number of restaurants:"
)

print(
    f"City: {highest_restaurant_city}"
)

print(
    f"Number of Restaurants: {highest_restaurant_count}"
)


# ============================================================
# DISPLAY TOP 10 CITIES
# ============================================================

print("\nTop 10 Cities by Number of Restaurants:")

top_10_cities = (
    city_restaurant_counts
    .head(10)
)


for city, count in top_10_cities.items():

    print(
        f"{city}: {count} restaurants"
    )


# ============================================================
# TASK 2 - PART 2
# AVERAGE RATING FOR EACH CITY
# ============================================================

print("\n")
print("=" * 70)
print("PART 2: AVERAGE RATING FOR EACH CITY")
print("=" * 70)


# Remove rows where City or Aggregate rating is missing

rating_data = df.dropna(
    subset=[
        "City",
        "Aggregate rating"
    ]
)


# Calculate average rating for each city

city_average_rating = (
    rating_data
    .groupby("City")["Aggregate rating"]
    .mean()
    .sort_values(
        ascending=False
    )
)


# ============================================================
# DISPLAY TOP 10 CITIES BY AVERAGE RATING
# ============================================================

print("\nTop 10 Cities by Average Rating:")

top_10_average_rating = (
    city_average_rating
    .head(10)
)


for city, rating in (
    top_10_average_rating.items()
):

    print(
        f"{city}: {rating:.2f}"
    )


# ============================================================
# TASK 2 - PART 3
# CITY WITH HIGHEST AVERAGE RATING
# ============================================================

print("\n")
print("=" * 70)
print("PART 3: CITY WITH HIGHEST AVERAGE RATING")
print("=" * 70)


# Find city with highest average rating

highest_average_rating_city = (
    city_average_rating.idxmax()
)

highest_average_rating = (
    city_average_rating.max()
)


print(
    f"\nCity with the highest average rating:"
)

print(
    f"City: {highest_average_rating_city}"
)

print(
    f"Average Rating: {highest_average_rating:.2f}"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("FINAL CITY ANALYSIS SUMMARY")
print("=" * 70)


print(
    f"\n1. City with the highest number of restaurants:"
)

print(
    f"   {highest_restaurant_city}"
)

print(
    f"   Number of Restaurants: "
    f"{highest_restaurant_count}"
)


print(
    f"\n2. City with the highest average rating:"
)

print(
    f"   {highest_average_rating_city}"
)

print(
    f"   Average Rating: "
    f"{highest_average_rating:.2f}"
)


# ============================================================
# SAVE RESULTS
# ============================================================

# Create output folder

OUTPUT_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "output"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# SAVE CITY RESTAURANT COUNTS
# ============================================================

restaurant_count_result = (
    city_restaurant_counts
    .reset_index()
)


restaurant_count_result.columns = [
    "City",
    "Restaurant Count"
]


restaurant_count_result.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "city_restaurant_counts.csv"
    ),
    index=False
)


# ============================================================
# SAVE CITY AVERAGE RATINGS
# ============================================================

average_rating_result = (
    city_average_rating
    .reset_index()
)


average_rating_result.columns = [
    "City",
    "Average Rating"
]


average_rating_result.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "city_average_ratings.csv"
    ),
    index=False
)


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 70)
print("TASK 2 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created:")

print(
    "1. city_restaurant_counts.csv"
)

print(
    "2. city_average_ratings.csv"
)

print("\nOutput folder:")
print(OUTPUT_DIR)