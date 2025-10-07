# import streamlit as st
# import json, random, time
# from datetime import date, datetime, timedelta
# from groq_client import get_llm_response
# import matplotlib.pyplot as plt

# # ----------------------------
# # Load challenges
# # ----------------------------
# with open("challenges.json", "r") as f:
#     challenges = json.load(f)

# # ----------------------------
# # Initialize user session progress
# # ----------------------------
# if "progress" not in st.session_state:
#     st.session_state.progress = {
#         "completed_problems": [],
#         "points": 0,
#         "streak": 0,
#         "last_solved_date": None,
#         "badges": [],
#         "weak_topics": {},
#         "time_spent": {},
#         "xp_level": 1
#     }

# progress = st.session_state.progress

# # ----------------------------
# # App layout
# # ----------------------------
# st.set_page_config(page_title="Ultimate DSA Coach", page_icon="🤖", layout="wide")
# st.title("🤖 Ultimate AI-Powered DSA Coach")

# # ----------------------------
# # User selects language & week
# # ----------------------------
# language = st.selectbox("Choose language:", ["Python", "C++", "Java", "JavaScript"])
# selected_week = st.slider("Select Week", 1, len(challenges["weeks"]), 1)
# week_data = challenges["weeks"][selected_week - 1]

# # ----------------------------
# # Adaptive Problem Selection
# # ----------------------------
# remaining_problems = [p for p in week_data["problems"] if p not in progress["completed_problems"]]
# if not remaining_problems:
#     daily_problem = None
#     st.success("🎉 All problems for this week are completed!")
# else:
#     weak_topic_probs = [p for p in remaining_problems if any(topic in p for topic in progress.get("weak_topics", {}))]
#     daily_problem = random.choice(weak_topic_probs or remaining_problems)
#     st.subheader(f"Week {selected_week}: {', '.join(week_data['topics'])}")
#     st.write(f"**Today's Problem:** {daily_problem}")

# # ----------------------------
# # Step-by-step Hints
# # ----------------------------
# if daily_problem and st.button("Show Hint"):
#     prompt = f"Provide step-by-step hints for '{daily_problem}' without giving full solution, in {language}."
#     with st.spinner("Generating hints..."):
#         hints = get_llm_response(prompt, language)
#     st.subheader("💡 Step-by-Step Hints")
#     st.write(hints)

# # ----------------------------
# # Code Submission & Validation
# # ----------------------------
# user_code = st.text_area("Submit your solution here:")
# start_time = time.time()

# if user_code and st.button("Validate Code"):
#     # Ask LLM to check correctness
#     check_prompt = f"""
# Check if this {language} code correctly solves the problem '{daily_problem}':
# {user_code}
# Respond ONLY with 'Correct' or 'Incorrect' at the start of your message.
# """
#     with st.spinner("Checking correctness..."):
#         check_response = get_llm_response(check_prompt, language)

#     st.subheader("📝 LLM Feedback")
#     st.write(check_response)

#     # Only mark progress if LLM says Correct
#     if check_response.strip().lower().startswith("correct"):
#         # --- Update Progress ---
#         elapsed_min = round((time.time() - start_time)/60,2)
#         progress["completed_problems"].append(daily_problem)
#         progress["points"] += 10
#         progress["time_spent"][daily_problem] = elapsed_min

#         # Update streak
#         today_str = date.today().isoformat()
#         last_date = progress.get("last_solved_date")
#         if last_date:
#             last_dt = datetime.fromisoformat(last_date)
#             if datetime.today().date() - last_dt.date() == timedelta(days=1):
#                 progress["streak"] += 1
#             else:
#                 progress["streak"] = 1
#         else:
#             progress["streak"] = 1
#         progress["last_solved_date"] = today_str

#         # Track weak topics if feedback mentions mistakes
#         if "incorrect" in check_response.lower() or "error" in check_response.lower():
#             for topic in week_data["topics"]:
#                 progress["weak_topics"][topic] = progress["weak_topics"].get(topic,0)+1

#         # Level up system
#         progress["xp_level"] = 1 + progress["points"] // 50

#         # Award badges
#         completed_count = sum(1 for p in week_data["problems"] if p in progress["completed_problems"])
#         if completed_count == len(week_data["problems"]) and f"Week {selected_week} Complete" not in progress["badges"]:
#             progress["badges"].append(f"Week {selected_week} Complete")
#             st.balloons()
#             st.success(f"🏆 Badge earned: Week {selected_week} Complete!")

