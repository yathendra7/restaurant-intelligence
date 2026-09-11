from pathlib import Path
import io

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "Dataset.csv"


# ============================================================
# RESTAURANT / FOOD IMAGES
# ============================================================

HERO_IMAGE = (
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
    "?auto=format&fit=crop&w=1800&q=85"
)

FOOD_IMAGES = [
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
    "?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1552566626-52f8b828add9"
    "?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f"
    "?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1547592180-85f173990554"
    "?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1513104890138-7c749659a591"
    "?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"
    "?auto=format&fit=crop&w=900&q=80",
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None

    df = pd.read_csv(DATA_FILE)

    # Clean column names
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # Convert numeric columns where available
    numeric_columns = [
        "Aggregate rating",
        "Votes",
        "Price range",
        "Average Cost for two",
        "Longitude",
        "Latitude",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


df = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_col(possible_names):
    """Find a column using exact or partial matching."""

    if df is None:
        return None

    # Exact match
    for name in possible_names:
        if name in df.columns:
            return name

    # Case-insensitive exact match
    lower_columns = {
        str(column).lower(): column
        for column in df.columns
    }

    for name in possible_names:
        if str(name).lower() in lower_columns:
            return lower_columns[str(name).lower()]

    # Partial match
    for column in df.columns:
        column_lower = str(column).lower()

        for name in possible_names:
            if str(name).lower() in column_lower:
                return column

    return None


def clean_text(series):
    return (
        series
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )


def format_number(value):
    if pd.isna(value):
        return "0"

    value = float(value)

    if value.is_integer():
        return f"{int(value):,}"

    return f"{value:,.2f}"


def format_currency(value):
    if pd.isna(value):
        return "₹0"

    return f"₹{float(value):,.0f}"


def prepare_chart(fig, height=430):
    fig.update_layout(
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#EDEDED"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),
    )

    return fig


def download_csv(dataframe, filename, label):
    csv_data = dataframe.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )


def show_table(dataframe, key):
    if dataframe.empty:
        st.info("No data available.")
        return

    show_data = st.checkbox(
        "Show data table",
        key=key
    )

    if show_data:
        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )

        download_csv(
            dataframe,
            "restaurant_analysis.csv",
            "Download CSV"
        )


# ============================================================
# CHECK DATASET
# ============================================================

if df is None:

    st.error(
        "Dataset.csv was not found."
    )

    st.write(
        "Make sure your project has this structure:"
    )

    st.code(
        """
Cognifyz-Data-Analysis-Internship
│
├── Dashboard
│   └── app.py
│
└── data
    └── Dataset.csv
        """
    )

    st.stop()


# ============================================================
# IDENTIFY IMPORTANT COLUMNS
# ============================================================

COL_RESTAURANT = find_col(
    ["Restaurant Name", "restaurant name"]
)

COL_CITY = find_col(
    ["City", "city"]
)

COL_CUISINE = find_col(
    ["Cuisines", "Cuisine", "cuisines"]
)

COL_RATING = find_col(
    ["Aggregate rating", "Rating", "aggregate rating"]
)

COL_VOTES = find_col(
    ["Votes", "votes"]
)

COL_PRICE = find_col(
    ["Price range", "Price Range", "price range"]
)

COL_COST = find_col(
    ["Average Cost for two", "Average cost for two"]
)

COL_BOOKING = find_col(
    ["Has Table booking", "Table booking"]
)

COL_DELIVERY = find_col(
    ["Has Online delivery", "Online delivery"]
)

COL_LATITUDE = find_col(
    ["Latitude", "latitude"]
)

COL_LONGITUDE = find_col(
    ["Longitude", "longitude"]
)

