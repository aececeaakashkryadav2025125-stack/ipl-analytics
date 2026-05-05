import streamlit as st
from utils.api import get_live_matches
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("🏏 Live Matches (Cricbuzz Style)")

# 🔁 Auto refresh
st_autorefresh(interval=15000, key="live_refresh")

matches = get_live_matches()

if matches:

    cols = st.columns(3)  # 3 cards per row

    for i, match in enumerate(matches[:6]):  # limit to 6 matches

        with cols[i % 3]:
            st.markdown("### 🟢 LIVE")

            st.markdown(f"**{match.get('team1')} vs {match.get('team2')}**")

            st.markdown(f"📍 {match.get('venue', 'Unknown')}")

            st.markdown("---")

            st.button(
                "🔮 Predict",
                key=f"predict_{i}"
            )

else:
    st.warning("No matches available")