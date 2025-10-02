import streamlit as st
import json, random, time
from datetime import date, datetime, timedelta
from groq_client import get_llm_response
import matplotlib.pyplot as plt

# Load challenges
with open("challenges.json", "r") as f:
    challenges = json.load(f)

# Load or initialize progress
try:
    with open("progress.json", "r") as f:
        progress = json.load(f)
except:
    progress = {
        "completed_problems": [],
        "points": 0,
        "streak": 0,
        "last_solved_date": None,
        "badges": [],
        "weak_topics": {},
        "time_spent": {},
        "xp_level": 1
    }

st.set_page_config(page_title="Ultimate DSA Coach", page_icon="🤖", layout="wide")
st.title("🤖 Ultimate AI-Powered DSA Coach")

# --- User selects language & week ---
language = st.selectbox("Choose language:", ["Python", "C++", "Java", "JavaScript"])
selected_week = st.slider("Select Week", 1, len(challenges["weeks"]), 1)
week_data = challenges["weeks"][selected_week - 1]

# --- Adaptive Problem Selection ---
remaining_problems = [p for p in week_data["problems"] if p not in progress["completed_problems"]]
if not remaining_problems:
    daily_problem = None
    st.success("🎉 All problems for this week are completed!")
else:
    # Prioritize weak topics if any
    weak_topic_probs = [p for p in remaining_problems if any(topic in p for topic in progress.get("weak_topics", {}))]
    daily_problem = random.choice(weak_topic_probs or remaining_problems)
    st.subheader(f"Week {selected_week}: {', '.join(week_data['topics'])}")
    st.write(f"**Today's Problem:** {daily_problem}")

# --- Step-by-step Hints ---
if daily_problem and st.button("Show Hint"):
    prompt = f"Provide step-by-step hints for '{daily_problem}' without giving full solution, in {language}."
    with st.spinner("Generating hints..."):
        hints = get_llm_response(prompt, language)
    st.subheader("💡 Step-by-Step Hints")
    st.write(hints)

# --- Code Submission & Validation ---
user_code = st.text_area("Submit your solution here:")
start_time = time.time()

if user_code and st.button("Validate Code"):
    prompt = f"Validate this {language} code for problem '{daily_problem}':\n{user_code}\nCheck correctness, suggest optimizations, and note errors."
    with st.spinner("Validating code..."):
        feedback = get_llm_response(prompt, language)
    st.subheader("📝 Code Review & Feedback")
    st.write(feedback)

    # --- Update Progress ---
    end_time = time.time()
    elapsed_min = round((end_time - start_time)/60,2)
    progress["completed_problems"].append(daily_problem)
    progress["points"] += 10
    progress["time_spent"][daily_problem] = elapsed_min

    # Update streak
    today_str = date.today().isoformat()
    last_date = progress.get("last_solved_date")
    if last_date:
        last_dt = datetime.fromisoformat(last_date)
        if datetime.today().date() - last_dt.date() == timedelta(days=1):
            progress["streak"] += 1
        else:
            progress["streak"] = 1
    else:
        progress["streak"] = 1
    progress["last_solved_date"] = today_str

    # Track weak topics
    if "incorrect" in feedback.lower() or "error" in feedback.lower():
        for topic in week_data["topics"]:
            progress["weak_topics"][topic] = progress["weak_topics"].get(topic,0)+1

    # Level up system
    progress["xp_level"] = 1 + progress["points"] // 50

    # Award badges
    completed_count = sum(1 for p in week_data["problems"] if p in progress["completed_problems"])
    if completed_count == len(week_data["problems"]) and f"Week {selected_week} Complete" not in progress["badges"]:
        progress["badges"].append(f"Week {selected_week} Complete")
        st.balloons()
        st.success(f"🏆 Badge earned: Week {selected_week} Complete!")

    # Save progress
    with open("progress.json","w") as f:
        json.dump(progress,f,indent=4)
    st.success(f"✅ '{daily_problem}' marked as completed!")

# --- Analytics ---
st.subheader("📊 Progress Overview")
st.write(f"Points: {progress['points']}, XP Level: {progress['xp_level']}")
st.write(f"Streak: {progress['streak']} days")
st.write(f"Badges: {', '.join(progress['badges']) if progress['badges'] else 'None'}")

# Weak Topics Chart
if progress.get("weak_topics"):
    st.subheader("⚠️ Weak Topics")
    st.bar_chart(progress["weak_topics"])

# Time Spent Chart
if progress.get("time_spent"):
    st.subheader("⏱ Time Spent per Problem (minutes)")
    st.bar_chart(progress["time_spent"])
