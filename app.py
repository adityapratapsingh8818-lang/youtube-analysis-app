import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(page_title="APS Growth - YouTube Analyzer", layout="wide")

# Show logo
st.image("logo.jpg", width=200)

st.title("📊 YouTube Channel Analyzer")
st.write("Upload your YouTube CSV data and get instant insights & suggestions.")

# Upload CSV
uploaded_file = st.file_uploader("Upload YouTube Analytics CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📌 Key Insights")

    if "Views" in df.columns:
        st.write("👉 Total Views:", int(df["Views"].sum()))

    if "Watch time (hours)" in df.columns:
        st.write("👉 Total Watch Time (hours):", round(df["Watch time (hours)"].sum(), 2))

    if "Impressions click-through rate (%)" in df.columns:
        avg_ctr = df["Impressions click-through rate (%)"].mean()
        st.write("👉 Average CTR:", round(avg_ctr, 2), "%")

        if avg_ctr < 5:
            st.error("⚠️ CTR is low. Improve thumbnails & titles.")
        else:
            st.success("✅ CTR is good. Keep consistency.")

    st.subheader("🚀 AI Suggestions")
    st.write("""
    • Post consistently (2–3 times per week)  
    • Use strong hooks in first 5 seconds  
    • Create Shorts from long videos  
    • Improve thumbnails with faces & emotions  
    • Use keywords in title + description  
    """)

    st.subheader("⏰ Best Time to Post")
    st.write("📅 Best days: **Wednesday, Friday, Sunday**")
    st.write("🕕 Best time: **6 PM – 9 PM (IST)**")

else:
    st.info("👆 Upload a CSV file to start analysis.")
