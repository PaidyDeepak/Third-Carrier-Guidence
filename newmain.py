import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Career Guidance Assistant",
    layout="wide"
)

api = st.secrets["general"]["GOOGLE_API_KEY"]

genai.configure(api_key=api)

MODEL_NAME = "gemini-2.5-flash"


# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------

def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "profile_saved" not in st.session_state:
        st.session_state.profile_saved = False


# ---------------------------------------------------
# LOAD LOGO
# ---------------------------------------------------

def load_logo():
    logo = Image.open("logo.png")
    return logo.resize((200,150))


# ---------------------------------------------------
# BUILD USER PROFILE
# ---------------------------------------------------

def user_profile_sidebar(logo):

    st.sidebar.image(logo)

    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Your Profile")

    interests = st.sidebar.text_input(
        "Interests",
        placeholder="Generative AI, Full Stack"
    )

    skills = st.sidebar.text_input(
        "Skills",
        placeholder="Python, C++"
    )

    education = st.sidebar.text_input(
        "Highest Education Received",
        placeholder="B.Tech"
    )

    experience = st.sidebar.text_input(
        "Experience",
        placeholder="5 years"
    )

    if st.sidebar.button("Save Profile", type="primary"):

        if interests and skills and education and experience:

            st.session_state.profile_saved = True
            st.sidebar.success("Profile saved successfully!")

        else:
            st.sidebar.error("Please fill all profile fields")

    return interests, skills, education, experience


# ---------------------------------------------------
# BUILD PROMPT
# ---------------------------------------------------

def build_prompt(interests, skills, education, experience, messages):

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
    User Profile:
    Interests: {interests}
    Skills: {skills}
    Education: {education}
    Experience: {experience}

    Conversation History:
    {conversation}

    Give career guidance based on the profile and conversation.
    """

    return prompt


# ---------------------------------------------------
# GENERATE RESPONSE FROM GEMINI
# ---------------------------------------------------

def generate_response(prompt):

    try:

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error: {e}"


# ---------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------

def display_chat():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# ---------------------------------------------------
# CHATBOT SECTION
# ---------------------------------------------------

def chatbot_ui(interests, skills, education, experience):

    st.title("🎓 AI Career Guidance Assistant")

    st.markdown(
        "Ask career related questions and receive personalized guidance."
    )

    display_chat()

    user_input = st.chat_input("Ask your career question...")

    if user_input:

        if not st.session_state.profile_saved:

            st.error("Please fill and save your profile first.")

            return

        # Save user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        prompt = build_prompt(
            interests,
            skills,
            education,
            experience,
            st.session_state.messages
        )

        with st.spinner("Generating response..."):

            reply = generate_response(prompt)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.markdown(reply)


# ---------------------------------------------------
# HISTORY TAB
# ---------------------------------------------------

def history_tab():

    st.title("📜 Chat History")

    if not st.session_state.messages:

        st.warning("No conversation yet.")

        return

    for msg in st.session_state.messages:

        role = "User" if msg["role"] == "user" else "Assistant"

        st.markdown("---")

        st.markdown(f"**{role}:** {msg['content']}")


# ---------------------------------------------------
# SAMPLE QUESTIONS
# ---------------------------------------------------

def sample_questions():

    st.markdown("### Suggested Questions")

    questions = [
        "How can I become a Cloud Engineer with my background?",
        "What career paths match my skills?",
        "What high paying jobs can I get with my profile?",
        "What skills should I learn next?"
    ]

    for q in questions:

        if st.button(q):

            st.session_state.messages.append(
                {"role":"user","content":q}
            )


# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------

def main():

    initialize_session()

    logo = load_logo()

    interests, skills, education, experience = user_profile_sidebar(logo)

    tab1, tab2 = st.tabs(["Chatbot", "History"])

    with tab1:

        sample_questions()

        chatbot_ui(interests, skills, education, experience)

    with tab2:

        history_tab()


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------

if __name__ == "__main__":

    main()
