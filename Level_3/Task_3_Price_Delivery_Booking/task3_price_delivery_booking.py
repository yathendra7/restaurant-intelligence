import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# LEVEL 3 - TASK 3
# PRICE RANGE VS ONLINE DELIVERY AND TABLE BOOKING
# ============================================================

print("=" * 70)
print("LEVEL 3 - TASK 3: PRICE RANGE VS ONLINE DELIVERY AND TABLE BOOKING")
print("=" * 70)

# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

DATA_PATH = "data/Dataset.csv"

OUTPUT_DIR = "Level_3/Task_3_Price_Delivery_Booking/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# 2. LOAD DATASET
# ------------------------------------------------------------

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print("Total restaurants:", len(df))

# ------------------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

print("\nChecking required columns...")

required_columns = [
    "Price range",
    "Has Online delivery",
    "Has Table booking"
]

for column in required_columns:
    if column in df.columns:
        print("✓", column)
    else:
        print("✗ Missing:", column)

# ------------------------------------------------------------
# 4. SELECT REQUIRED DATA
# ------------------------------------------------------------

analysis_df = df[
    [
        "Price range",
        "Has Online delivery",
        "Has Table booking"
    ]
].copy()

analysis_df = analysis_df.dropna()

print("\nValid records for analysis:", len(analysis_df))

# ------------------------------------------------------------
# 5. ONLINE DELIVERY ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PRICE RANGE VS ONLINE DELIVERY")
print("=" * 70)

delivery_table = pd.crosstab(
    analysis_df["Price range"],
    analysis_df["Has Online delivery"]
)

print("\nRestaurant count:")
print(delivery_table)

delivery_percentage = pd.crosstab(
    analysis_df["Price range"],
    analysis_df["Has Online delivery"],
    normalize="index"
) * 100

print("\nOnline delivery percentage:")
print(delivery_percentage.round(2))

delivery_percentage.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "online_delivery_by_price_range.csv"
    )
)

print("\nSaved:")
print("online_delivery_by_price_range.csv")

# ------------------------------------------------------------
# 6. TABLE BOOKING ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PRICE RANGE VS TABLE BOOKING")
print("=" * 70)

booking_table = pd.crosstab(
    analysis_df["Price range"],
    analysis_df["Has Table booking"]
)

print("\nRestaurant count:")
print(booking_table)

booking_percentage = pd.crosstab(
    analysis_df["Price range"],
    analysis_df["Has Table booking"],
    normalize="index"
) * 100

print("\nTable booking percentage:")
print(booking_percentage.round(2))

booking_percentage.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "table_booking_by_price_range.csv"
    )
)

print("\nSaved:")
print("table_booking_by_price_range.csv")

# ------------------------------------------------------------
# 7. COMBINED SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("COMBINED PRICE RANGE SERVICE ANALYSIS")
print("=" * 70)

summary = []

for price_range in sorted(
    analysis_df["Price range"].unique()
):

    subset = analysis_df[
        analysis_df["Price range"] == price_range
    ]

    total = len(subset)

    online_yes = (
        subset["Has Online delivery"] == "Yes"
    ).sum()

    booking_yes = (
        subset["Has Table booking"] == "Yes"
    ).sum()

    online_percentage = (
        online_yes / total
    ) * 100

    booking_percentage_value = (
        booking_yes / total
    ) * 100

    summary.append({
        "Price Range": price_range,
        "Total Restaurants": total,
        "Online Delivery Restaurants": online_yes,
        "Online Delivery %": online_percentage,
        "Table Booking Restaurants": booking_yes,
        "Table Booking %": booking_percentage_value
    })

summary_df = pd.DataFrame(summary)

print("\nSummary:")
print(summary_df.to_string(index=False))

summary_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "price_range_service_summary.csv"
    ),
    index=False
)

print("\nSaved:")
print("price_range_service_summary.csv")

# ------------------------------------------------------------
# 8. CORRELATION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)

correlation_df = analysis_df.copy()

correlation_df["Online Delivery Binary"] = (
    correlation_df["Has Online delivery"]
    .map({
        "Yes": 1,
        "No": 0
    })
)

correlation_df["Table Booking Binary"] = (
    correlation_df["Has Table booking"]
    .map({
        "Yes": 1,
        "No": 0
    })
)

delivery_correlation = correlation_df[
    ["Price range", "Online Delivery Binary"]
].corr().iloc[0, 1]

