import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---- LOAD MODEL ----
model = pickle.load(open('models/model.pkl', 'rb'))

st.title("🤖 IPL Win Predictor")

teams = [
    "Mumbai Indians", "Chennai Super Kings", "RCB",
    "KKR", "Delhi Capitals", "Punjab Kings"
]

# ---- INPUT UI ----
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)
    balls_left = st.slider("Balls Left", 1, 120, 60)
    current_score = st.number_input("Current Score", min_value=0, value=100)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)
    wickets_left = st.slider("Wickets Left", 0, 10, 5)
    target = st.number_input("Target Score", min_value=1, value=180)

# ---- BUTTON ----
if st.button("Predict"):

    # validation
    if batting_team == bowling_team:
        st.warning("⚠️ Select different teams")
        st.stop()

    runs_left = target - current_score
    balls_left_safe = max(balls_left, 1)

    if runs_left <= 0:
        st.success(f"{batting_team} already WON 🏆")
        st.stop()

    if wickets_left == 0:
        st.error("All wickets lost ❌")
        st.stop()

    required_run_rate = (runs_left * 6) / balls_left_safe

    overs_completed = (120 - balls_left) / 6
    current_run_rate = current_score / max(overs_completed, 1)

    # dataframe
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'current_score': [current_score],
        'runs_left': [runs_left],
        'required_run_rate': [required_run_rate]
    })

    # prediction
    result = model.predict_proba(input_df)[0]

    win_prob = round(result[1] * 100, 2)
    lose_prob = round(result[0] * 100, 2)

    # output
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

    if win_prob > 70:
        st.success("🔥 Strong winning position")
    elif win_prob > 40:
        st.warning("⚖️ Balanced match")
    else:
        st.error("📉 Under pressure")

    # graph
    fig, ax = plt.subplots()
    ax.bar(["Win", "Lose"], [win_prob, lose_prob])
    ax.set_ylabel("Probability (%)")

    st.pyplot(fig)