#         st.success(f"✅ '{daily_problem}' marked as completed!")
#     else:
#         st.warning("❌ Your solution is not correct. Check the hints and try again.")

# # ----------------------------
# # Reset Progress Button
# # ----------------------------
# if st.button("Reset Progress"):
#     st.session_state.progress = {
#         "completed_problems": [],
#         "points": 0,
#         "streak": 0,
#         "last_solved_date": None,
#         "badges": [],
#         "weak_topics": {},
#         "time_spent": {},
#         "xp_level": 1
#     }
#     st.success("✅ Your progress has been reset!")

# # ----------------------------
# # Analytics
# # ----------------------------
# st.subheader("📊 Progress Overview")
# st.write(f"Points: {progress['points']}, XP Level: {progress['xp_level']}")
# st.write(f"Streak: {progress['streak']} days")
# st.write(f"Badges: {', '.join(progress['badges']) if progress['badges'] else 'None'}")

# # Weak Topics Chart
# if progress.get("weak_topics"):
#     st.subheader("⚠️ Weak Topics")
#     st.bar_chart(progress["weak_topics"])

# # Time Spent Chart
# if progress.get("time_spent"):
#     st.subheader("⏱ Time Spent per Problem (minutes)")
#     st.bar_chart(progress["time_spent"])





# import streamlit as st
# import json, random, time, os
# from datetime import date, datetime, timedelta
# from groq_client import get_llm_response

# # ----------------------------
# # Load challenges
# # ----------------------------
# with open("challenges.json", "r") as f:
#     challenges = json.load(f)

# # ----------------------------
# # User login
# # ----------------------------
# st.sidebar.title("Login / Register")
# username = st.sidebar.text_input("Enter your username:")

# if not username:
#     st.warning("Please enter a username to start!")
#     st.stop()

# # Ensure users folder exists
# if not os.path.exists("users"):
#     os.makedirs("users")

# user_file = f"users/{username}.json"

# # Load or initialize user progress
# if os.path.exists(user_file):
#     with open(user_file, "r") as f:
#         progress = json.load(f)
# else:
#     progress = {
#         "completed_problems": [],
#         "points": 0,
#         "streak": 0,
#         "last_solved_date": None,
#         "badges": [],
#         "weak_topics": {},
#         "time_spent": {},
#         "xp_level": 1
#     }

# st.session_state["progress"] = progress

# # ----------------------------
# # App layout
# # ----------------------------
# st.set_page_config(page_title="Ultimate DSA Coach", page_icon="🤖", layout="wide")
# st.title(f"🤖 Ultimate AI-Powered DSA Coach - User: {username}")

# # ----------------------------
# # Language & week selection
# # ----------------------------
# language = st.selectbox("Choose language:", ["Python", "C++", "Java", "JavaScript"])
# selected_week = st.slider("Select Week", 1, len(challenges["weeks"]), 1)
# week_data = challenges["weeks"][selected_week - 1]

# # ----------------------------
# # Adaptive problem selection
# # ----------------------------
# remaining_problems = [p for p in week_data["problems"] if p not in progress["completed_problems"]]
# if not remaining_problems:
#     daily_problem = None
#     st.success("🎉 All problems for this week are completed!")
# else:
#     weak_topic_probs = [p for p in remaining_problems if any(topic in p for topic in progress.get("weak_topics", {}))]
#     daily_problem = random.choice(weak_topic_probs or remaining_problems)
#     st.subheader(f"Week {selected_week}: {', '.join(week_data['topics'])}")
#     st.write(f"**Today's Problem:** {daily_problem}")

# # ----------------------------
# # Step-by-step hints
# # ----------------------------
# if daily_problem and st.button("Show Hint"):
#     prompt = f"Provide step-by-step hints for '{daily_problem}' without giving full solution, in {language}."
#     with st.spinner("Generating hints..."):
#         hints = get_llm_response(prompt, language)
#     st.subheader("💡 Step-by-Step Hints")
#     st.write(hints)

# # ----------------------------
# # Code submission & validation
# # ----------------------------
# user_code = st.text_area("Submit your solution here:")
# start_time = time.time()

# if user_code and st.button("Validate Code"):
#     # Ask LLM to check correctness
#     check_prompt = f"""
# Check if this {language} code correctly solves the problem '{daily_problem}':
# {user_code}
# Respond ONLY with 'Correct' or 'Incorrect' at the start of your message.
# """
#     with st.spinner("Checking correctness..."):
#         check_response = get_llm_response(check_prompt, language)

#     st.subheader("📝 LLM Feedback")
#     st.write(check_response)

