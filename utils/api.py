import requests
import streamlit as st

# ✅ DEFINE API KEY (THIS WAS MISSING)
API_KEY = st.secrets["API_KEY"]

def get_live_matches():
    url = f"https://api.cricketdata.org/v1/matches?apikey={API_KEY}"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        data = response.json()
        matches = data.get("data", [])

        return matches

    except Exception as e:
        print("API ERROR:", e)
        return []