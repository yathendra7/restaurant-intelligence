import pandas as pd

# Load the dataset
df = pd.read_csv("data/Dataset.csv")

# Display first 5 rows
print(df.head())

# Display dataset shape
print("\nDataset Shape:")
print(df.shape)

# Display column names
print("\nColumn Names:")
print(df.columns.tolist())
# ==========================================
# TASK 1: TOP CUISINES
# ==========================================

# Remove rows where cuisine information is missing
cuisine_data = df.dropna(subset=["Cuisines"]).copy()

# Count each cuisine
cuisine_counts = cuisine_data["Cuisines"].value_counts()

# Get top 3 cuisines
top_3_cuisines = cuisine_counts.head(3)

# Calculate percentage
total_restaurants = len(cuisine_data)

top_3_percentage = (top_3_cuisines / total_restaurants) * 100

# Display results
print("\n" + "=" * 50)
print("TOP 3 CUISINES")
print("=" * 50)

for cuisine, count in top_3_cuisines.items():
    percentage = top_3_percentage[cuisine]

    print(f"{cuisine}:")
    print(f"  Number of Restaurants: {count}")
    print(f"  Percentage: {percentage:.2f}%")
    print()

# Display as a table
result = pd.DataFrame({
    "Cuisine": top_3_cuisines.index,
    "Restaurant Count": top_3_cuisines.values,
    "Percentage": top_3_percentage.values
})

print("Top 3 Cuisines Summary:")
print(result.to_string(index=False))