COL_RATING_TEXT = find_col(
    ["Rating text", "rating text"]
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🍽️ Restaurant")
    st.caption("Intelligence Platform")

    st.divider()

    page = st.radio(
        "Explore",
        [
            "Home",
            "Cuisine Intelligence",
            "City Intelligence",
            "Price Intelligence",
            "Rating Intelligence",
            "Geographic Intelligence",
            "Restaurant Chains",
            "Feedback Intelligence",
            "Votes Intelligence",
            "Service & Booking",
        ]
    )

    st.divider()

    st.caption("Dataset")

    st.metric(
        "Restaurants",
        f"{len(df):,}"
    )

    st.caption(
        "Powered by Streamlit + Plotly"
    )


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.image(
        HERO_IMAGE,
        use_container_width=True
    )

    st.title(
        "Discover the Restaurant Market"
    )

    st.write(
        "A data-driven restaurant intelligence platform "
        "for understanding cuisines, cities, pricing, ratings, "
        "customer engagement and restaurant services."
    )

    st.divider()

    # KPI SECTION

    total_restaurants = len(df)

    if COL_CITY:
        total_cities = df[COL_CITY].nunique()
    else:
        total_cities = 0

    if COL_CUISINE:
        total_cuisines = (
            df[COL_CUISINE]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
            .nunique()
        )
    else:
        total_cuisines = 0

    if COL_RATING:
        average_rating = df[COL_RATING].mean()
    else:
        average_rating = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Restaurants",
            format_number(total_restaurants)
        )

    with col2:
        st.metric(
            "Cities",
            format_number(total_cities)
        )

    with col3:
        st.metric(
            "Cuisine Types",
            format_number(total_cuisines)
        )

    with col4:
        st.metric(
            "Average Rating",
            f"{average_rating:.2f}"
        )

    st.divider()

    # FEATURED RESTAURANT VISUALS

    st.subheader("A taste of the restaurant landscape")

    image_columns = st.columns(3)

    titles = [
        "Dining experiences",
        "Popular cuisines",
        "Restaurant discovery",
    ]

    descriptions = [
        "Explore the characteristics of restaurants across the dataset.",
        "Understand which cuisines dominate the market.",
        "Compare restaurants, cities, prices and customer engagement.",
    ]

    for index in range(3):

        with image_columns[index]:

            st.image(
                FOOD_IMAGES[index],
                use_container_width=True
            )

            st.subheader(
                titles[index]
            )

            st.write(
                descriptions[index]
            )

    st.divider()

    # TOP RESTAURANTS

    st.subheader("Top-rated restaurants")

    if COL_RESTAURANT and COL_RATING:

        top_restaurants = (
            df[
                [
                    COL_RESTAURANT,
                    COL_RATING
                ]
            ]
            .dropna()
            .sort_values(
                COL_RATING,
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_restaurants,
            use_container_width=True,
            hide_index=True
        )

    st.info(
        "Use the sections in the sidebar to explore the complete "
        "restaurant intelligence analysis."
    )


# ============================================================
# CUISINE INTELLIGENCE
# ============================================================

elif page == "Cuisine Intelligence":

    st.title("Cuisine Intelligence")

    st.write(
        "Discover the most common cuisines and understand "
        "their restaurant presence and ratings."
    )

    if COL_CUISINE:

        cuisine_data = (
            df[COL_CUISINE]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
        )

        cuisine_counts = (
            cuisine_data
            .value_counts()
            .head(15)
            .reset_index()
        )

        cuisine_counts.columns = [
            "Cuisine",
            "Restaurants"
        ]

        fig = px.bar(
            cuisine_counts,
            x="Restaurants",
            y="Cuisine",
            orientation="h",
            title="Most Popular Cuisines",
        )

        fig.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        st.subheader("Cuisine snapshot")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                FOOD_IMAGES[3],
                use_container_width=True
            )

        with col2:
            st.image(
                FOOD_IMAGES[4],
                use_container_width=True
            )

        with col3:
            st.image(
                FOOD_IMAGES[5],
                use_container_width=True
            )

        show_table(
            cuisine_counts,
            "show_cuisine_table"
        )

    else:
        st.warning(
            "Cuisine column was not found."
        )


# ============================================================
# CITY INTELLIGENCE
# ============================================================

