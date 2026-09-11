import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# COGNIFYZ DATA ANALYSIS INTERNSHIP
# LEVEL 1 - TASK 4
# ONLINE DELIVERY ANALYSIS
# ============================================================

print("=" * 70)
print("COGNIFYZ DATA ANALYSIS INTERNSHIP")
print("LEVEL 1 - TASK 4: ONLINE DELIVERY ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# STEP 1: Find the project directory
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
print("- Has Online delivery")
print("- Aggregate rating")

# ------------------------------------------------------------
# STEP 5: Check online delivery values
# ------------------------------------------------------------

print("\nOnline Delivery Values:")
print(
    df["Has Online delivery"]
    .value_counts()
)

# ------------------------------------------------------------
# STEP 6: Calculate number of restaurants
# ------------------------------------------------------------

delivery_counts = (
    df["Has Online delivery"]
    .value_counts()
)

total_restaurants = delivery_counts.sum()

# ------------------------------------------------------------
# STEP 7: Calculate percentages
# ------------------------------------------------------------

delivery_percentages = (
    delivery_counts / total_restaurants
) * 100

# ------------------------------------------------------------
# STEP 8: Display delivery percentages
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ONLINE DELIVERY DISTRIBUTION")
print("=" * 70)

for status, count in delivery_counts.items():

    percentage = delivery_percentages[status]

    print(f"\nOnline Delivery: {status}")
    print(f"Number of Restaurants : {count}")
    print(f"Percentage            : {percentage:.2f}%")

# ------------------------------------------------------------
# STEP 9: Calculate average ratings
# ------------------------------------------------------------

average_ratings = (
    df.groupby("Has Online delivery")["Aggregate rating"]
    .mean()
)

# ------------------------------------------------------------
# STEP 10: Display average ratings
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AVERAGE RATING COMPARISON")
print("=" * 70)

for status, rating in average_ratings.items():

    print(f"\nOnline Delivery: {status}")
    print(f"Average Rating: {rating:.2f}")

# ------------------------------------------------------------
# STEP 11: Compare ratings
# ------------------------------------------------------------

if "Yes" in average_ratings.index and "No" in average_ratings.index:

    yes_rating = average_ratings["Yes"]
    no_rating = average_ratings["No"]

    difference = yes_rating - no_rating

    print("\n" + "=" * 70)
    print("RATING COMPARISON RESULT")
    print("=" * 70)

    print(f"\nAverage rating WITH online delivery    : {yes_rating:.2f}")
    print(f"Average rating WITHOUT online delivery : {no_rating:.2f}")
    print(f"Rating difference                      : {difference:.2f}")

    if yes_rating > no_rating:

        print(
            "\nConclusion: Restaurants offering online delivery "
            "have a higher average rating."
        )

    elif yes_rating < no_rating:

        print(
            "\nConclusion: Restaurants without online delivery "
            "have a higher average rating."
        )

    else:

        print(
            "\nConclusion: Both groups have the same average rating."
        )

# ------------------------------------------------------------
# STEP 12: Create summary table
# ------------------------------------------------------------

result = pd.DataFrame({
    "Online Delivery": delivery_counts.index,
    "Restaurant Count": delivery_counts.values,
    "Percentage": [
        delivery_percentages[status]
        for status in delivery_counts.index
    ],
    "Average Rating": [
        average_ratings[status]
        for status in delivery_counts.index
    ]
})

print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)

print(
    result.to_string(index=False)
)

# ------------------------------------------------------------
# STEP 13: Create output folder
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
# STEP 14: Save CSV
# ------------------------------------------------------------

csv_path = os.path.join(
    OUTPUT_DIR,
    "online_delivery_analysis.csv"
)

result.to_csv(
    csv_path,
    index=False
)

print("\nCSV file created successfully!")
print(csv_path)

# ------------------------------------------------------------
# STEP 15: Create bar chart
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    average_ratings.index,
    average_ratings.values
)

plt.xlabel("Online Delivery")
plt.ylabel("Average Aggregate Rating")

plt.title(
    "Average Restaurant Rating: Online Delivery vs No Online Delivery"
)

plt.ylim(0, 5)

plt.tight_layout()

# ------------------------------------------------------------
# STEP 16: Save chart
# ------------------------------------------------------------

chart_path = os.path.join(
    OUTPUT_DIR,
    "online_delivery_rating_comparison.png"
)

plt.savefig(
    chart_path,
    dpi=300
)

plt.close()

print("\nChart created successfully!")
print(chart_path)

# ------------------------------------------------------------
# TASK COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TASK 4 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created inside the output folder:")
print("1. online_delivery_analysis.csv")
print("2. online_delivery_rating_comparison.png")

print("\nYou can use these files in your internship submission/report.")