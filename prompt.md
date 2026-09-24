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
# SIDEBAR - HEALTH PROFILE
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


diet_type = st.sidebar.selectbox(
    "Diet Type",
    [
        "Vegetarian",
        "Non-Vegetarian",
        "Vegan"
    ]
)


allergies = st.sidebar.text_area(
    "Food Allergies",
    "",
    placeholder="Example: peanuts, milk, soy"
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
        st.write(f"**Diet Type:** {diet_type}")

        st.write(
            f"**Food Allergies:** "
            f"{allergies if allergies else 'None reported'}"
        )

        st.write(f"**BMI:** {bmi}")
        st.write(f"**Protein Target:** {protein} g/day")


# =========================================================
# AI FEATURES
# =========================================================

st.divider()


tab1, tab2 = st.tabs(
    [
        "🍽️ Diet Recommendations",
        "🤖 AI Health Assistant"
    ]
)


# =========================================================
# TAB 1 - DIET RECOMMENDATION
# =========================================================

with tab1:

    st.header("Personalized Diet Recommendation")

    st.write(
        "Generate a simple one-day diet plan based on "
        "your health profile, diet type, goal and allergies."
    )


    if st.button(
        "Get Diet Recommendations",
        type="primary"
    ):

        # -------------------------------------------------
        # RAG SEARCH
        # -------------------------------------------------

        with st.spinner(
            "Searching nutrition knowledge..."
        ):

            try:

                search_query = f"""
Diet type: {diet_type}

Goal: {goal}

Food allergies:
{allergies if allergies else "None reported"}

Find useful nutrition information about:

healthy foods,
protein sources,
calories,
breakfast,
morning snacks,
lunch,
evening snacks,
dinner,
meal planning.
"""

                documents = search_knowledge(
                    search_query,
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


        # -------------------------------------------------
        # DIET RECOMMENDATION PROMPT
        # -------------------------------------------------

        diet_prompt = f"""
You are a helpful AI nutrition assistant.

Use the following nutrition knowledge to create
a simple one-day diet plan.

NUTRITION KNOWLEDGE:

{context}


USER INFORMATION:

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

Activity Level: {activity}

Goal: {goal}

Diet Type: {diet_type}

Food Allergy:
{allergies if allergies else "None reported"}

Estimated BMI: {bmi}

BMI Category: {bmi_status}

Estimated BMR: {bmr} kcal/day

Estimated TDEE: {tdee} kcal/day

Estimated Daily Calorie Target:
{calories} kcal/day

Estimated Protein Target:
{protein} g/day


CREATE THE FOLLOWING:

1. Breakfast

2. Morning Snack

3. Lunch

4. Evening Snack

5. Dinner


FOR EVERY MEAL PROVIDE:

- Food
- Portion
- Approximate calories
- Approximate protein


IMPORTANT RULES:

1. Respect the user's diet type.

2. Do not recommend foods containing
   the stated allergy.

3. If the allergy information is unclear,
   do not assume that a food is safe.

4. For packaged or processed foods,
   advise checking the ingredient label
   when allergens may be present.

5. Use the provided nutrition knowledge
   when possible.

6. Keep the plan simple and practical.

7. Calorie and protein values are estimates.

8. Do not diagnose diseases.

9. Do not prescribe medicines.

10. Do not claim to cure diseases.

11. Do not claim that this plan is a
    medical prescription.

12. This is general wellness information,
    not medical advice.

13. Do not invent information from the
    provided knowledge base.

14. If the knowledge base does not contain
    useful information for a recommendation,
    clearly identify the recommendation
    as a general estimate.

15. If the user has a serious allergy or
    medical condition, recommend consulting
    a qualified healthcare professional.
"""


        # -------------------------------------------------
        # LLM MESSAGES
        # -------------------------------------------------

        diet_messages = [
            {
                "role": "system",
                "content": diet_prompt
            },
            {
                "role": "user",
                "content": (
                    "Create my personalized "
                    "one-day diet plan."
                )
            }
        ]


        # -------------------------------------------------
        # GENERATE DIET PLAN
        # -------------------------------------------------

        with st.spinner(
            "AI is creating your personalized diet plan..."
        ):

            try:

                diet_answer = ask_llm(
                    diet_messages
                )

                st.success(
                    "Personalized diet plan generated."
                )

                st.markdown(
                    diet_answer
                )

            except Exception as e:

                st.error(
                    "Diet recommendation generate "
                    f"nahi ho saki.\n\nError: {e}"
                )


# =========================================================
# TAB 2 - AI HEALTH ASSISTANT
# =========================================================

with tab2:

    st.header("AI Nutrition Assistant")

    st.caption(
        "Ask questions about nutrition, protein, calories, "
        "vegetarian foods, meal planning and wellness."
    )


    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    user_question = st.chat_input(
        "Ask your health or nutrition question..."
    )


    if user_question:

        # -------------------------------------------------
        # DISPLAY USER MESSAGE
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )


        with st.chat_message("user"):

            st.markdown(
                user_question
            )


        # -------------------------------------------------
        # RAG SEARCH
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CHATBOT PROMPT
        # -------------------------------------------------

        system_prompt = f"""
You are an AI health and nutrition assistant.

Use the following knowledge to answer
the user's question.

NUTRITION KNOWLEDGE:

{context}


USER INFORMATION:

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

Activity Level: {activity}

Goal: {goal}

Diet Type: {diet_type}

Food Allergy:
{allergies if allergies else "None reported"}

Estimated BMI: {bmi}

Estimated BMR: {bmr} kcal/day

Estimated TDEE: {tdee} kcal/day

Estimated Daily Calorie Target:
{calories} kcal/day

Estimated Protein Target:
{protein} g/day


USER QUESTION:

{user_question}


INSTRUCTIONS:

1. Answer clearly.

2. Keep the explanation beginner-friendly.

3. Use the provided nutrition knowledge
   when possible.

4. Do not invent medical facts.

5. Do not invent information from
   the knowledge base.

6. Do not diagnose diseases.

7. Do not prescribe medicines.

8. Do not claim to cure diseases.

9. Respect the user's diet type.

10. Do not recommend foods containing
    a stated food allergy.

11. If the allergy information is unclear,
    do not assume that a food is safe.

12. Treat BMI, BMR, TDEE, calorie and
    protein values as estimates.

13. If the question concerns a serious
    medical problem, recommend consulting
    a qualified healthcare professional.

14. If the knowledge base does not contain
    enough information to answer confidently,
    say so instead of inventing an answer.

15. This application provides general health
    and nutrition information for educational
    and wellness purposes.

16. This is not a substitute for professional
    medical advice.
"""


        # -------------------------------------------------
        # BUILD MESSAGES
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CALL LLM
        # -------------------------------------------------

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

            st.markdown(
                answer
            )


        # -------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # -------------------------------------------------

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