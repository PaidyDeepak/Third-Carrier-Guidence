import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()
api= st.secrets["general"]["GOOGLE_API_KEY"]
genai.configure(api_key=api)
# Load and resize logo
logo = Image.open("logo.png")
resized_logo = logo.resize((200, 150))  # Adjust width and height as needed

if "history" not in st.session_state:
        st.session_state.history = {}

#dividing the space
col1, col2 = st.columns([5, 1])
c1, c2 = st.columns([5, 1])
co1, co2 = st.columns([5, 1])
#main function
def get_carrier_guidence(prompt):
    try:
        model=genai.GenerativeModel("gemini-1.5-flash")
        response=model.generate_content(prompt)
        st.subheader("Response is generated :")
        return response.text
        
    except Exception as e:
        return f"Error is :{e}"
def history():
    if not st.session_state.history:
        st.error("History is Empty")
    else:
        for q, a in st.session_state.history.items():
            st.markdown("----")
            st.markdown(f"**Question:** {q}  \n→ **Answer:** {a}")
    

#checking the api
if not api:
    with col1:
        st.error(" Google API Key not found. Please set GOOGLE_API_KEY in your .env file.")
        st.info("Get your API key from: https://aistudio.google.com/app/apikey")
        st.stop()
else:
    with col1:
        #center
        st.set_page_config(page_title="Carrier Guidence Assistant",layout="wide")
        st.title("🎓 Generative AI-Powered Carrier Guidance Assistant")
        st.markdown("""Welcome to your personalized carrier advisor.
                    Fill out your background information in the sidebar and ask carrier-related questions below.""")
        
    # Sidebar 
    with col1:
        st.sidebar.image(resized_logo)
        st.sidebar.markdown("---")
        st.sidebar.subheader("👤 Your Profile")
            
        with c1:
            interests=st.sidebar.text_input("Interests",placeholder="Generative AI , Full Stack")
            skills=st.sidebar.text_input("Skills",placeholder="Python ,C++")
            education=st.sidebar.text_input("Higest Education Received",placeholder="B.Tech")
            exp=st.sidebar.text_input("Experience",placeholder="5 years")
                
            if st.sidebar.button("Save",type="primary") :
                if  interests and skills and education and exp :
                    st.sidebar.subheader(":green-background[Saved Successfully!!]")
                else:
                    st.error("Please fill your details in profile !!!!")
            st.sidebar.markdown("---")  
    
    # Main section for questions
    st.markdown("---")
    with col1:
        st.markdown("Suggested Questions:")
        sample_tags = ["How can i become a cloud Engineer with my background and skills ?",
                       "With my profile, what i should do to be successful in Carrier ? ", 
                       " Can i become a cloud engineer With my skills and Education ? ",
                       "What are the highest paiying jobs i can get with my profile ? ",]
        with st.expander("Click to expand"):
            for tag in sample_tags:
                if st.button(tag):
                    st.session_state["tags"] = st.session_state.get("tags", "") + f"{tag}, "
    
    with c1:
        # Text area for user input
        question=st.text_input("Chat with our Bot for your doubts :",placeholder="With my profile what should i do ?",key="tags")
    with co1:
        st.markdown("----")
        st.subheader("Created by Deepak")
        st.markdown("Built using Streamlit and Gemini")
    with c2:
        if st.button("submit"): 
            with c1:
                if not (interests and skills and education and exp):
                    st.error("Please fill your details in profile !!!!")
                elif question:
                    prompt=(
                        f"My interests are {interests}. My skills are {skills} ."
                        f"My educational background is {education} . My experience is {exp} ."
                        f"Heremy question is : {question} ."
                    )
                    with c1:
                        with st.spinner("Generating response..."):
                            result = get_carrier_guidence(prompt)
                        st.markdown(result)
                        if "history" not in st.session_state:
                            st.session_state.history = {}
                        st.session_state.history[question] = result
                        if st.sidebar.button("📖 History",type="tertiary"):
                            history()  
                            st.sidebar.markdown("---")
                                              
                   
