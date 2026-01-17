import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="YouTube Channel Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOGO & TITLE ----------------
st.image("logo.jpg", width=120)
st.title("📊 YouTube Channel Analyzer")
st.write("Upload **multiple YouTube Analytics CSV files** and get instant insights.")

# ---------------- FILE UPLOADER ----------------
uploaded_files = st.file_uploader(
    "Upload YouTube Analytics CSV files",
    type="csv",
    accept_multiple_files=True
)

# ---------------- HELPER FUNCTION ----------------
def find_column(possible_names, columns):
    for col in columns:
        for name in possible_names:
            if name.lower() in col.lower():
                return col
    return None

# ---------------- MAIN LOGIC ----------------
if uploaded_files:
    dfs = []

    for file in uploaded_files:
        df = pd.read_csv(file)
        df["Source File"] = file.name
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    st.success(f"✅ {len(uploaded_files)} CSV files uploaded and combined!")

    # ---------------- COLUMN DETECTION ----------------
    views_col = find_column(["views"], df.columns)
    likes_col = find_column(["like"], df.columns)
    comments_col = find_column(["comment"], df.columns)
    ctr_col = find_column(["ctr"], df.columns)
    watch_col = find_column(["average view duration", "watch"], df.columns)
    publish_col = find_column(["publish"], df.columns)

    # ---------------- METRICS ----------------
    total_views = df[views_col].sum() if views_col else 0
    avg_views = int(df[views_col].mean()) if views_col else 0
    total_likes = df[likes_col].sum() if likes_col else 0
    total_comments = df[comments_col].sum() if comments_col else 0
    avg_ctr = round(df[ctr_col].mean(), 2) if ctr_col else 0
    avg_watch = int(df[watch_col].mean()) if watch_col else 0

    engagement_rate = (
        round((total_likes + total_comments) / total_views * 100, 2)
        if total_views > 0 else 0
    )

    # ---------------- DISPLAY METRICS ----------------
    st.subheader("📈 Channel Performance")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Views", f"{total_views:,}")
    col2.metric("Avg Views / Video", f"{avg_views:,}")
    col3.metric("Avg CTR (%)", avg_ctr)
    col4.metric("Avg Watch Time (sec)", avg_watch)
    col5.metric("Engagement (%)", engagement_rate)

    # ---------------- BEST TIME TO POST ----------------
    best_time = "Not enough data"
    best_day = "Not enough data"

    if publish_col and views_col:
        df[publish_col] = pd.to_datetime(df[publish_col], errors="coerce")
        df["Hour"] = df[publish_col].dt.hour
        df["Day"] = df[publish_col].dt.day_name()

        best_hour = int(df.groupby("Hour")[views_col].mean().idxmax())
        best_day = df.groupby("Day")[views_col].mean().idxmax()

        best_time = f"{best_hour % 12 or 12}:00 {'AM' if best_hour < 12 else 'PM'}"

    st.subheader("📅 Best Time to Post")
    st.write(f"**Best Day:** {best_day}")
    st.write(f"**Best Time:** {best_time}")

    # ---------------- WEAK POINTS ----------------
    st.subheader("⚠️ Areas to Improve")

    weak_points = []

    if avg_ctr < 5:
        weak_points.append("Low CTR – Improve thumbnails & titles")
    if avg_watch < 30:
        weak_points.append("Low watch time – Hook viewers in first 5 seconds")
    if engagement_rate < 2:
        weak_points.append("Low engagement – Ask viewers to like & comment")

    if not weak_points:
        weak_points.append("✅ No critical weaknesses detected")

    for w in weak_points:
        st.warning(w)

    # ---------------- STRATEGY ----------------
    st.subheader("🚀 Actionable Growth Strategy")
    st.markdown("""
- Use **faces + emotions** in thumbnails  
- Titles = **Curiosity + Clear benefit**  
- Hook viewers in **first 3–5 seconds**  
- Post **Shorts daily (1–2/day)**  
- Long videos **2–3/week**  
- Pin comments & reply fast  
""")

    # ---------------- DATA PREVIEW ----------------
    with st.expander("🔍 View Combined Data"):
        st.dataframe(df.head(100))

else:
    st.info("⬆️ Upload 1 or more CSV files to start analysis.")
