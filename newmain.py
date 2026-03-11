import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# ----------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Career Guidance Assistant",
    layout="wide"
)

api = st.secrets["general"]["GOOGLE_API_KEY"]

genai.configure(api_key=api)

MODEL_NAME = "gemini-2.5-flash"

# ----------------------------------------------------
# SESSION INITIALIZATION
# ----------------------------------------------------

def initialize_session():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "profile" not in st.session_state:
        st.session_state.profile = {}

# ----------------------------------------------------
# LOAD LOGO
# ----------------------------------------------------

def load_logo():

    logo = Image.open("logo.png")
    return logo.resize((200,150))

# ----------------------------------------------------
# SIDEBAR PROFILE
# ----------------------------------------------------

def sidebar_profile(logo):

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
        "Education",
        placeholder="B.Tech"
    )

    experience = st.sidebar.text_input(
        "Experience",
        placeholder="1 year"
    )

    if st.sidebar.button("Save Profile"):

        if interests and skills and education and experience:

            st.session_state.profile = {
                "interests": interests,
                "skills": skills,
                "education": education,
                "experience": experience
            }

            st.sidebar.success("Profile Saved")

        else:
            st.sidebar.error("Please fill all fields")

# ----------------------------------------------------
# BUILD PROMPT
# ----------------------------------------------------

def build_prompt(messages):

    profile = st.session_state.profile

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
    User Profile:
    Interests: {profile.get("interests")}
    Skills: {profile.get("skills")}
    Education: {profile.get("education")}
    Experience: {profile.get("experience")}

    Conversation History:
    {conversation}

    Provide career guidance based on the user's profile and chat history.
    """

    return prompt

# ----------------------------------------------------
# GEMINI RESPONSE
# ----------------------------------------------------

def generate_response(prompt):

    try:

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error: {e}"

# ----------------------------------------------------
# FLOATING CHAT CSS
# ----------------------------------------------------

def floating_chat_css():

    st.markdown(
    """
    <style>

    .chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        height: 500px;
        background: white;
        border-radius: 12px;
        border: 1px solid #ccc;
        padding: 15px;
        overflow-y: auto;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
        z-index: 999;
    }

    </style>
    """,
    unsafe_allow_html=True
    )

# ----------------------------------------------------
# FLOATING CHATBOT
# ----------------------------------------------------

def floating_chatbot():

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    st.markdown("### 🤖 Career AI Assistant")

    for msg in st.session_state.messages:

        role = "🧑 You" if msg["role"] == "user" else "🤖 AI"

        st.markdown(f"**{role}:** {msg['content']}")

    user_input = st.text_input(
        "Type your message",
        key="floating_input"
    )

    if st.button("Send"):

        if not st.session_state.profile:

            st.error("Please save your profile first.")

        elif user_input:

            st.session_state.messages.append(
                {"role":"user","content":user_input}
            )

            prompt = build_prompt(st.session_state.messages)

            with st.spinner("Thinking..."):

                reply = generate_response(prompt)

            st.session_state.messages.append(
                {"role":"assistant","content":reply}
            )

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# HISTORY TAB
# ----------------------------------------------------

def history_tab():

    st.title("📜 Chat History")

    if not st.session_state.messages:

        st.warning("No conversation yet.")

        return

    for msg in st.session_state.messages:

        role = "User" if msg["role"] == "user" else "Assistant"

        st.markdown("---")
        st.markdown(f"**{role}:** {msg['content']}")

# ----------------------------------------------------
# MAIN APP
# ----------------------------------------------------

def main():

    initialize_session()

    logo = load_logo()

    sidebar_profile(logo)

    tab1, tab2 = st.tabs(["Chatbot", "History"])

    with tab1:

        st.title("🎓 Generative AI Career Guidance Assistant")

        st.markdown(
        "Fill your profile in the sidebar and start chatting with the AI assistant."
        )

        floating_chat_css()

        floating_chatbot()

    with tab2:

        history_tab()

# ----------------------------------------------------
# RUN APP
# ----------------------------------------------------

if __name__ == "__main__":

    main()