#     if check_response.strip().lower().startswith("correct"):
#         # Update progress
#         elapsed_min = round((time.time() - start_time)/60, 2)
#         progress["completed_problems"].append(daily_problem)
#         progress["points"] += 10
#         progress["time_spent"][daily_problem] = elapsed_min

#         # Update streak
#         today_str = date.today().isoformat()
#         last_date = progress.get("last_solved_date")
#         if last_date:
#             last_dt = datetime.fromisoformat(last_date)
#             if datetime.today().date() - last_dt.date() == timedelta(days=1):
#                 progress["streak"] += 1
#             else:
#                 progress["streak"] = 1
#         else:
#             progress["streak"] = 1
#         progress["last_solved_date"] = today_str

#         # Track weak topics if feedback mentions mistakes
#         if "incorrect" in check_response.lower() or "error" in check_response.lower():
#             for topic in week_data["topics"]:
#                 progress["weak_topics"][topic] = progress["weak_topics"].get(topic,0)+1

#         # Level up system
#         progress["xp_level"] = 1 + progress["points"] // 50

#         # Award badges
#         completed_count = sum(1 for p in week_data["problems"] if p in progress["completed_problems"])
#         if completed_count == len(week_data["problems"]) and f"Week {selected_week} Complete" not in progress["badges"]:
#             progress["badges"].append(f"Week {selected_week} Complete")
#             st.balloons()
#             st.success(f"🏆 Badge earned: Week {selected_week} Complete!")

#         # Save progress
#         with open(user_file, "w") as f:
#             json.dump(progress, f, indent=4)

#         st.success(f"✅ '{daily_problem}' marked as completed!")
#     else:
#         st.warning("❌ Your solution is not correct. Check the hints and try again.")

# # ----------------------------
# # Reset progress button
# # ----------------------------
# if st.button("Reset Progress"):
#     progress = {
#         "completed_problems": [],
#         "points": 0,
#         "streak": 0,
#         "last_solved_date": None,
#         "badges": [],
#         "weak_topics": {},
#         "time_spent": {},
#         "xp_level": 1
#     }
#     st.session_state["progress"] = progress
#     with open(user_file, "w") as f:
#         json.dump(progress, f, indent=4)
#     st.success("✅ Your progress has been reset!")

# # ----------------------------
# # Analytics
# # ----------------------------
# st.subheader("📊 Progress Overview")
# st.write(f"Points: {progress['points']}, XP Level: {progress['xp_level']}")
# st.write(f"Streak: {progress['streak']} days")
# st.write(f"Badges: {', '.join(progress['badges']) if progress['badges'] else 'None'}")

# # Weak Topics Chart
# if progress.get("weak_topics"):
#     st.subheader("⚠️ Weak Topics")
#     st.bar_chart(progress["weak_topics"])

# # Time Spent Chart
# if progress.get("time_spent"):
#     st.subheader("⏱ Time Spent per Problem (minutes)")
#     st.bar_chart(progress["time_spent"])



import streamlit as st
import json, random, time, os, hashlib
from datetime import date, datetime, timedelta
from groq_client import get_llm_response

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Ultimate DSA Coach", page_icon="🤖", layout="wide")

# ----------------------------
# Ensure users folder exists
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(BASE_DIR, "users")
if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)

# ----------------------------
# Load challenges file
# ----------------------------
challenges_file = os.path.join(BASE_DIR, "challenges.json")
if not os.path.exists(challenges_file):
    st.error("❌ challenges.json file not found in app directory.")
    st.stop()

with open(challenges_file, "r") as f:
    challenges = json.load(f)

# ----------------------------
# User login / register with password
# ----------------------------
st.sidebar.title("Login / Register")
username = st.sidebar.text_input("Enter your username:")
password = st.sidebar.text_input("Enter your password:", type="password")

if not username or not password:
    st.warning("Please enter both username and password to start!")
    st.stop()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Path to user's file
user_file = os.path.join(USERS_DIR, f"{username}.json")

# Load or register user
if os.path.exists(user_file):
    # Existing user → verify password
    with open(user_file, "r") as f:
        data = json.load(f)
    if data.get("password") == hash_password(password):
        progress = data
        st.success(f"✅ Welcome back, {username}!")
    else:
        st.error("❌ Incorrect password!")
        st.stop()
