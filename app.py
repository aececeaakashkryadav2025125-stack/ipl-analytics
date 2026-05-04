import streamlit as st
import pandas as pd
import pickle

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

    # calculate features
    runs_left = target - current_score
    balls_left_safe = max(balls_left, 1)

    required_run_rate = (runs_left * 6) / balls_left_safe

    # create dataframe
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'current_score': [current_score],
        'runs_left': [runs_left],
        'required_run_rate': [required_run_rate]
    })

    # predict
    result = model.predict_proba(input_df)[0]

    win_prob = round(result[1] * 100, 2)
    lose_prob = round(result[0] * 100, 2)

    # output
    st.success(f"Winning Probability: {win_prob}%")
    st.info(f"Losing Probability: {lose_prob}%")
