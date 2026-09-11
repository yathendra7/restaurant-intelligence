import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# LEVEL 3 - TASK 1: RESTAURANT REVIEWS
# ============================================================

input_file = r"data\Dataset.csv"
output_folder = r"Level_3\Task_1_Restaurant_Reviews\output"

os.makedirs(output_folder, exist_ok=True)

print("=" * 65)
print("LEVEL 3 - TASK 1: RESTAURANT REVIEWS")
print("=" * 65)

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(input_file)

print(f"Dataset loaded successfully.")
print(f"Total restaurants: {len(df)}")

# ============================================================
# 2. CHECK AVAILABLE REVIEW-RELATED COLUMNS
# ============================================================

print("\nChecking review-related information...")

review_columns = [
    column for column in df.columns
    if any(word in column.lower()
           for word in ["review", "comment", "feedback"])
]

if review_columns:
    print("Review-related columns found:")
    print(review_columns)
else:
    print("No actual written review/comment column found.")

print("\nAvailable rating feedback column: Rating text")

# ============================================================
# 3. RATING TEXT DISTRIBUTION
# ============================================================

print("\nAnalyzing Rating text distribution...")

rating_text_counts = (
    df["Rating text"]
    .value_counts()
    .reset_index()
)

rating_text_counts.columns = [
    "Rating Text",
    "Restaurant Count"
]

rating_text_counts["Percentage"] = (
    rating_text_counts["Restaurant Count"]
    / len(df)
    * 100
).round(2)

print("\nRating text distribution:")

print(
    rating_text_counts.to_string(index=False)
)

rating_text_output = os.path.join(
    output_folder,
    "rating_text_distribution.csv"
)

rating_text_counts.to_csv(
    rating_text_output,
    index=False
)

print("\nSaved:")
print(rating_text_output)

# ============================================================
# 4. RATING TEXT VS AVERAGE RATING
# ============================================================

print("\nAnalyzing rating text versus aggregate rating...")

rating_analysis = (
    df.groupby("Rating text")
    .agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean"),
        Average_Votes=("Votes", "mean"),
        Total_Votes=("Votes", "sum")
    )
    .reset_index()
)

rating_analysis["Average_Rating"] = (
    rating_analysis["Average_Rating"]
    .round(2)
)

rating_analysis["Average_Votes"] = (
    rating_analysis["Average_Votes"]
    .round(2)
)

print("\nRating text analysis:")

print(
    rating_analysis.to_string(index=False)
)

rating_analysis_output = os.path.join(
    output_folder,
    "rating_text_analysis.csv"
)

rating_analysis.to_csv(
    rating_analysis_output,
    index=False
)

print("\nSaved:")
print(rating_analysis_output)

# ============================================================
# 5. POSITIVE / NEGATIVE CATEGORY ANALYSIS
# ============================================================

print("\nClassifying rating feedback...")

positive_categories = [
    "Excellent",
    "Very Good",
    "Good"
]

negative_categories = [
    "Average",
    "Poor"
]

def classify_rating(text):

    if text in positive_categories:
        return "Positive"

    elif text in negative_categories:
        return "Negative"

    else:
        return "Not Rated"


df["Feedback Category"] = (
    df["Rating text"]
    .apply(classify_rating)
)

feedback_counts = (
    df["Feedback Category"]
    .value_counts()
    .reset_index()
)

feedback_counts.columns = [
    "Feedback Category",
    "Restaurant Count"
]

feedback_counts["Percentage"] = (
    feedback_counts["Restaurant Count"]
    / len(df)
    * 100
).round(2)

print("\nPositive / Negative feedback distribution:")

print(
    feedback_counts.to_string(index=False)
)

feedback_output = os.path.join(
    output_folder,
    "positive_negative_feedback_analysis.csv"
)

feedback_counts.to_csv(
    feedback_output,
    index=False
)

print("\nSaved:")
print(feedback_output)

# ============================================================
# 6. POSITIVE / NEGATIVE FEEDBACK VS RATINGS
# ============================================================

feedback_rating_analysis = (
    df.groupby("Feedback Category")
    .agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Average_Rating=("Aggregate rating", "mean"),
        Average_Votes=("Votes", "mean")
    )
    .reset_index()
)