else:
    # New user → register
    progress = {
        "password": hash_password(password),
        "completed_problems": [],
        "points": 0,
        "streak": 0,
        "last_solved_date": None,
        "badges": [],
        "weak_topics": {},
        "time_spent": {},
        "xp_level": 1
    }
    with open(user_file, "w") as f:
        json.dump(progress, f, indent=4)
    st.success(f"🎉 Account created for {username}!")

# Save in session state
st.session_state["progress"] = progress

# ----------------------------
# Main App Layout
# ----------------------------
st.title(f"🤖 Ultimate AI-Powered DSA Coach - User: {username}")

# ----------------------------
# Language & week selection
# ----------------------------
language = st.selectbox("Choose language:", ["Python", "C++", "Java", "JavaScript"])
selected_week = st.slider("Select Week", 1, len(challenges["weeks"]), 1)
week_data = challenges["weeks"][selected_week - 1]

# ----------------------------
# Adaptive problem selection
# ----------------------------
remaining_problems = [p for p in week_data["problems"] if p not in progress["completed_problems"]]
if not remaining_problems:
    daily_problem = None
    st.success("🎉 All problems for this week are completed!")
else:
    weak_topic_probs = [
        p for p in remaining_problems 
        if any(topic in p for topic in progress.get("weak_topics", {}))
    ]
    daily_problem = random.choice(weak_topic_probs or remaining_problems)
    st.subheader(f"Week {selected_week}: {', '.join(week_data['topics'])}")
    st.write(f"**Today's Problem:** {daily_problem}")

# ----------------------------
# Step-by-step hints
# ----------------------------
if daily_problem and st.button("Show Hint"):
    prompt = f"Provide step-by-step hints for '{daily_problem}' without giving full solution, in {language}."
    with st.spinner("Generating hints..."):
        hints = get_llm_response(prompt, language)
    st.subheader("💡 Step-by-Step Hints")
    st.write(hints)

# ----------------------------
# Code submission & validation
# ----------------------------
user_code = st.text_area("Submit your solution here:")
start_time = time.time()

if user_code and st.button("Validate Code"):
    check_prompt = f"""
Check if this {language} code correctly solves the problem '{daily_problem}':
{user_code}
Respond ONLY with 'Correct' or 'Incorrect' at the start of your message.
"""
    with st.spinner("Checking correctness..."):
        check_response = get_llm_response(check_prompt, language)

    st.subheader("📝 LLM Feedback")
    st.write(check_response)

    if check_response.strip().lower().startswith("correct"):
        # Update progress
        elapsed_min = round((time.time() - start_time) / 60, 2)
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

        # Weak topics tracking
        if "incorrect" in check_response.lower() or "error" in check_response.lower():
            for topic in week_data["topics"]:
                progress["weak_topics"][topic] = progress["weak_topics"].get(topic, 0) + 1

        # Level up system
        progress["xp_level"] = 1 + progress["points"] // 50

        # Award badges
        completed_count = sum(1 for p in week_data["problems"] if p in progress["completed_problems"])
        if completed_count == len(week_data["problems"]) and f"Week {selected_week} Complete" not in progress["badges"]:
            progress["badges"].append(f"Week {selected_week} Complete")
            st.balloons()
            st.success(f"🏆 Badge earned: Week {selected_week} Complete!")

        # Save progress to user file
        with open(user_file, "w") as f:
            json.dump(progress, f, indent=4)

        st.success(f"✅ '{daily_problem}' marked as completed!")
    else:
        st.warning("❌ Your solution is not correct. Check the hints and try again.")

# ----------------------------
# Reset progress
# ----------------------------
if st.button("Reset Progress"):
    progress = {
        "password": progress["password"],  # keep password intact
        "completed_problems": [],
        "points": 0,
        "streak": 0,
        "last_solved_date": None,
        "badges": [],
        "weak_topics": {},
        "time_spent": {},
        "xp_level": 1
    }
    st.session_state["progress"] = progress
    with open(user_file, "w") as f:
        json.dump(progress, f, indent=4)
    st.success("✅ Your progress has been reset!")

# ----------------------------
# Analytics
# ----------------------------
st.subheader("📊 Progress Overview")
st.write(f"Points: {progress['points']}, XP Level: {progress['xp_level']}")
st.write(f"Streak: {progress['streak']} days")
st.write(f"Badges: {', '.join(progress['badges']) if progress['badges'] else 'None'}")

if progress.get("weak_topics"):
    st.subheader("⚠️ Weak Topics")
    st.bar_chart(progress["weak_topics"])

if progress.get("time_spent"):
    st.subheader("⏱ Time Spent per Problem (minutes)")
    st.bar_chart(progress["time_spent"])
