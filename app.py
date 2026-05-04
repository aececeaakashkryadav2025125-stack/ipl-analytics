import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---- LOAD MODEL ----

model = pickle.load(open('models/model.pkl', 'rb'))

st.set_page_config(page_title="IPL Predictor", layout="centered")

st.title("🏏 IPL Win Predictor")
st.write("Enter match situation:")

teams = [
"Mumbai Indians", "Chennai Super Kings", "RCB",
"KKR", "Delhi Capitals", "Punjab Kings"
]

# ---- INPUTS ----

batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)

balls_left = st.number_input("Balls Left", min_value=1, max_value=120, value=60)
wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, value=5)
current_score = st.number_input("Current Score", min_value=0, value=100)
target = st.number_input("Target Score", min_value=1, value=180)

# ---- PREDICT ----

if st.button("Predict"):


# ---- CALCULATIONS ----


    # ---- CALCULATIONS ----
    runs_left = target - current_score
    balls_left_safe = max(balls_left, 1)

    required_run_rate = (runs_left * 6) / balls_left_safe

    overs_completed = (120 - balls_left) / 6
    current_run_rate = current_score / max(overs_completed, 1)

    # ---- VALIDATION ----
    if batting_team == bowling_team:
        st.error("Batting and Bowling team cannot be same ❌")
        st.stop()

    if runs_left <= 0:
        st.success(f"{batting_team} already WON 🏆")
        st.stop()

    if wickets_left == 0:
        st.error("All wickets lost ❌")
        st.stop()

    # ---- CREATE INPUT ----
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'current_score': [current_score],
        'runs_left': [runs_left],
        'required_run_rate': [required_run_rate]
    })

    # ---- PREDICT ----
    result = model.predict_proba(input_df)[0]

    win_prob = round(result[1] * 100, 2)
    lose_prob = round(result[0] * 100, 2)

    # ---- METRICS ----
    st.metric("Winning %", f"{win_prob}%")
    st.metric("Losing %", f"{lose_prob}%")

    # ---- PROGRESS BAR ----
    st.progress(int(win_prob))

    # ---- MATCH INSIGHTS ----
    st.write(f"Runs Left: {runs_left}")
    st.write(f"Required Run Rate: {round(required_run_rate, 2)}")
    st.write(f"Current Run Rate: {round(current_run_rate, 2)}")

    # ---- MATCH STATUS ----
    if win_prob > 70:
        st.success("🔥 Strong winning position")
    elif win_prob > 40:
        st.warning("⚖️ Balanced match")
    else:
        st.error("📉 Losing position")

    # ---- GRAPH ----
    fig, ax = plt.subplots()

    labels = ['Win', 'Lose']
    values = [win_prob, lose_prob]

    ax.bar(labels, values)
    ax.set_ylabel("Probability (%)")
    ax.set_title("Match Win Probability")

    st.pyplot(fig)
