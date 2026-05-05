import streamlit as st
from utils.api import get_matches
import time

st.set_page_config(layout="wide")

st.title("🏏 Live Matches (Cricbuzz Style)")

REFRESH_SECONDS = 15

# ---- FETCH ----
matches, match_type = get_matches()

# ---- UI ----
if matches:

    # ✅ FIXED INDENTATION
    if match_type == "live":
        st.success("🔴 Live Matches")
    elif match_type == "upcoming":
        st.info("📅 Upcoming Matches")
    elif match_type == "demo":
        st.warning("⚠️ Demo Matches (API returned no data)")

    # ✅ SHOW CARDS FOR ALL CASES
    cols = st.columns(3)

    for i, match in enumerate(matches[:6]):

        with cols[i % 3]:

            team1 = match.get("team1", "Team A")
            team2 = match.get("team2", "Team B")
            venue = match.get("venue", "Unknown Venue")
            date = match.get("date", "")

            st.markdown("### 🟢 MATCH")

            st.markdown(f"**{team1} vs {team2}**")
            st.markdown(f"📍 {venue}")

            if date:
                st.caption(f"📅 {date}")

            st.markdown("---")

            st.button("🔮 Predict", key=f"predict_{i}")

else:
    st.error("❌ No matches found (API issue or quota exceeded)")

    with st.expander("🔍 Debug API Response"):
        st.write(matches)

# ---- AUTO REFRESH ----
st.caption(f"🔄 Auto-refresh every {REFRESH_SECONDS} seconds")

time.sleep(REFRESH_SECONDS)
st.rerun()