feedback_rating_analysis["Average_Rating"] = (
    feedback_rating_analysis["Average_Rating"]
    .round(2)
)

feedback_rating_analysis["Average_Votes"] = (
    feedback_rating_analysis["Average_Votes"]
    .round(2)
)

print("\nFeedback category versus rating:")

print(
    feedback_rating_analysis.to_string(index=False)
)

feedback_rating_output = os.path.join(
    output_folder,
    "feedback_category_rating_analysis.csv"
)

feedback_rating_analysis.to_csv(
    feedback_rating_output,
    index=False
)

print("\nSaved:")
print(feedback_rating_output)

# ============================================================
# 7. CHART - RATING TEXT DISTRIBUTION
# ============================================================

print("\nCreating Rating text distribution chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    rating_text_counts["Rating Text"],
    rating_text_counts["Restaurant Count"]
)

plt.title(
    "Distribution of Restaurant Rating Feedback",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Rating Text")
plt.ylabel("Number of Restaurants")

plt.xticks(rotation=30)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

rating_chart = os.path.join(
    output_folder,
    "rating_text_distribution.png"
)

plt.savefig(
    rating_chart,
    dpi=300
)

plt.close()

print("Saved:")
print(rating_chart)

# ============================================================
# 8. CHART - POSITIVE VS NEGATIVE
# ============================================================

print("\nCreating positive versus negative feedback chart...")

chart_data = feedback_counts[
    feedback_counts["Feedback Category"] != "Not Rated"
].copy()

plt.figure(figsize=(8, 6))

plt.bar(
    chart_data["Feedback Category"],
    chart_data["Restaurant Count"]
)

plt.title(
    "Positive vs Negative Restaurant Feedback",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Feedback Category")
plt.ylabel("Number of Restaurants")

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

feedback_chart = os.path.join(
    output_folder,
    "positive_negative_feedback.png"
)

plt.savefig(
    feedback_chart,
    dpi=300
)

plt.close()

print("Saved:")
print(feedback_chart)

# ============================================================
# 9. LIMITATION INFORMATION
# ============================================================

limitation_file = os.path.join(
    output_folder,
    "review_analysis_limitation.txt"
)

with open(limitation_file, "w", encoding="utf-8") as file:

    file.write(
        "RESTAURANT REVIEW ANALYSIS - DATASET LIMITATION\n"
    )

    file.write("=" * 60 + "\n\n")

    file.write(
        "The provided dataset does not contain actual written "
        "restaurant review or comment text.\n\n"
    )

    file.write(
        "Therefore, keyword-frequency analysis and average "
        "review-length analysis cannot be performed directly.\n\n"
    )

    file.write(
        "The available 'Rating text' column was used as the "
        "available textual feedback classification.\n\n"
    )

    file.write(
        "Positive categories used: Excellent, Very Good, Good.\n"
    )

    file.write(
        "Negative categories used: Average, Poor.\n"
    )

print("\nDataset limitation documented in:")
print(limitation_file)

# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("RESTAURANT REVIEW ANALYSIS SUMMARY")
print("=" * 65)

print("\nMost common rating feedback:")

most_common = rating_text_counts.iloc[0]

print(
    f"{most_common['Rating Text']} "
    f"({int(most_common['Restaurant Count'])} restaurants, "
    f"{most_common['Percentage']:.2f}%)"
)

print("\nFeedback category summary:")

print(
    feedback_counts.to_string(index=False)
)

print("\nIMPORTANT DATASET LIMITATION:")
print(
    "Actual written review text is not available in the dataset."
)

print(
    "Therefore, review keyword and review-length analysis "
    "cannot be performed."
)

print("\n" + "=" * 65)
print("TASK 1 COMPLETED SUCCESSFULLY")
print("=" * 65)

print("\nGenerated files:")

print("1. rating_text_distribution.csv")
print("2. rating_text_analysis.csv")
print("3. positive_negative_feedback_analysis.csv")
print("4. feedback_category_rating_analysis.csv")
print("5. rating_text_distribution.png")
print("6. positive_negative_feedback.png")
print("7. review_analysis_limitation.txt")