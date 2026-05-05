import streamlit as st
from utils.api import get_live_matches
import time

st.set_page_config(layout="wide")

st.title("🏏 Live Matches (Cricbuzz Style)")

# ---- AUTO REFRESH ----
REFRESH_SECONDS = 15

# ---- FETCH DATA ----
matches = get_live_matches()

# ---- UI ----
if matches and len(matches) > 0:

    st.markdown("### 🔴 Live Matches")

    cols = st.columns(3)  # 3 cards per row

    for i, match in enumerate(matches[:6]):

        with cols[i % 3]:

            st.markdown("### 🟢 MATCH")

            team1 = match.get("team1", "Team A")
            team2 = match.get("team2", "Team B")
            venue = match.get("venue", "Unknown Venue")

            st.markdown(f"**{team1} vs {team2}**")
            st.markdown(f"📍 {venue}")

            st.markdown("---")

            if st.button("🔮 Predict", key=f"predict_{i}"):
                st.switch_page("pages/2_Predictor.py")

else:
    st.warning("🚫 No live IPL matches right now")

    # ✅ DEMO FALLBACK (VERY IMPORTANT)
    st.markdown("### 🔁 Demo Match (for testing)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🟡 CSK")
        st.markdown("### 120/3")
        st.markdown("Overs: 12")

    with col2:
        st.markdown("## 🔵 MI")
        st.markdown("Bowling")

    st.markdown("---")

    st.info("This is demo data because live API returned no matches")

    if st.button("🔮 Predict Demo Match"):
        st.switch_page("pages/2_Predictor.py")

    # Debug section
    with st.expander("🔍 Debug API Response"):
        st.write(matches)

# ---- AUTO REFRESH ----
st.caption(f"🔄 Auto-refreshing every {REFRESH_SECONDS} seconds")

time.sleep(REFRESH_SECONDS)
st.rerun()