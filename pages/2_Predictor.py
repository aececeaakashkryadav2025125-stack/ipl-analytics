import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---- LOAD MODEL ----
model = pickle.load(open('models/model.pkl', 'rb'))

st.set_page_config(layout="wide")

st.title("🔮 IPL Win Predictor")

# ---- TEAMS ----
teams = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "RCB",
    "KKR",
    "Delhi Capitals",
    "Punjab Kings"
]

# ---- SESSION AUTO-FILL (IMPORTANT FIX) ----
default_batting = st.session_state.get("batting_team", teams[0])
default_bowling = st.session_state.get("bowling_team", teams[1])

# fallback safety (if API sends unknown team)
if default_batting not in teams:
    default_batting = teams[0]

if default_bowling not in teams:
    default_bowling = teams[1]

# ---- INPUT UI ----
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox(
        "Batting Team",
        teams,
        index=teams.index(default_batting)
    )

with col2:
    bowling_team = st.selectbox(
        "Bowling Team",
        teams,
        index=teams.index(default_bowling)
    )

target = st.number_input("Target", min_value=1, value=180)
current_score = st.number_input("Current Score", min_value=0, value=100)
overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=10.0)
wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, value=5)

# ---- CALCULATIONS ----
balls_left = int((20 - overs) * 6)
runs_left = target - current_score

# ---- BUTTON ----
if st.button("Predict"):

    if batting_team == bowling_team:
        st.warning("⚠️ Select different teams")
        st.stop()

    balls_left_safe = max(balls_left, 1)

    if runs_left <= 0:
        st.success(f"{batting_team} already WON 🏆")
        st.stop()

    if wickets_left == 0:
        st.error("All wickets lost ❌")
        st.stop()

    required_run_rate = (runs_left * 6) / balls_left_safe

    overs_completed = max(overs, 1)
    current_run_rate = current_score / overs_completed

    # ---- DATAFRAME ----
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'current_score': [current_score],
        'runs_left': [runs_left],
        'required_run_rate': [required_run_rate]
    })

    # ---- PREDICTION ----
    result = model.predict_proba(input_df)[0]

    win_prob = round(result[1] * 100, 2)
    lose_prob = round(result[0] * 100, 2)

    # ---- OUTPUT ----
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🏆 Win %", f"{win_prob}%")

    with col2:
        st.metric("❌ Lose %", f"{lose_prob}%")

    st.progress(int(win_prob))

    st.subheader("📊 Match Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Runs Left", runs_left)
    col2.metric("Req RR", round(required_run_rate, 2))
    col3.metric("Curr RR", round(current_run_rate, 2))

    # ---- STATUS ----
    if win_prob > 70:
        st.success("🔥 Strong winning position")
    elif win_prob > 40:
        st.warning("⚖️ Balanced match")
    else:
        st.error("📉 Under pressure")

    # ---- GRAPH ----
    fig, ax = plt.subplots()
    ax.bar(["Win", "Lose"], [win_prob, lose_prob])
    ax.set_ylabel("Probability (%)")

    st.pyplot(fig)