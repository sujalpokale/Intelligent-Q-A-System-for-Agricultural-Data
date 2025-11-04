import streamlit as st
import pandas as pd
from planner import parse_query
from analysis import compare_rainfall_and_top_crops, trend_and_correlation, district_max_crop
from db import read_sql, init_db

# === Streamlit configuration ===
st.set_page_config(page_title="Samarth Q&A Demo", layout="wide")
init_db()

st.title("🌾 Project Samarth — Q&A over data.gov.in datasets")

query = st.text_area("Ask a question (examples:)", 
                     placeholder="e.g., Compare rainfall in Maharashtra and Gujarat for the last 10 years",
                     height=120)

if st.button("Run"):
    if not query.strip():
        st.warning("Please type a question.")
    else:
        plan = parse_query(query)
        intent = plan.get("intent")
        st.write("**Planned intent:**", intent)

        # === Intent: Compare rainfall and top crops ===
        if intent == "compare_rainfall_and_top_crops":
            state_x = plan["state_x"]
            state_y = plan["state_y"]
            n = plan["year_num"]

            df_years = read_sql("SELECT DISTINCT year FROM rainfall_annual_state ORDER BY year DESC")
            if df_years.empty:
                st.error("⚠️ No rainfall data loaded. Please run normalization first.")
            else:
                max_year = int(df_years["year"].max())
                years = list(range(max_year - n + 1, max_year + 1))

                st.info(f"Comparing {state_x} vs {state_y} for years {years[0]}–{years[-1]}")
                resp = compare_rainfall_and_top_crops(state_x, state_y, years, top_m=5)

                st.subheader("📊 Average Annual Rainfall (mm)")
                st.dataframe(resp["rainfall_avg"])

                st.subheader(f"🌾 Top Crops in {state_x}")
                st.dataframe(pd.DataFrame(resp["top_crops_state_x"], columns=["Crop ID"]))

                st.subheader(f"🌾 Top Crops in {state_y}")
                st.dataframe(pd.DataFrame(resp["top_crops_state_y"], columns=["Crop ID"]))

                st.subheader("🔎 Provenance — Rainfall Data Used")
                st.dataframe(resp["rain_provenance"].head(100))

                st.subheader("🔎 Provenance — Crop Data Used")
                st.dataframe(resp["crop_provenance"].head(100))

        # === Intent: District with highest crop production ===
        elif intent == "district_max_crop":
            state = plan["state"]
            crop = plan["crop"]
            st.info(f"Finding highest and lowest producing districts for {crop} in {state}...")
            resp = district_max_crop(state, crop)
            st.json(resp)

        # === Intent: Crop trend and correlation with rainfall ===
        elif intent == "trend_and_correlation":
            state = plan["state"]
            crop = plan["crop"]
            n = plan["year_num"]

            df_years = read_sql("SELECT DISTINCT year FROM rainfall_annual_state ORDER BY year DESC")
            if df_years.empty:
                st.error("⚠️ No rainfall data loaded. Please run normalization first.")
            else:
                max_year = int(df_years["year"].max())
                years = list(range(max_year - n + 1, max_year + 1))

                st.info(f"Analyzing {crop} trend in {state} for years {years[0]}–{years[-1]}")
                resp = trend_and_correlation(state, crop, years)
                st.subheader("📈 Production Trend and Rainfall Correlation")
                st.json(resp)

        # === Unknown intent ===
        else:
            st.error("Sorry, I couldn't understand that question. Try examples like:")
            st.markdown("""
            - Compare rainfall in Maharashtra and Gujarat for the last 10 years  
            - Identify the district in Punjab with the highest production of wheat  
            - Analyze the trend of rice production in Kerala over the past 8 years
            """)
