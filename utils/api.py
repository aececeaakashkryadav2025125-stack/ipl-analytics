import streamlit as st
import requests

API_KEY = st.secrets.get("API_KEY", "")

BASE_URL = "https://api.cricketdata.org/v1/matches"


def fetch_matches(params):
    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print("API ERROR:", e)
        return []


def get_live_matches():
    return fetch_matches({
        "apikey": API_KEY,
        "status": "live"
    })


def get_upcoming_matches():
    return fetch_matches({
        "apikey": API_KEY,
        "status": "upcoming"
    })


# ✅ THIS IS THE MISSING FUNCTION
def get_matches():
    live = get_live_matches()

    if live:
        return live, "live"

    upcoming = get_upcoming_matches()

    if upcoming:
        return upcoming, "upcoming"

    # 🔥 DEMO FALLBACK (VERY IMPORTANT)
    return [
        {
            "team1": "Chennai Super Kings",
            "team2": "Mumbai Indians",
            "venue": "Wankhede Stadium",
            "date": "Today 7:30 PM"
        },
        {
            "team1": "RCB",
            "team2": "KKR",
            "venue": "Chinnaswamy Stadium",
            "date": "Tomorrow 7:30 PM"
        }
    ], "demo"