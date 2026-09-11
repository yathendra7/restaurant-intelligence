
from pathlib import Path
import io

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "Dataset.csv"

OUTPUT_DIRS = {
    "price": BASE_DIR / "Level_1" / "Task_3_Price_Range_Distribution" / "output",
    "delivery": BASE_DIR / "Level_1" / "Task_4_Online_Delivery" / "output",
    "ratings": BASE_DIR / "Level_2" / "Task_1_Restaurant_Ratings" / "output",
    "cuisine_combo": BASE_DIR / "Level_2" / "Task_2_Cuisine_Combination" / "output",
    "geographic": BASE_DIR / "Level_2" / "Task_3_Geographic_Analysis" / "output",
    "chains": BASE_DIR / "Level_2" / "Task_4_Restaurant_Chains" / "output",
    "reviews": BASE_DIR / "Level_3" / "Task_1_Restaurant_Reviews" / "output",
    "votes": BASE_DIR / "Level_3" / "Task_2_Votes_Analysis" / "output",
    "services": BASE_DIR / "Level_3" / "Task_3_Price_Delivery_Booking" / "output",
}


# ============================================================
# PREMIUM STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ---------------- GLOBAL ---------------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 5%, rgba(255,255,255,0.045), transparent 25%),
            radial-gradient(circle at 85% 15%, rgba(255,255,255,0.035), transparent 25%),
            #0b0b0b;
        color: #f5f5f0;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: #101010;
        border-right: 1px solid #252525;
    }

    /* ---------------- NAV ---------------- */

    .nav-logo {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .nav-small {
        color: #858585;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* ---------------- HERO ---------------- */

    .hero-label {
        color: #999999;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-top: 2rem;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: clamp(3.5rem, 8vw, 7.8rem);
        line-height: 0.88;
        letter-spacing: -0.075em;
        font-weight: 700;
        margin: 0;
        color: #f7f7f2;
    }

    .hero-title-accent {
        color: #8e8e87;
    }

    .hero-text {
        max-width: 650px;
        margin-top: 1.8rem;
        color: #a6a6a0;
        font-size: 1.08rem;
        line-height: 1.7;
    }

    .hero-tag {
        display: inline-block;
        margin-top: 1.6rem;
        padding: 0.55rem 0.9rem;
        border: 1px solid #303030;
        border-radius: 100px;
        color: #d2d2cc;
        font-size: 0.78rem;
        background: #111111;
    }

    /* ---------------- SECTION ---------------- */

    .section-kicker {
        color: #888880;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .section-title {
        font-size: clamp(2rem, 4vw, 4.4rem);
        line-height: 0.98;
        letter-spacing: -0.055em;
        font-weight: 650;
        color: #f3f3ee;
        margin-bottom: 0.8rem;
    }

    .section-description {
        color: #96968f;
        max-width: 700px;
        line-height: 1.65;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* ---------------- CARDS ---------------- */

    .intel-card {
        background: #111111;
        border: 1px solid #292929;
        border-radius: 22px;
        padding: 1.55rem;
        min-height: 150px;
        transition: 0.2s ease;
    }

    .intel-card:hover {
        border-color: #4a4a4a;
        transform: translateY(-2px);
    }

    .intel-number {
        font-size: 2.25rem;
        line-height: 1;
        font-weight: 650;
        letter-spacing: -0.055em;
        color: #f4f4ef;
    }

    .intel-label {
        color: #8d8d87;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 0.7rem;
    }

    .feature-card {
        background: #111111;
        border: 1px solid #282828;
        border-radius: 25px;
        padding: 1.45rem;
        min-height: 100%;
    }

    .feature-number {
        color: #696963;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
        font-weight: 700;
    }

    .feature-title {
        color: #f1f1ec;
        font-size: 1.45rem;
        font-weight: 650;
        letter-spacing: -0.035em;
        margin-top: 0.7rem;
    }

    .feature-description {
        color: #898983;
        line-height: 1.55;
        margin-top: 0.5rem;
        font-size: 0.88rem;
    }

    /* ---------------- VISUAL PANEL ---------------- */

    .visual-panel {
        background: #101010;
        border: 1px solid #292929;
        border-radius: 28px;
        padding: 1.1rem;
    }

    .visual-label {
        color: #81817b;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        padding: 0.4rem 0.5rem 0.7rem;
    }

    /* ---------------- INSIGHT ---------------- */

    .insight-box {
        background: #151515;
        border: 1px solid #303030;
        border-radius: 20px;
        padding: 1.25rem 1.4rem;
        margin-top: 1rem;
    }

    .insight-label {
        color: #777771;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-size: 0.68rem;
        font-weight: 700;
    }

    .insight-text {
        color: #d4d4ce;
        margin-top: 0.5rem;
        line-height: 1.5;
    }

    /* ---------------- BUTTONS ---------------- */

    div.stButton > button {
        border-radius: 100px;
        border: 1px solid #333333;
        background: #151515;
        color: #e6e6df;
        min-height: 2.2rem;
        font-size: 0.76rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        border-color: #777777;
        background: #202020;
        color: white;
    }

    div.stDownloadButton > button {
        border-radius: 100px;
        border: 1px solid #333333;
        background: #e8e8e1;
        color: #111111;
        min-height: 2.2rem;
        font-size: 0.76rem;
        font-weight: 700;
    }

    /* ---------------- DATAFRAME ---------------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #292929;
        border-radius: 15px;
        overflow: hidden;
    }

    /* ---------------- DIVIDER ---------------- */

    .soft-divider {
        height: 1px;
        background: #242424;
        margin: 5rem 0;
    }

    /* ---------------- FOOTER ---------------- */

    .footer {
        border-top: 1px solid #252525;
        padding-top: 2rem;
        margin-top: 5rem;
        color: #666660;
        font-size: 0.75rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None

    df = pd.read_csv(DATA_FILE)

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    # Numeric columns
    numeric_columns = [
        "Aggregate rating",
        "Votes",
        "Price range",
        "Average Cost for two",
        "Longitude",
        "Latitude",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()


if df is None:
    st.error(f"Dataset not found:\n\n{DATA_FILE}")
    st.stop()


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_col(*names):
    normalized = {
        str(c).lower().strip(): c
        for c in df.columns
    }

    for name in names:
        key = name.lower().strip()

        if key in normalized:
            return normalized[key]

    for name in names:
        key = name.lower().strip()

        for col in df.columns:
            if key in str(col).lower():
                return col

    return None


COL_RESTAURANT = find_col("Restaurant Name")
COL_CITY = find_col("City")
COL_CUISINE = find_col("Cuisines")
COL_RATING = find_col("Aggregate rating")
COL_VOTES = find_col("Votes")
COL_PRICE = find_col("Price range")
COL_COST = find_col("Average Cost for two")
COL_BOOKING = find_col("Has Table booking")
COL_DELIVERY = find_col("Has Online delivery")
COL_LAT = find_col("Latitude")
COL_LON = find_col("Longitude")
COL_RATING_TEXT = find_col("Rating text")


# ============================================================
# GENERAL HELPERS
# ============================================================

def safe_series(col, default=0):
    if col and col in df.columns:
        return df[col]
    return pd.Series([default] * len(df), index=df.index)


def number(value):
    if pd.isna(value):
        return "—"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    if value.is_integer():
        return f"{int(value):,}"

    return f"{value:,.1f}"


def rating_value():
    s = pd.to_numeric(safe_series(COL_RATING, np.nan), errors="coerce")
    return s


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color="#cfcfc8",
        ),
        margin=dict(l=15, r=15, t=35, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#303030",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#202020",
            zeroline=False,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    return fig


def section_title(kicker, title, description):
    st.markdown(
        f"""
        <div class="section-kicker">{kicker}</div>
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def insight(text):
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-label">Key insight</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def table_controls(table_df, key_name, filename):
    """
    Each section has independent SHOW / HIDE / DOWNLOAD controls.
    """

    state_key = f"show_{key_name}"

    if state_key not in st.session_state:
        st.session_state[state_key] = False

    c1, c2, c3 = st.columns([0.8, 0.8, 1.0])

    with c1:
        if st.button(
            "SHOW",
            key=f"show_btn_{key_name}",
            use_container_width=True,
        ):
            st.session_state[state_key] = True

    with c2:
        if st.button(
            "HIDE",
            key=f"hide_btn_{key_name}",
            use_container_width=True,
        ):
            st.session_state[state_key] = False

    with c3:
        if st.session_state[state_key]:
            csv_bytes = table_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "DOWNLOAD",
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
                key=f"download_{key_name}",
                use_container_width=True,
            )

    if st.session_state[state_key]:
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
        )


def chart_card(title, subtitle, fig):
    st.markdown(
        f"""
        <div class="visual-panel">
            <div class="visual-label">{title} · {subtitle}</div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("### Restaurant Intelligence")
    st.caption("Explore your restaurant ecosystem")

    page = st.radio(
        "Explore",
        [
            "Overview",
            "Cuisine Intelligence",
            "City Intelligence",
            "Price Intelligence",
            "Rating Intelligence",
            "Geographic Intelligence",
            "Restaurant Chains",
            "Feedback Intelligence",
            "Votes Intelligence",
            "Service & Booking",
        ],
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="nav-small">Restaurant Intelligence</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-label">Restaurant data · intelligence · decisions</div>

    <div class="hero-title">
        Restaurant<br>
        <span class="hero-title-accent">intelligence.</span>
    </div>

    <div class="hero-text">
        Understand what's happening across restaurants, cuisines,
        locations, pricing, ratings, delivery and customer engagement —
        all through one intelligent analytics experience.
    </div>

    <div class="hero-tag">
        Data-driven restaurant intelligence
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    section_title(
        "01 · Overview",
        "Know what's happening.",
        "A high-level view of the restaurant ecosystem before you dive into individual intelligence areas.",
    )

    total_restaurants = len(df)

    total_cities = (
        df[COL_CITY].nunique()
        if COL_CITY
        else 0
    )

    total_cuisines = 0

    if COL_CUISINE:
        total_cuisines = (
            df[COL_CUISINE]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
            .replace("", np.nan)
            .dropna()
            .nunique()
        )

    avg_rating = rating_value().mean()

    total_votes = (
        pd.to_numeric(
            safe_series(COL_VOTES, 0),
            errors="coerce",
        )
        .fillna(0)
        .sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("Restaurants", number(total_restaurants)),
        ("Cities", number(total_cities)),
        ("Cuisines", number(total_cuisines)),
        ("Total votes", number(total_votes)),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        cards,
    ):
        with col:
            st.markdown(
                f"""
                <div class="intel-card">
                    <div class="intel-number">{value}</div>
                    <div class="intel-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:

        if COL_CITY:
            city_counts = (
                df[COL_CITY]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .sort_values()
            )

            fig = px.bar(
                city_counts,
                x=city_counts.values,
                y=city_counts.index,
                orientation="h",
                title="Restaurant concentration by city",
            )

            chart_layout(fig, 430)

            chart_card(
                "MARKET LANDSCAPE",
                "TOP CITIES",
                fig,
            )

            city_table = city_counts.reset_index()
            city_table.columns = ["City", "Restaurants"]

            table_controls(
                city_table,
                "overview_cities",
                "restaurant_city_overview.csv",
            )

    with right:

        if COL_RATING:

            rating_bins = pd.cut(
                rating_value(),
                bins=[
                    -0.01,
                    1,
                    2,
                    3,
                    4,
                    5.01,
                ],
                labels=[
                    "0–1",
                    "1–2",
                    "2–3",
                    "3–4",
                    "4–5",
                ],
            )

            rating_counts = (
                rating_bins
                .value_counts()
                .sort_index()
            )

            fig = px.bar(
                x=rating_counts.index.astype(str),
                y=rating_counts.values,
                title="Rating distribution",
            )

            chart_layout(fig, 430)

            chart_card(
                "PERFORMANCE",
                "RATING DISTRIBUTION",
                fig,
            )

            rating_table = rating_counts.reset_index()
            rating_table.columns = ["Rating Range", "Restaurants"]

            table_controls(
                rating_table,
                "overview_ratings",
                "restaurant_rating_overview.csv",
            )

    insight(
        f"The dataset contains {number(total_restaurants)} restaurants "
        f"across {number(total_cities)} cities, with an average rating "
        f"of {avg_rating:.2f}."
    )


# ============================================================
# CUISINE INTELLIGENCE
# ============================================================

elif page == "Cuisine Intelligence":

    section_title(
        "02 · Cuisine",
        "What do people eat?",
        "Understand the cuisine landscape, identify dominant categories and uncover where restaurant variety is concentrated.",
    )

    if not COL_CUISINE:
        st.warning("Cuisine information is not available.")
        st.stop()

    cuisine_data = (
        df[COL_CUISINE]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    cuisine_data = cuisine_data[cuisine_data != ""]

    cuisine_counts = (
        cuisine_data
        .value_counts()
        .head(15)
        .sort_values()
    )

    fig = px.bar(
        cuisine_counts,
        x=cuisine_counts.values,
        y=cuisine_counts.index,
        orientation="h",
        title="Most represented cuisines",
    )

    chart_layout(fig, 520)

    chart_card(
        "CUISINE LANDSCAPE",
        "TOP 15",
        fig,
    )

    top_cuisine = cuisine_counts.idxmax()

    insight(
        f"{top_cuisine} is the most represented cuisine in the dataset, "
        f"with {number(cuisine_counts.max())} restaurant records."
    )

    cuisine_table = cuisine_counts.reset_index()
    cuisine_table.columns = ["Cuisine", "Restaurants"]

    table_controls(
        cuisine_table,
        "cuisine",
        "cuisine_intelligence.csv",
    )


# ============================================================
# CITY INTELLIGENCE
# ============================================================

elif page == "City Intelligence":

    section_title(
        "03 · Cities",
        "Where is the market?",
        "Compare restaurant concentration and average ratings across cities to understand geographic market strength.",
    )

    if not COL_CITY:
        st.warning("City information is not available.")
        st.stop()

    city_summary = (
        df.groupby(COL_CITY)
        .agg(
            Restaurants=(COL_CITY, "size"),
            Average_Rating=(
                COL_RATING,
                "mean",
            ) if COL_RATING else (
                COL_CITY,
                "size",
            ),
        )
        .reset_index()
    )

    if COL_RATING:
        city_summary = city_summary.sort_values(
            "Restaurants",
            ascending=False,
        ).head(15)

        fig = px.bar(
            city_summary.sort_values("Restaurants"),
            x="Restaurants",
            y=COL_CITY,
            orientation="h",
            title="Largest restaurant markets",
        )

        chart_layout(fig, 520)

        chart_card(
            "CITY LANDSCAPE",
            "RESTAURANT CONCENTRATION",
            fig,
        )

        rating_city = (
            df.groupby(COL_CITY)[COL_RATING]
            .mean()
            .dropna()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
        )

        fig2 = px.bar(
            rating_city,
            x=rating_city.values,
            y=rating_city.index,
            orientation="h",
            title="Highest average-rated cities",
        )

        chart_layout(fig2, 450)

        chart_card(
            "CITY PERFORMANCE",
            "AVERAGE RATING",
            fig2,
        )

    else:
        city_counts = df[COL_CITY].value_counts().head(15).sort_values()

        fig = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation="h",
            title="Restaurants by city",
        )

        chart_layout(fig, 500)

        chart_card(
            "CITY LANDSCAPE",
            "RESTAURANT COUNT",
            fig,
        )

    table_controls(
        city_summary,
        "city",
        "city_intelligence.csv",
    )


# ============================================================
# PRICE INTELLIGENCE
# ============================================================

elif page == "Price Intelligence":

    section_title(
        "04 · Pricing",
        "What does the market charge?",
        "Explore price-range distribution and understand how service availability changes across pricing levels.",
    )

    if not COL_PRICE:
        st.warning("Price range information is not available.")
        st.stop()

    price_counts = (
        df[COL_PRICE]
        .dropna()
        .value_counts()
        .sort_index()
    )

    fig = px.bar(
        x=price_counts.index.astype(str),
        y=price_counts.values,
        title="Restaurant distribution by price range",
    )

    chart_layout(fig, 420)

    chart_card(
        "PRICE LANDSCAPE",
        "DISTRIBUTION",
        fig,
    )

    if COL_COST:
        cost_by_price = (
            df.groupby(COL_PRICE)[COL_COST]
            .mean()
            .dropna()
            .sort_index()
        )

        fig2 = px.line(
            x=cost_by_price.index.astype(str),
            y=cost_by_price.values,
            markers=True,
            title="Average cost for two by price range",
        )

        chart_layout(fig2, 400)

        chart_card(
            "SPENDING",
            "AVERAGE COST FOR TWO",
            fig2,
        )

    price_table = price_counts.reset_index()
    price_table.columns = ["Price Range", "Restaurants"]

    table_controls(
        price_table,
        "price",
        "price_intelligence.csv",
    )


# ============================================================
# RATING INTELLIGENCE
# ============================================================

elif page == "Rating Intelligence":

    section_title(
        "05 · Ratings",
        "How is performance perceived?",
        "Turn restaurant ratings into a clear view of quality distribution and overall customer perception.",
    )

    if not COL_RATING:
        st.warning("Rating information is not available.")
        st.stop()

    ratings = rating_value().dropna()

    fig = px.histogram(
        ratings,
        nbins=20,
        title="Restaurant rating distribution",
    )

    chart_layout(fig, 430)

    chart_card(
        "QUALITY SIGNAL",
        "RATING DISTRIBUTION",
        fig,
    )

    avg = ratings.mean()
    median = ratings.median()

    c1, c2, c3 = st.columns(3)

    for col, label, value in [
        (c1, "Average rating", f"{avg:.2f}"),
        (c2, "Median rating", f"{median:.2f}"),
        (c3, "Highest rating", f"{ratings.max():.2f}"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="intel-card">
                    <div class="intel-number">{value}</div>
                    <div class="intel-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if COL_RATING_TEXT:

        feedback_counts = (
            df[COL_RATING_TEXT]
            .dropna()
            .astype(str)
            .value_counts()
        )

        fig2 = px.bar(
            x=feedback_counts.index,
            y=feedback_counts.values,
            title="Rating feedback categories",
        )

        chart_layout(fig2, 400)

        chart_card(
            "CUSTOMER PERCEPTION",
            "RATING TEXT",
            fig2,
        )

    rating_table = (
        pd.DataFrame(
            {
                "Rating": ratings.round(2)
            }
        )
        .value_counts()
        .reset_index(name="Restaurants")
    )

    table_controls(
        rating_table,
        "ratings",
        "rating_intelligence.csv",
    )


# ============================================================
# GEOGRAPHIC INTELLIGENCE
# ============================================================

elif page == "Geographic Intelligence":

    section_title(
        "06 · Geography",
        "Where are restaurants located?",
        "Explore the spatial distribution of restaurants and identify geographic concentrations in the market.",
    )

    if not COL_LAT or not COL_LON:
        st.warning(
            "Latitude and Longitude columns were not found in the dataset."
        )
        st.stop()

    geo = df[
        [
            c
            for c in [
                COL_RESTAURANT,
                COL_CITY,
                COL_LAT,
                COL_LON,
                COL_RATING,
            ]
            if c
        ]
    ].copy()

    geo[COL_LAT] = pd.to_numeric(
        geo[COL_LAT],
        errors="coerce",
    )

    geo[COL_LON] = pd.to_numeric(
        geo[COL_LON],
        errors="coerce",
    )

    geo = geo.dropna(
        subset=[COL_LAT, COL_LON]
    )

    geo = geo[
        geo[COL_LAT].between(-90, 90)
        & geo[COL_LON].between(-180, 180)
    ]

    if len(geo) == 0:
        st.warning("No valid geographic coordinates were found.")
        st.stop()

    # Limit visual points for performance.
    map_data = geo.sample(
        min(len(geo), 3500),
        random_state=42,
    )

    hover_cols = []

    if COL_RESTAURANT:
        hover_cols.append(COL_RESTAURANT)

    if COL_CITY:
        hover_cols.append(COL_CITY)

    if COL_RATING:
        hover_cols.append(COL_RATING)

    fig = px.scatter_geo(
        map_data,
        lat=COL_LAT,
        lon=COL_LON,
        hover_name=COL_RESTAURANT if COL_RESTAURANT else None,
        hover_data=hover_cols,
        projection="natural earth",
        title="Restaurant geographic distribution",
    )

    fig.update_geos(
        showland=True,
        landcolor="#161616",
        showocean=True,
        oceancolor="#090909",
        showcountries=True,
        countrycolor="#363636",
        showcoastlines=True,
        coastlinecolor="#333333",
    )

    fig.update_traces(
        marker=dict(
            size=5,
            opacity=0.65,
        )
    )

    fig.update_layout(
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)"
        ),
        font=dict(color="#cfcfc8"),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    chart_card(
        "GEOGRAPHIC LANDSCAPE",
        "RESTAURANT LOCATIONS",
        fig,
    )

    insight(
        f"{number(len(geo))} restaurants contain valid latitude and longitude "
        "coordinates and are available for geographic analysis."
    )

    table_controls(
        geo,
        "geographic",
        "geographic_restaurant_locations.csv",
    )


# ============================================================
# RESTAURANT CHAINS
# ============================================================

elif page == "Restaurant Chains":

    section_title(
        "07 · Chains",
        "Which brands scale?",
        "Identify restaurant names with multiple outlets and compare their presence, ratings and popularity.",
    )

    if not COL_RESTAURANT:
        st.warning("Restaurant Name information is not available.")
        st.stop()

    chain_counts = (
        df[COL_RESTAURANT]
        .dropna()
        .astype(str)
        .value_counts()
    )

    chain_counts = chain_counts[
        chain_counts > 1
    ].head(15).sort_values()

    fig = px.bar(
        x=chain_counts.values,
        y=chain_counts.index,
        orientation="h",
        title="Restaurant brands by outlet count",
    )

    chart_layout(fig, 500)

    chart_card(
        "BRAND SCALE",
        "TOP RESTAURANT CHAINS",
        fig,
    )

    if COL_RATING:

        chain_rating = (
            df.groupby(COL_RESTAURANT)[COL_RATING]
            .agg(
                Outlets="size",
                Average_Rating="mean",
            )
            .query("Outlets > 1")
            .sort_values(
                "Average_Rating",
                ascending=False,
            )
            .head(15)
            .sort_values("Average_Rating")
        )

        fig2 = px.bar(
            chain_rating,
            x="Average_Rating",
            y=chain_rating.index,
            orientation="h",
            title="Highest-rated multi-outlet brands",
        )

        chart_layout(fig2, 500)

        chart_card(
            "BRAND PERFORMANCE",
            "AVERAGE RATING",
            fig2,
        )

    chain_table = (
        chain_counts
        .reset_index()
    )

    chain_table.columns = [
        "Restaurant Chain",
        "Outlets",
    ]

    table_controls(
        chain_table,
        "chains",
        "restaurant_chains.csv",
    )


# ============================================================
# FEEDBACK INTELLIGENCE
# ============================================================

elif page == "Feedback Intelligence":

    section_title(
        "08 · Feedback",
        "What are customers saying?",
        "Use rating feedback categories as a customer-perception signal and understand how restaurants are distributed across sentiment-like rating labels.",
    )

    if not COL_RATING_TEXT:
        st.warning(
            "No Rating text column was found."
        )
        st.stop()

    feedback = (
        df[COL_RATING_TEXT]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
    )

    fig = px.bar(
        x=feedback.index,
        y=feedback.values,
        title="Rating feedback categories",
    )

    chart_layout(fig, 430)

    chart_card(
        "CUSTOMER SIGNAL",
        "FEEDBACK CATEGORIES",
        fig,
    )

    if len(feedback) > 0:
        dominant = feedback.idxmax()

        insight(
            f"The most common rating feedback category is "
            f"'{dominant}', representing {number(feedback.max())} restaurants."
        )

    feedback_table = feedback.reset_index()
    feedback_table.columns = [
        "Feedback Category",
        "Restaurants",
    ]

    table_controls(
        feedback_table,
        "feedback",
        "feedback_intelligence.csv",
    )

    st.caption(
        "Note: the dataset contains rating feedback categories rather "
        "than full written customer review comments."
    )


# ============================================================
# VOTES INTELLIGENCE
# ============================================================

elif page == "Votes Intelligence":

    section_title(
        "09 · Engagement",
        "Which restaurants get attention?",
        "Votes provide an engagement signal that can reveal restaurants receiving unusually high levels of customer interaction.",
    )

    if not COL_VOTES:
        st.warning("Votes information is not available.")
        st.stop()

    votes = pd.to_numeric(
        safe_series(COL_VOTES, 0),
        errors="coerce",
    ).fillna(0)

    if COL_RESTAURANT:

        vote_df = pd.DataFrame(
            {
                "Restaurant": df[COL_RESTAURANT],
                "Votes": votes,
            }
        ).dropna(subset=["Restaurant"])

        top_votes = (
            vote_df
            .groupby("Restaurant")["Votes"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values()
        )

        fig = px.bar(
            x=top_votes.values,
            y=top_votes.index,
            orientation="h",
            title="Restaurants receiving the most votes",
        )

        chart_layout(fig, 500)

        chart_card(
            "CUSTOMER ENGAGEMENT",
            "TOP VOTED RESTAURANTS",
            fig,
        )

        vote_table = top_votes.reset_index()
        vote_table.columns = [
            "Restaurant",
            "Votes",
        ]

        table_controls(
            vote_table,
            "votes",
            "votes_intelligence.csv",
        )

    if COL_RATING:

        correlation_df = pd.DataFrame(
            {
                "Rating": rating_value(),
                "Votes": votes,
            }
        ).dropna()

        if len(correlation_df) > 2:

            correlation = correlation_df[
                "Rating"
            ].corr(
                correlation_df["Votes"]
            )

            fig2 = px.scatter(
                correlation_df.sample(
                    min(len(correlation_df), 3000),
                    random_state=42,
                ),
                x="Rating",
                y="Votes",
                title="Votes vs rating",
                opacity=0.55,
            )

            chart_layout(fig2, 430)

            chart_card(
                "ENGAGEMENT PATTERN",
                "VOTES VS RATING",
                fig2,
            )

            insight(
                f"The correlation between rating and votes is "
                f"{correlation:.2f}."
            )


# ============================================================
# SERVICE & BOOKING
# ============================================================

elif page == "Service & Booking":

    section_title(
        "10 · Services",
        "How do restaurants serve customers?",
        "Compare online delivery and table-booking availability to understand the service layer across the restaurant market.",
    )

    left, right = st.columns(2)

    if COL_DELIVERY:

        delivery = (
            df[COL_DELIVERY]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        fig = px.pie(
            names=delivery.index,
            values=delivery.values,
            hole=0.65,
            title="Online delivery availability",
        )

        fig.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cfcfc8"),
            margin=dict(l=10, r=10, t=45, b=10),
            legend=dict(
                bgcolor="rgba(0,0,0,0)"
            ),
        )

        with left:
            chart_card(
                "DELIVERY",
                "ONLINE AVAILABILITY",
                fig,
            )

        delivery_table = delivery.reset_index()
        delivery_table.columns = [
            "Online Delivery",
            "Restaurants",
        ]

        with left:
            table_controls(
                delivery_table,
                "delivery",
                "delivery_service.csv",
            )

    if COL_BOOKING:

        booking = (
            df[COL_BOOKING]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        fig2 = px.pie(
            names=booking.index,
            values=booking.values,
            hole=0.65,
            title="Table booking availability",
        )

        fig2.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cfcfc8"),
            margin=dict(l=10, r=10, t=45, b=10),
            legend=dict(
                bgcolor="rgba(0,0,0,0)"
            ),
        )

        with right:
            chart_card(
                "BOOKING",
                "TABLE RESERVATIONS",
                fig2,
            )

        booking_table = booking.reset_index()
        booking_table.columns = [
            "Table Booking",
            "Restaurants",
        ]

        with right:
            table_controls(
                booking_table,
                "booking",
                "booking_service.csv",
            )

    # Price vs service comparison
    if COL_PRICE and COL_DELIVERY:

        service_df = df[
            [COL_PRICE, COL_DELIVERY]
        ].copy()

        service_df[COL_PRICE] = pd.to_numeric(
            service_df[COL_PRICE],
            errors="coerce",
        )

        service_df = service_df.dropna(
            subset=[COL_PRICE]
        )

        service_summary = (
            pd.crosstab(
                service_df[COL_PRICE],
                service_df[COL_DELIVERY],
                normalize="index",
            )
            .mul(100)
            .round(1)
        )

        fig3 = px.bar(
            service_summary,
            barmode="group",
            title="Online delivery availability by price range",
        )

        chart_layout(fig3, 450)

        chart_card(
            "SERVICE ECONOMICS",
            "PRICE VS DELIVERY",
            fig3,
        )

        table_controls(
            service_summary.reset_index(),
            "service_price",
            "price_delivery_comparison.csv",
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Restaurant Intelligence · Data Analytics · Python · Pandas · Plotly · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)