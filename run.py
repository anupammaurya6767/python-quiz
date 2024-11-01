import streamlit as st
from questions_db import quiz_data, generate_mixed_quiz

def initialize_session_state():
    if 'current_score' not in st.session_state:
        st.session_state.current_score = 0
    if 'questions_answered' not in st.session_state:
        st.session_state.questions_answered = 0
    if 'current_week' not in st.session_state:
        st.session_state.current_week = "Select Week"
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'correct_answer_shown' not in st.session_state:
        st.session_state.correct_answer_shown = False
    if 'mixed_quiz_questions' not in st.session_state:
        st.session_state.mixed_quiz_questions = None

def main():
    st.set_page_config(
        page_title="Python Programming Quiz",
        page_icon="🐍",
        layout="wide"
    )

    st.title("Python Programming Quiz 🎓")
    st.markdown("Test your Python knowledge!")

    initialize_session_state()

  
    weeks = ["Select Week", "Mixed Quiz (50 Questions)"] + list(quiz_data.keys())
    week = st.selectbox(
        "Select Quiz Mode:",
        weeks,
        index=weeks.index(st.session_state.current_week)
    )


    if week != st.session_state.current_week:
        st.session_state.current_week = week
        st.session_state.current_question_index = 0
        st.session_state.current_score = 0
        st.session_state.questions_answered = 0
        st.session_state.submitted = False
        st.session_state.correct_answer_shown = False
        if week == "Mixed Quiz (50 Questions)":
            st.session_state.mixed_quiz_questions = generate_mixed_quiz(50)

    if week == "Select Week":
        st.info("Please select a quiz mode to begin!")
        return


    if week == "Mixed Quiz (50 Questions)":
        questions = st.session_state.mixed_quiz_questions
    else:
        questions = quiz_data[week]

    current_question = questions[st.session_state.current_question_index]

    st.markdown(f"### Question {st.session_state.current_question_index + 1} of {len(questions)}")


    if week == "Mixed Quiz (50 Questions)":
        st.markdown(f"*Source: {current_question['source_week']}*")

    st.markdown(f"**{current_question['question']}**")


    if isinstance(current_question["correct_answer"], list):
        answer = st.multiselect(
            "Select all correct answers:",
            current_question["options"],
            disabled=st.session_state.submitted
        )
    else:
        answer = st.radio(
            "Select your answer:",
            current_question["options"],
            disabled=st.session_state.submitted
        )


    if not st.session_state.submitted:
        if st.button("Submit"):
            st.session_state.submitted = True
            st.session_state.questions_answered += 1

            # Check answer
            if isinstance(current_question["correct_answer"], list):
                is_correct = set(answer) == set(current_question["correct_answer"])
            else:
                is_correct = answer == current_question["correct_answer"]

            if is_correct:
                st.session_state.current_score += 1
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect!")


    if st.session_state.submitted:
        if not st.session_state.correct_answer_shown:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Try Again"):
                    st.session_state.submitted = False
            with col2:
                if st.button("Show Correct Answer"):
                    st.session_state.correct_answer_shown = True

        if st.session_state.correct_answer_shown:
            if isinstance(current_question["correct_answer"], list):
                st.info(f"The correct answers are: {', '.join(current_question['correct_answer'])}")
            else:
                st.info(f"The correct answer is: {current_question['correct_answer']}")

        if st.button("Next Question ➡️"):
            if st.session_state.current_question_index < len(questions) - 1:
                st.session_state.current_question_index += 1
                st.session_state.submitted = False
                st.session_state.correct_answer_shown = False
            else:
                st.balloons()
                st.success("🎉 Quiz Completed!")
                final_score = f"Final Score: {st.session_state.current_score}/{st.session_state.questions_answered}"
                st.markdown(f"### {final_score}")

                # Display performance breakdown for mixed quiz
                if week == "Mixed Quiz (50 Questions)":
                    st.markdown("### Performance by Week:")
                    week_performance = {}
                    for q in questions:
                        week = q['source_week']
                        week_performance[week] = week_performance.get(week, {'total': 0, 'correct': 0})
                        week_performance[week]['total'] += 1

                    for week, stats in week_performance.items():
                        percentage = (stats['correct'] / stats['total']) * 100
                        st.markdown(f"- {week}: {stats['correct']}/{stats['total']} ({percentage:.1f}%)")

                if st.button("Restart Quiz"):
                    st.session_state.current_question_index = 0
                    st.session_state.current_score = 0
                    st.session_state.questions_answered = 0
                    st.session_state.submitted = False
                    st.session_state.correct_answer_shown = False
                    if week == "Mixed Quiz (50 Questions)":
                        st.session_state.mixed_quiz_questions = generate_mixed_quiz(50)


    with st.sidebar:
        st.markdown("### Quiz Statistics 📊")
        st.markdown(f"**Current Score:** {st.session_state.current_score}/{st.session_state.questions_answered}")

        if st.session_state.questions_answered > 0:
            accuracy = (st.session_state.current_score/st.session_state.questions_answered) * 100
            st.markdown(f"**Accuracy:** {accuracy:.1f}%")

        # Progress bar
        progress = (st.session_state.current_question_index + 1) / len(questions)
        st.progress(progress)
        st.markdown(f"**Question:** {st.session_state.current_question_index + 1}/{len(questions)}")

if __name__ == "__main__":
    main()
