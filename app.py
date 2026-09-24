import streamlit as st

from diet import (
    bmi_calculator,
    bmi_category,
    bmr_calculator,
    tdee_calculator,
    calorie_target,
    protein_target
)

from rag import search_knowledge
from api import ask_llm


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏋️",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# TITLE
# =========================================================

st.title("AI Health Assistant")

st.write(
    "Personalized wellness assistant powered by "
    "GPT-OSS-120B + RAG."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Your Health Profile")


gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)


age = st.sidebar.slider(
    "Age",
    min_value=10,
    max_value=100,
    value=25
)


weight = st.sidebar.slider(
    "Weight (kg)",
    min_value=30,
    max_value=200,
    value=70
)


height = st.sidebar.slider(
    "Height (cm)",
    min_value=100,
    max_value=250,
    value=170
)


activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active",
        "Extra Active"
    ]
)


goal = st.sidebar.selectbox(
    "Your Goal",
    [
        "Lose Weight",
        "Maintain Weight",
        "Gain Weight"
    ]
)


# =========================================================
# CALCULATIONS
# =========================================================

bmi = bmi_calculator(
    weight,
    height
)


bmi_status = bmi_category(
    bmi
)


bmr = bmr_calculator(
    gender,
    age,
    weight,
    height
)


tdee = tdee_calculator(
    bmr,
    activity
)


calories = calorie_target(
    tdee,
    goal
)


protein = protein_target(
    weight,
    goal
)


# =========================================================
# HEALTH DASHBOARD
# =========================================================

st.header("Health Dashboard")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "BMI",
    bmi
)


col2.metric(
    "BMR",
    f"{bmr:.0f} kcal"
)


col3.metric(
    "TDEE",
    f"{tdee:.0f} kcal"
)


col4.metric(
    "Daily Calories",
    f"{calories:.0f} kcal"
)


st.info(
    f"**BMI Category:** {bmi_status}  \n"
    f"**Estimated Protein Target:** {protein} g/day"
)


# =========================================================
# PROFILE SUMMARY
# =========================================================

with st.expander("View Health Profile"):

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.write(f"**Gender:** {gender}")
        st.write(f"**Age:** {age}")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Height:** {height} cm")

    with profile_col2:

        st.write(f"**Activity:** {activity}")
        st.write(f"**Goal:** {goal}")
        st.write(f"**BMI:** {bmi}")
        st.write(f"**Protein Target:** {protein} g")


# =========================================================
# AI ASSISTANT
# =========================================================

st.divider()

st.header("AI Nutrition Assistant")


st.caption(
    "Ask questions about nutrition, protein, calories, "
    "vegetarian foods, meal planning and wellness."
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_question = st.chat_input(
    "Ask your health or nutrition question..."
)


if user_question:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    with st.chat_message("user"):

        st.markdown(user_question)


    # -----------------------------------------------------
    # RAG SEARCH
    # -----------------------------------------------------

    with st.spinner(
        "Searching nutrition knowledge..."
    ):

        try:

            documents = search_knowledge(
                user_question,
                k=4
            )

            context = "\n\n".join(
                [
                    doc.page_content
                    for doc in documents
                ]
            )

        except Exception as e:

            context = ""

            st.warning(
                f"Knowledge base unavailable: {e}"
            )


    # -----------------------------------------------------
    # SYSTEM PROMPT
    # -----------------------------------------------------

    system_prompt = f"""
You are an AI Health and Nutrition Assistant.

Your job is to provide general wellness and nutrition
information using the user's profile and the provided
knowledge-base context.

IMPORTANT RULES:

1. Do not diagnose diseases.
2. Do not prescribe medication.
3. Do not claim to replace a doctor or dietitian.
4. If the user describes serious or emergency symptoms,
   recommend appropriate professional medical care.
5. Do not invent facts from the knowledge base.
6. If the knowledge base does not contain the answer,
   clearly say that the information is not available
   in the provided knowledge base.
7. Give practical, easy-to-understand answers.
8. Consider the user's goal and profile.
9. Distinguish estimates from medically established facts.
10. Do not make extreme diet recommendations.

USER PROFILE:

Gender: {gender}
Age: {age}
Weight: {weight} kg
Height: {height} cm
Activity Level: {activity}
Goal: {goal}

CALCULATED VALUES:

BMI: {bmi}
BMI Category: {bmi_status}
BMR: {bmr} kcal/day
TDEE: {tdee} kcal/day
Estimated Daily Calories: {calories} kcal/day
Estimated Protein Target: {protein} g/day


KNOWLEDGE BASE CONTEXT:

{context}
"""


    # -----------------------------------------------------
    # BUILD LLM MESSAGES
    # -----------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # Keep recent conversation
    messages.extend(
        st.session_state.messages[-10:]
    )


    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "AI is preparing your answer..."
        ):

            try:

                answer = ask_llm(
                    messages
                )

            except Exception as e:

                answer = (
                    "Sorry, AI response generate "
                    f"nahi ho saka.\n\nError: {e}"
                )

        st.markdown(answer)


    # -----------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "This application provides general wellness and "
    "nutrition information and is not a substitute for "
    "professional medical advice."
)