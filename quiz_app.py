import streamlit as st

# -------------------------------
# 1️⃣ Initialize session state
# -------------------------------
# Streamlit "remembers" these values across page reruns
# current_q = which question we are on (-1 = landing page)
# answers = list to store user's answers
if "current_q" not in st.session_state:
    st.session_state.current_q = -1  # Start at landing page
if "answers" not in st.session_state:
    st.session_state.answers = []

# -------------------------------
# 2️⃣ Define helper functions
# -------------------------------
def start_quiz():
    """
    Start the quiz: set the first question
    and immediately rerun the app to show it.
    """
    st.session_state.current_q = 0
    st.rerun()  # Forces Streamlit to refresh the UI

def restart_quiz():
    """
    Restart the quiz: go back to landing page,
    clear previous answers and per-question selections.
    """
    st.session_state.current_q = -1
    st.session_state.answers = []
    
    # Remove stored selections for each question
    for key in list(st.session_state.keys()):
        if key.startswith("answer_"):
            del st.session_state[key]
    
    st.rerun()  # Refresh UI immediately

# -------------------------------
# 3️⃣ Define the quiz questions
# -------------------------------
# Each question is a dictionary with text, options, and correct answer
questions = [
    {
        "text": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "correct": "Paris"
    },
    {
        "text": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "correct": "Mars"
    },
    {
        "text": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "correct": "12"
    }
]

# -------------------------------
# 4️⃣ Landing Page
# -------------------------------
if st.session_state.current_q == -1:
    st.title("🌟 Welcome to QuizMaster!")
    
    # Display an image for the landing page (replace with your own)
    st.image("assets/quiz_image.png")
    
    st.write("""
    Test your knowledge with this fun quiz!  
    One question at a time. Try your best and see your final score!
    """)
    
    # Start button: when clicked, go to the first question
    if st.button("Start Quiz"):
        start_quiz()

# -------------------------------
# 5️⃣ Quiz Questions
# -------------------------------
elif 0 <= st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]  # Current question
    
    # Show question number and text
    st.subheader(f"Question {st.session_state.current_q + 1}")
    st.write(q["text"])
    
    # Use session state to remember user's selection per question
    key_name = f"answer_{st.session_state.current_q}"
    if key_name not in st.session_state:
        st.session_state[key_name] = q["options"][0]  # Default to first option
    
    # Radio buttons for answer selection
    st.session_state[key_name] = st.radio(
        "Choose your answer:",
        q["options"],
        index=q["options"].index(st.session_state[key_name]),
        key=f"radio_{st.session_state.current_q}"
    )
    
    # Submit button: save the answer and go to next question
    if st.button("Submit", key=f"btn_{st.session_state.current_q}"):
        st.session_state.answers.append(st.session_state[key_name])
        st.session_state.current_q += 1
        st.rerun()  # Show next question immediately

# -------------------------------
# 6️⃣ Results Page
# -------------------------------
else:
    st.header("📊 Quiz Results")
    score = 0  # Initialize score counter
    
    # Show each question, user's answer, and correct answer
    for i, q in enumerate(questions):
        user_ans = st.session_state.answers[i]
        correct_ans = q["correct"]
        
        st.write(f"**Question {i+1}:** {q['text']}")
        if user_ans == correct_ans:
            st.success(f"✅ Your answer: {user_ans} (Correct!)")
            score += 1
        else:
            st.error(f"❌ Your answer: {user_ans} (Correct: {correct_ans})")
        st.write("---")
    
    # Show total score
    st.write(f"### Your Score: {score} / {len(questions)}")
    
    # Give a fun interpretation of the score
    if score == len(questions):
        st.info("🏆 Quiz Master! Perfect score!")
    elif score == 0:
        st.info("😅 No Brainer! Better luck next time.")
    elif score <= len(questions) // 2:
        st.info("🤔 Room to improve. Keep trying!")
    else:
        st.info("👍 Good job! Almost there!")
    
    # Restart button to play again
    if st.button("Restart Quiz"):
        restart_quiz()
