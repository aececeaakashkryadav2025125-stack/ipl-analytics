import streamlit as st
from utils.api import get_live_matches
import time

st.set_page_config(layout="wide")

st.title("🏏 Live Matches (Cricbuzz Style)")

# ---- AUTO REFRESH (NO EXTRA LIBRARY) ----
REFRESH_SECONDS = 15

# ---- FETCH DATA ----
matches = get_live_matches()

# ---- UI ----
if matches:

    st.markdown("### 🔴 Live Matches")

    cols = st.columns(3)  # 3 cards per row

    for i, match in enumerate(matches[:6]):  # limit to 6 matches

        with cols[i % 3]:

            st.markdown("### 🟢 LIVE")

            team1 = match.get("team1", "Team A")
            team2 = match.get("team2", "Team B")
            venue = match.get("venue", "Unknown Venue")

            st.markdown(f"**{team1} vs {team2}**")
            st.markdown(f"📍 {venue}")

            st.markdown("---")

            st.button(
                "🔮 Predict",
                key=f"predict_{i}"
            )

else:
    st.warning("🚫 No matches available or API failed")

    # Debug (optional)
    with st.expander("🔍 Debug API Response"):
        st.write(matches)

# ---- AUTO REFRESH LOOP ----
st.caption(f"🔄 Auto-refreshing every {REFRESH_SECONDS} seconds")

time.sleep(REFRESH_SECONDS)
st.rerun()