booking_correlation = correlation_df[
    ["Price range", "Table Booking Binary"]
].corr().iloc[0, 1]

print(
    "\nPrice Range vs Online Delivery:",
    round(delivery_correlation, 4)
)

print(
    "Price Range vs Table Booking:",
    round(booking_correlation, 4)
)

correlation_results = pd.DataFrame({
    "Relationship": [
        "Price Range vs Online Delivery",
        "Price Range vs Table Booking"
    ],
    "Correlation": [
        delivery_correlation,
        booking_correlation
    ]
})

correlation_results.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "price_service_correlations.csv"
    ),
    index=False
)

print("\nSaved:")
print("price_service_correlations.csv")

# ------------------------------------------------------------
# 9. ONLINE DELIVERY CHART
# ------------------------------------------------------------

print("\nCreating online delivery chart...")

delivery_yes = delivery_percentage["Yes"]

plt.figure(figsize=(8, 5))

plt.bar(
    delivery_yes.index.astype(str),
    delivery_yes.values
)

plt.xlabel("Price Range")
plt.ylabel("Online Delivery (%)")
plt.title("Online Delivery Availability by Price Range")

plt.ylim(0, 100)

for i, value in enumerate(delivery_yes.values):

    plt.text(
        i,
        value + 2,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "online_delivery_by_price_range.png"
    ),
    dpi=300
)

plt.close()

print("Saved:")
print("online_delivery_by_price_range.png")

# ------------------------------------------------------------
# 10. TABLE BOOKING CHART
# ------------------------------------------------------------

print("\nCreating table booking chart...")

booking_yes = booking_percentage["Yes"]

plt.figure(figsize=(8, 5))

plt.bar(
    booking_yes.index.astype(str),
    booking_yes.values
)

plt.xlabel("Price Range")
plt.ylabel("Table Booking (%)")
plt.title("Table Booking Availability by Price Range")

plt.ylim(0, 100)

for i, value in enumerate(booking_yes.values):

    plt.text(
        i,
        value + 2,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "table_booking_by_price_range.png"
    ),
    dpi=300
)

plt.close()

print("Saved:")
print("table_booking_by_price_range.png")

# ------------------------------------------------------------
# 11. COMBINED CHART
# ------------------------------------------------------------

print("\nCreating combined service chart...")

x = range(len(summary_df))

width = 0.35

plt.figure(figsize=(9, 6))

plt.bar(
    [i - width / 2 for i in x],
    summary_df["Online Delivery %"],
    width=width,
    label="Online Delivery"
)

plt.bar(
    [i + width / 2 for i in x],
    summary_df["Table Booking %"],
    width=width,
    label="Table Booking"
)

plt.xticks(
    list(x),
    summary_df["Price Range"]
)

plt.xlabel("Price Range")
plt.ylabel("Availability (%)")

plt.title(
    "Online Delivery and Table Booking by Price Range"
)

plt.ylim(0, 100)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "price_range_service_comparison.png"
    ),
    dpi=300
)

plt.close()

print("Saved:")
print("price_range_service_comparison.png")

# ------------------------------------------------------------
# 12. FINAL FINDINGS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TASK 3 SUMMARY")
print("=" * 70)

highest_delivery = summary_df.loc[
    summary_df["Online Delivery %"].idxmax()
]

highest_booking = summary_df.loc[
    summary_df["Table Booking %"].idxmax()
]

print(
    "\nPrice range with highest online delivery:",
    highest_delivery["Price Range"]
)

print(
    "Online delivery percentage:",
    round(highest_delivery["Online Delivery %"], 2),
    "%"
)

print(
    "\nPrice range with highest table booking:",
    highest_booking["Price Range"]
)

print(
    "Table booking percentage:",
    round(highest_booking["Table Booking %"], 2),
    "%"
)

print(
    "\nPrice Range vs Online Delivery correlation:",
    round(delivery_correlation, 4)
)

print(
    "Price Range vs Table Booking correlation:",
    round(booking_correlation, 4)
)

# ------------------------------------------------------------
# 13. COMPLETION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TASK 3 COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated files:")

print("1. online_delivery_by_price_range.csv")
print("2. table_booking_by_price_range.csv")
print("3. price_range_service_summary.csv")
print("4. price_service_correlations.csv")
print("5. online_delivery_by_price_range.png")
print("6. table_booking_by_price_range.png")
print("7. price_range_service_comparison.png")