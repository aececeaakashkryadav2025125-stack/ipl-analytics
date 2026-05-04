import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# ---- CUSTOM STYLING ----
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# ---- LOAD MODEL ----
model = pickle.load(open('models/model.pkl', 'rb'))

# ---- PAGE CONFIG ----
st.set_page_config(page_title="IPL Predictor", layout="centered")

st.title("🏏 IPL Win Predictor")
st.markdown("### 📊 Real-time match win probability predictor")
st.divider()

teams = [
    "Mumbai Indians", "Chennai Super Kings", "RCB",
    "KKR", "Delhi Capitals", "Punjab Kings"
]

# ---- INPUT UI (COLUMNS) ----
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)
    balls_left = st.slider("Balls Left", 1, 120, 60)
    current_score = st.number_input("Current Score", min_value=0, value=100)

with col2:
    bowling_team = st.selectbox("Bowling Team", teams)
    wickets_left = st.slider("Wickets Left", 0, 10, 5)
    target = st.number_input("Target Score", min_value=1, value=180)

# ---- PREDICTION ----
if st.button("Predict"):

    # ---- VALIDATION ----
    if batting_team == bowling_team:
        st.warning("⚠️ Select different teams")
        st.stop()

    # ---- CALCULATIONS ----
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
    with st.spinner("Calculating match outcome..."):
        result = model.predict_proba(input_df)[0]

    win_prob = round(result[1] * 100, 2)
    lose_prob = round(result[0] * 100, 2)

    # ---- METRICS ----
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🏆 Win %", f"{win_prob}%", delta=f"{win_prob - 50:.2f}")

    with col2:
        st.metric("❌ Lose %", f"{lose_prob}%", delta=f"{lose_prob - 50:.2f}")

    # ---- PROGRESS BAR ----
    st.progress(int(win_prob))

    # ---- MATCH INSIGHTS ----
    st.subheader("📌 Match Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Runs Left", runs_left)
    col2.metric("Req RR", round(required_run_rate, 2))
    col3.metric("Curr RR", round(current_run_rate, 2))

    # ---- MATCH STATUS ----
    if win_prob > 70:
        st.success("🔥 Strong winning position")
    elif win_prob > 40:
        st.warning("⚖️ Match is balanced")
    else:
        st.error("📉 Under pressure")

    # ---- GRAPH ----
    fig, ax = plt.subplots()

    ax.bar(["Win", "Lose"], [win_prob, lose_prob])
    ax.set_ylabel("Probability (%)")
    ax.set_title("Winning Chances")

    st.pyplot(fig)