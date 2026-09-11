import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# COGNIFYZ DATA ANALYSIS INTERNSHIP
# LEVEL 1 - TASK 3
# PRICE RANGE DISTRIBUTION
# ============================================================

print("=" * 70)
print("COGNIFYZ DATA ANALYSIS INTERNSHIP")
print("LEVEL 1 - TASK 3: PRICE RANGE DISTRIBUTION")
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
# STEP 4: Check Price range column
# ------------------------------------------------------------

print("\nPrice range column found successfully!")

print("\nPrice Range Values:")
print(df["Price range"].value_counts().sort_index())

# ------------------------------------------------------------
# STEP 5: Remove missing Price range values
# ------------------------------------------------------------

price_data = df.dropna(
    subset=["Price range"]
).copy()

# ------------------------------------------------------------
# STEP 6: Calculate number of restaurants
# ------------------------------------------------------------

price_counts = (
    price_data["Price range"]
    .value_counts()
    .sort_index()
)

# ------------------------------------------------------------
# STEP 7: Calculate percentage
# ------------------------------------------------------------

total_restaurants = len(price_data)

price_percentages = (
    price_counts / total_restaurants
) * 100

# ------------------------------------------------------------
# STEP 8: Display results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PRICE RANGE DISTRIBUTION")
print("=" * 70)

for price_range, count in price_counts.items():

    percentage = price_percentages[price_range]

    print(f"\nPrice Range {price_range}")
    print(f"Number of Restaurants : {count}")
    print(f"Percentage            : {percentage:.2f}%")

# ------------------------------------------------------------
# STEP 9: Create summary DataFrame
# ------------------------------------------------------------

result = pd.DataFrame({
    "Price Range": price_counts.index,
    "Restaurant Count": price_counts.values,
    "Percentage": price_percentages.values
})

print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)

print(result.to_string(index=False))

# ------------------------------------------------------------
# STEP 10: Create output folder
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
# STEP 11: Save CSV result
# ------------------------------------------------------------

csv_path = os.path.join(
    OUTPUT_DIR,
    "price_range_distribution.csv"
)

result.to_csv(
    csv_path,
    index=False
)

print("\nCSV file created successfully!")
print(csv_path)

# ------------------------------------------------------------
# STEP 12: Create bar chart
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    result["Price Range"].astype(str),
    result["Restaurant Count"]
)

plt.xlabel("Price Range")
plt.ylabel("Number of Restaurants")

plt.title(
    "Distribution of Restaurants by Price Range"
)

plt.tight_layout()

# ------------------------------------------------------------
# STEP 13: Save chart
# ------------------------------------------------------------

chart_path = os.path.join(
    OUTPUT_DIR,
    "price_range_distribution.png"
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
print("TASK 3 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nFiles created inside the output folder:")
print("1. price_range_distribution.csv")
print("2. price_range_distribution.png")

print("\nYou can use these files in your internship submission/report.")