import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# LEVEL 2 - TASK 3: GEOGRAPHIC ANALYSIS
# ============================================================

# File paths
input_file = r"data\Dataset.csv"
output_folder = r"Level_2\Task_3_Geographic_Analysis\output"

# Create output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 60)
print("LEVEL 2 - TASK 3: GEOGRAPHIC ANALYSIS")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(input_file)

print(f"Dataset loaded successfully.")
print(f"Total restaurants: {len(df)}")

# ============================================================
# 2. CLEAN LATITUDE AND LONGITUDE
# ============================================================

print("\nCleaning geographic data...")

df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

geo_df = df.dropna(subset=["Latitude", "Longitude"]).copy()

print(f"Restaurants with valid coordinates: {len(geo_df)}")
print(f"Restaurants without valid coordinates: {len(df) - len(geo_df)}")

# ============================================================
# 3. SAVE CLEAN GEOGRAPHIC DATA
# ============================================================

geo_output = os.path.join(
    output_folder,
    "restaurant_geographic_data.csv"
)

geo_df[
    [
        "Restaurant ID",
        "Restaurant Name",
        "City",
        "Locality",
        "Latitude",
        "Longitude",
        "Aggregate rating"
    ]
].to_csv(geo_output, index=False)

print(f"\nGeographic data saved to:")
print(geo_output)

# ============================================================
# 4. GEOGRAPHIC MAP
# ============================================================

print("\nCreating geographic restaurant map...")

plt.figure(figsize=(12, 8))

plt.scatter(
    geo_df["Longitude"],
    geo_df["Latitude"],
    s=8,
    alpha=0.4
)

plt.title(
    "Geographic Distribution of Restaurants",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.grid(True, alpha=0.3)

plt.tight_layout()

map_output = os.path.join(
    output_folder,
    "restaurant_geographic_map.png"
)

plt.savefig(map_output, dpi=300)
plt.close()

print(f"Geographic map saved to:")
print(map_output)

# ============================================================
# 5. CITY-BASED CLUSTER ANALYSIS
# ============================================================

print("\nAnalyzing restaurant clusters by city...")

city_counts = (
    geo_df
    .groupby("City")
    .size()
    .reset_index(name="Restaurant Count")
    .sort_values("Restaurant Count", ascending=False)
)

city_output = os.path.join(
    output_folder,
    "city_geographic_clusters.csv"
)

city_counts.to_csv(city_output, index=False)

print("\nTop 15 cities by number of geographically mapped restaurants:")

print(
    city_counts.head(15).to_string(index=False)
)

print(f"\nCity cluster analysis saved to:")
print(city_output)

# ============================================================
# 6. TOP CITY CLUSTER CHART
# ============================================================

print("\nCreating city cluster chart...")

top_cities = city_counts.head(15).sort_values(
    "Restaurant Count",
    ascending=True
)

plt.figure(figsize=(12, 8))

plt.barh(
    top_cities["City"],
    top_cities["Restaurant Count"]
)

plt.title(
    "Top 15 Cities by Number of Restaurants",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Restaurants")
plt.ylabel("City")

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()

cluster_output = os.path.join(
    output_folder,
    "top_city_geographic_clusters.png"
)

plt.savefig(cluster_output, dpi=300)
plt.close()

print(f"City cluster chart saved to:")
print(cluster_output)

# ============================================================
# 7. GEOGRAPHIC SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("GEOGRAPHIC ANALYSIS SUMMARY")
print("=" * 60)

print(f"\nTotal restaurants: {len(df)}")
print(f"Valid geographic records: {len(geo_df)}")

print(
    f"Latitude range: "
    f"{geo_df['Latitude'].min():.4f} to "
    f"{geo_df['Latitude'].max():.4f}"
)

print(
    f"Longitude range: "
    f"{geo_df['Longitude'].min():.4f} to "
    f"{geo_df['Longitude'].max():.4f}"
)

print("\nTop 5 geographic clusters by city:")

print(
    city_counts.head(5).to_string(index=False)
)

print("\n" + "=" * 60)
print("TASK 3 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nGenerated files:")

print("1. restaurant_geographic_data.csv")
print("2. restaurant_geographic_map.png")
print("3. city_geographic_clusters.csv")
print("4. top_city_geographic_clusters.png")