elif page == "City Intelligence":

    st.title("City Intelligence")

    st.write(
        "Compare restaurant concentration and market presence "
        "across cities."
    )

    if COL_CITY:

        city_counts = (
            df[COL_CITY]
            .fillna("Unknown")
            .value_counts()
            .head(15)
            .reset_index()
        )

        city_counts.columns = [
            "City",
            "Restaurants"
        ]

        fig = px.bar(
            city_counts,
            x="City",
            y="Restaurants",
            title="Restaurant Presence by City",
        )

        fig.update_xaxes(
            tickangle=-45
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        if COL_RATING:

            city_rating = (
                df.groupby(COL_CITY)[COL_RATING]
                .mean()
                .sort_values(
                    ascending=False
                )
                .head(15)
                .reset_index()
            )

            city_rating.columns = [
                "City",
                "Average Rating"
            ]

            fig2 = px.bar(
                city_rating,
                x="City",
                y="Average Rating",
                title="Highest Rated Cities",
            )

            fig2.update_xaxes(
                tickangle=-45
            )

            st.plotly_chart(
                prepare_chart(fig2),
                use_container_width=True
            )

        show_table(
            city_counts,
            "show_city_table"
        )

    else:
        st.warning(
            "City column was not found."
        )


# ============================================================
# PRICE INTELLIGENCE
# ============================================================

elif page == "Price Intelligence":

    st.title("Price Intelligence")

    st.write(
        "Understand how restaurants are distributed across "
        "different price ranges."
    )

    if COL_PRICE:

        price_counts = (
            df[COL_PRICE]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )

        price_counts.columns = [
            "Price Range",
            "Restaurants"
        ]

        fig = px.bar(
            price_counts,
            x="Price Range",
            y="Restaurants",
            title="Restaurants by Price Range",
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                FOOD_IMAGES[0],
                use_container_width=True
            )

            st.subheader(
                "Affordable dining"
            )

            st.write(
                "Explore restaurants positioned toward "
                "lower price categories."
            )

        with col2:

            st.image(
                FOOD_IMAGES[1],
                use_container_width=True
            )

            st.subheader(
                "Premium dining"
            )

            st.write(
                "Identify restaurants operating in higher "
                "price categories."
            )

        if COL_COST:

            average_cost = df[COL_COST].mean()

            st.metric(
                "Average Cost for Two",
                format_currency(average_cost)
            )

        show_table(
            price_counts,
            "show_price_table"
        )

    else:
        st.warning(
            "Price range column was not found."
        )


# ============================================================
# RATING INTELLIGENCE
# ============================================================

elif page == "Rating Intelligence":

    st.title("Rating Intelligence")

    st.write(
        "Analyze restaurant ratings and understand "
        "customer satisfaction patterns."
    )

    if COL_RATING:

        rating_data = (
            df[COL_RATING]
            .dropna()
        )

        fig = px.histogram(
            rating_data,
            x=COL_RATING,
            nbins=20,
            title="Restaurant Rating Distribution",
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Rating",
                f"{rating_data.mean():.2f}"
            )

        with col2:
            st.metric(
                "Highest Rating",
                f"{rating_data.max():.2f}"
            )

        with col3:
            st.metric(
                "Lowest Rating",
                f"{rating_data.min():.2f}"
            )

        if COL_RATING_TEXT:

            rating_text = (
                df[COL_RATING_TEXT]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )

            rating_text.columns = [
                "Rating Category",
                "Restaurants"
            ]

            fig2 = px.pie(
                rating_text,
                names="Rating Category",
                values="Restaurants",
                title="Rating Categories",
            )

            st.plotly_chart(
                prepare_chart(fig2),
                use_container_width=True
            )

            show_table(
                rating_text,
                "show_rating_table"
            )

    else:
        st.warning(
            "Rating column was not found."
        )


# ============================================================
# GEOGRAPHIC INTELLIGENCE
# ============================================================

elif page == "Geographic Intelligence":

    st.title("Geographic Intelligence")

    st.write(
        "Visualize the geographic distribution of restaurants."
    )

    if (
        COL_LATITUDE
        and COL_LONGITUDE
    ):

        map_data = df[
            [
                COL_LATITUDE,
                COL_LONGITUDE
            ]
        ].copy()

        map_data[COL_LATITUDE] = pd.to_numeric(
            map_data[COL_LATITUDE],
            errors="coerce"
        )

        map_data[COL_LONGITUDE] = pd.to_numeric(
            map_data[COL_LONGITUDE],
            errors="coerce"
        )

        map_data = map_data.dropna()

        map_data = map_data.rename(
            columns={
                COL_LATITUDE: "latitude",
                COL_LONGITUDE: "longitude",
            }
        )

        st.map(
            map_data,
            latitude="latitude",
            longitude="longitude",
            size=10,
        )

        st.metric(
            "Mapped Restaurants",
            format_number(len(map_data))
        )

    else:
        st.warning(
            "Latitude and Longitude columns were not found."
        )


# ============================================================
# RESTAURANT CHAINS
# ============================================================

elif page == "Restaurant Chains":

    st.title("Restaurant Chains")

    st.write(
        "Identify restaurant brands with multiple locations "
        "across the dataset."
    )

    if COL_RESTAURANT:

        chain_counts = (
            df[COL_RESTAURANT]
            .fillna("Unknown")
            .value_counts()
            .head(20)
            .reset_index()
        )

        chain_counts.columns = [
            "Restaurant",
            "Locations"
        ]

        fig = px.bar(
            chain_counts,
            x="Locations",
            y="Restaurant",
            orientation="h",
            title="Restaurants with the Most Locations",
        )

        fig.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        show_table(
            chain_counts,
            "show_chain_table"
        )

    else:
        st.warning(
            "Restaurant Name column was not found."
        )


# ============================================================
# FEEDBACK INTELLIGENCE
# ============================================================

elif page == "Feedback Intelligence":

    st.title("Feedback Intelligence")

    st.write(
        "Understand customer feedback through ratings "
        "and review-related indicators."
    )

    if COL_RATING and COL_VOTES:

        feedback_data = df[
            [
                COL_RATING,
                COL_VOTES
            ]
        ].dropna()

        fig = px.scatter(
            feedback_data,
            x=COL_RATING,
            y=COL_VOTES,
            title="Ratings vs Customer Votes",
            opacity=0.65,
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        correlation = feedback_data[
            COL_RATING
        ].corr(
            feedback_data[COL_VOTES]
        )

        st.metric(
            "Rating / Vote Correlation",
            f"{correlation:.3f}"
        )

        st.info(
            "A higher number of votes indicates stronger "
            "customer engagement with the restaurant."
        )

    else:
        st.warning(
            "Rating or Votes column was not found."
        )


# ============================================================
# VOTES INTELLIGENCE
# ============================================================

elif page == "Votes Intelligence":

    st.title("Votes Intelligence")

    st.write(
        "Find restaurants receiving the strongest "
        "customer engagement."
    )

    if COL_VOTES:

        vote_data = df[
            [
                c for c in [
                    COL_RESTAURANT,
                    COL_CITY,
                    COL_RATING,
                    COL_VOTES
                ]
                if c is not None
            ]
        ].copy()

        vote_data = vote_data.dropna(
            subset=[COL_VOTES]
        )

        top_votes = (
            vote_data
            .sort_values(
                COL_VOTES,
                ascending=False
            )
            .head(20)
        )

        fig = px.bar(
            top_votes.head(15),
            x=COL_VOTES,
            y=COL_RESTAURANT
            if COL_RESTAURANT
            else COL_VOTES,
            orientation="h",
            title="Most Voted Restaurants",
        )

        fig.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            prepare_chart(fig),
            use_container_width=True
        )

        st.metric(
            "Total Votes",
            format_number(
                df[COL_VOTES].sum()
            )
        )

        show_table(
            top_votes,
            "show_votes_table"
        )

    else:
        st.warning(
            "Votes column was not found."
        )


# ============================================================
# SERVICE & BOOKING
# ============================================================

elif page == "Service & Booking":

    st.title("Service & Booking")

    st.write(
        "Explore table booking and online delivery adoption "
        "across restaurants."
    )

    service_columns = []

    if COL_BOOKING:
        service_columns.append(COL_BOOKING)

    if COL_DELIVERY:
        service_columns.append(COL_DELIVERY)

    if not service_columns:

        st.warning(
            "Booking or delivery columns were not found."
        )

    else:

        for column in service_columns:

            service_counts = (
                df[column]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            service_counts.columns = [
                "Service",
                "Restaurants"
            ]

            st.subheader(
                column
            )

            fig = px.pie(
                service_counts,
                names="Service",
                values="Restaurants",
                title=f"{column} Distribution",
            )

            st.plotly_chart(
                prepare_chart(fig),
                use_container_width=True
            )

            show_table(
                service_counts,
                f"show_{column}_table"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                FOOD_IMAGES[2],
                use_container_width=True
            )

            st.subheader(
                "Table booking"
            )

            st.write(
                "Understand how restaurants support "
                "advance table reservations."
            )

        with col2:

            st.image(
                FOOD_IMAGES[3],
                use_container_width=True
            )

            st.subheader(
                "Online delivery"
            )

            st.write(
                "Explore the adoption of online delivery "
                "services."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Restaurant Intelligence • Cognifyz Data Analysis Internship"
)