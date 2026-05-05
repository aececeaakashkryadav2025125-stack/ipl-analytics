import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 IPL Analytics Dashboard")

# ---- LOAD DATA ----
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# ---- SECTION 1: MATCHS PER TEAM ----
st.subheader("🏏 Matches Played by Teams")

team_counts = matches['team1'].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(team_counts.index, team_counts.values)
ax1.set_xticklabels(team_counts.index, rotation=45)
ax1.set_ylabel("Matches")

st.pyplot(fig1)

# ---- SECTION 2: TOP SCORING TEAMS ----
st.subheader("🔥 Top Scoring Teams")

team_runs = deliveries.groupby('batting_team')['total_runs'].sum().sort_values(ascending=False).head(6)

fig2, ax2 = plt.subplots()
ax2.bar(team_runs.index, team_runs.values)
ax2.set_xticklabels(team_runs.index, rotation=45)
ax2.set_ylabel("Runs")

st.pyplot(fig2)

# ---- SECTION 3: TOP BATSMEN ----
# ---- SECTION 3: TOP BATSMEN ----
st.subheader("🏆 Top Batsmen")

top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
ax3.bar(top_batsmen.index, top_batsmen.values)
ax3.set_xticklabels(top_batsmen.index, rotation=45)
ax3.set_ylabel("Runs")

st.pyplot(fig3)