from shiny import App, ui, reactive, render, session
from pathlib import Path
# -------------------------------
# 1️⃣ Quiz questions
# -------------------------------
questions = [
    {
        "text": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "correct": "Paris",
    },
    {
        "text": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "correct": "Mars",
    },
    {
        "text": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "correct": "12",
    },
]

# -------------------------------
# 2️⃣ UI
# -------------------------------
app_ui = ui.page_fluid(
    ui.h2("🌟 Welcome to QuizMaster!", style="text-align:center; margin-bottom:20px;"),
    ui.output_ui("main_ui")
)

# -------------------------------
# 3️⃣ Server
# -------------------------------
def server(input, output, session: session.Session):

    current_q = reactive.Value(-1)
    answers = reactive.Value([])

    @output
    @render.ui
    def main_ui():
        # ---------- Landing Page ----------
        if current_q.get() == -1:
            return ui.div(
                ui.div(
                    ui.img(
                        src="quiz_image.png",  # <-- must be in www/
                        style="width:250px; display:block; margin:auto; border-radius:10px;"
                    ),
                    ui.p(
                        "Test your knowledge with this fun quiz! "
                        "One question at a time. Try your best and see your final score!",
                        style="text-align:center; margin-top:15px;"
                    ),
                    ui.div(
                        ui.input_action_button("start_btn", "Start Quiz", class_="btn btn-primary btn-lg"),
                        style="text-align:center; margin-top:20px;"
                    ),
                    class_="card shadow p-4",
                    style="max-width:600px; margin:auto; margin-top:50px; border-radius:15px;"
                )
            )

        # ---------- Quiz Questions ----------
        elif 0 <= current_q.get() < len(questions):
            q_idx = current_q.get()
            q = questions[q_idx]
            prev_selection = q["options"][0]
            if len(answers.get()) > q_idx:
                prev_selection = answers.get()[q_idx]

            return ui.div(
                ui.div(
                    ui.h4(f"Question {q_idx + 1} of {len(questions)}", style="margin-bottom:15px;"),
                    ui.p(q["text"]),
                    ui.input_radio_buttons(
                        f"radio_{q_idx}",
                        "Choose your answer:",
                        choices=q["options"],
                        selected=prev_selection
                    ),
                    ui.input_action_button(f"submit_{q_idx}", "Submit", class_="btn btn-success"),
                    class_="card shadow p-4",
                    style="max-width:600px; margin:auto; margin-top:50px; border-radius:15px;"
                )
            )

        # ---------- Results Page ----------
        else:
            score = sum(
                1 for i, q in enumerate(questions)
                if answers.get()[i] == q["correct"]
            )

            results_ui = [
                ui.h4(f"Your Score: {score} / {len(questions)}", style="text-align:center; margin-bottom:20px;")
            ]

            for i, q in enumerate(questions):
                user_ans = answers.get()[i]
                correct_ans = q["correct"]
                color = "green" if user_ans == correct_ans else "red"
                icon = "✅" if user_ans == correct_ans else "❌"

                results_ui.append(
                    ui.div(
                        ui.p(f"Question {i+1}: {q['text']}"),
                        ui.p(f"{icon} Your answer: {user_ans} (Correct: {correct_ans})", style=f"color:{color}; font-weight:bold;"),
                        class_="card p-3 mb-3 shadow",
                        style="border-radius:10px;"
                    )
                )

            # Fun interpretation
            if score == len(questions):
                results_ui.append(ui.p("🏆 Quiz Master! Perfect score!", style="text-align:center; font-weight:bold;"))
            elif score == 0:
                results_ui.append(ui.p("😅 No Brainer! Better luck next time.", style="text-align:center; font-weight:bold;"))
            elif score <= len(questions) // 2:
                results_ui.append(ui.p("🤔 Room to improve. Keep trying!", style="text-align:center; font-weight:bold;"))
            else:
                results_ui.append(ui.p("👍 Good job! Almost there!", style="text-align:center; font-weight:bold;"))

            # Restart button
            results_ui.append(
                ui.div(
                    ui.input_action_button("restart_btn", "Restart Quiz", class_="btn btn-primary"),
                    style="text-align:center; margin-top:20px;"
                )
            )

            return ui.div(*results_ui, style="max-width:700px; margin:auto; margin-top:30px;")

    # -------------------------------
    # Button observers
    # -------------------------------
    @reactive.Effect
    def start_button_observer():
        if input.start_btn() > 0:
            current_q.set(0)
            answers.set([])

    @reactive.Effect
    def restart_button_observer():
        if input.restart_btn() > 0:
            current_q.set(-1)
            answers.set([])

    @reactive.Effect
    def submit_button_observer():
        q_idx = current_q.get()
        if 0 <= q_idx < len(questions):
            submit_input = getattr(input, f"submit_{q_idx}", None)
            radio_input = getattr(input, f"radio_{q_idx}", None)
            if submit_input is not None and submit_input() > 0:
                # Save selected answer
                new_answers = answers.get().copy()
                if len(new_answers) > q_idx:
                    new_answers[q_idx] = radio_input()
                else:
                    new_answers.append(radio_input())
                answers.set(new_answers)
                # Move to next question
                current_q.set(current_q.get() + 1)

# -------------------------------
# 4️⃣ App
# -------------------------------
www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)

