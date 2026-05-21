import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. APP CONFIGURATION & BLUE THEME (NO WATERMARK) ---
st.set_page_config(page_title="A·chik AI Brain", page_icon="🧠", layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp {
                background-color: #F0F8FF; /* Light Blue Mix */
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 2. PERMANENT MEMORY & SYSTEM STATES ---
if "garo_knowledge" not in st.session_state:
    st.session_state.garo_knowledge = "Nok: House, Chii: Water, Sal: Sun, Mikka: Rain"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "premium_users" not in st.session_state:
    st.session_state.premium_users = []

# --- 3. LOGIN SYSTEM (USER & ADMIN) ---
def login_page():
    st.markdown("<h1 style='text-align: center; color: #00008B;'>🔐 A·chik AI-ona Rimchaksoa</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>The World's Most Powerful Garo AI. Created by Pingrak G Momin.</h4>", unsafe_allow_html=True)
    
    email = st.text_input("Na·ni Email ID-ko sebo (Enter your Email):")
    admin_password = st.text_input("Password (For Admin Only - Users leave blank):", type="password")
    
    if st.button("Napbo (Login)"):
        # Admin Login
        if email == "kasarasank@gmail.com":
            if admin_password == "Abcsdem.o\"a\"AIaGA:kt,iA2002227ta;a\"',25bts3:30;ba\",,":
                st.session_state.role = "Admin"
                st.session_state.email = email
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Password Guala! (Access Denied)")
        # User Login (No Password needed)
        elif email != "":
            st.session_state.role = "User"
            st.session_state.email = email
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Kripya Email ID-ko sebo!")

# --- 4. ADMIN PANEL (The Control Room) ---
def admin_panel():
    st.markdown("<h2 style='color: #00008B;'>👑 Admin Control Room (Pingrak G Momin)</h2>", unsafe_allow_html=True)
    
    # API Engine Setup
    st.subheader("🔑 AI Engine API Key (Gemini)")
    api_key_input = st.text_input("Enter API Key to activate AI:", type="password")
    if st.button("Activate AI Brain"):
        st.session_state.api_key = api_key_input
        st.success("✅ AI Engine Activated Successfully!")

    # PDF & Book Training System (RAG UI)
    st.subheader("📚 A·chik Ki·tap Upload (Train AI & Premium Books)")
    book_name = st.text_input("Book Name (e.g., Dictionary, Agan me·apa):")
    uploaded_pdf = st.file_uploader("Upload PDF File:", type=["pdf"])
    
    if st.button("Save to AI Database"):
        if uploaded_pdf:
            st.success(f"✅ '{book_name}' uploaded! The AI system is processing the text into the offline database.")
            # Advanced Python PDF to Excel parsing logic will connect here.

    # Monetization / Subscription Section
    st.subheader("💳 Subscription & Payment Setup")
    st.write("Upload your QR Code for users to buy Premium Books.")
    qr_upload = st.file_uploader("Upload QR Code Image:", type=["png", "jpg", "jpeg"])
    sub_price = st.text_input("Set Subscription Price (Rs):", value="299")
    
    if st.button("Ong·katbo (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. USER PANEL (The 2-AI Magic Translator) ---
def user_panel():
    st.markdown("<h2 style='color: #00008B;'>🤖 A·chik AI Assistant</h2>", unsafe_allow_html=True)
    
    if not st.session_state.api_key:
        st.warning("⚠️ AI Engine is currently offline. Admin Pingrak is updating the system. Please wait.")
        if st.button("Ong·katbo (Logout)"):
            st.session_state.logged_in = False
            st.rerun()
        return

    # Reminder System (Basic Time Logic)
    current_hour = datetime.datetime.now().hour
    if current_hour >= 22 or current_hour < 5:
        st.info("🌙 Walo tusina somoi ong·jok. Isolko bi·e tusibo. (It is late, time to pray and sleep.)")
    elif current_hour >= 5 and current_hour <= 9:
        st.info("🌅 Pringnam! Poraina somoi ong·jok. (Good morning! Time to study.)")

    # Connect to Gemini AI
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Premium Check
    if st.session_state.email in st.session_state.premium_users:
        st.success("🌟 Premium User: You have access to Agan me·apa & Dictionary books!")
    else:
        st.warning("🔓 Upgrade to Premium to unlock full A·chik Dictionary and Books. Contact Admin.")

    # Chat history display
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    user_query = st.chat_input("Na·a maiko u·ina ska? (Ask me anything...)")
    
    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        # --- THE 2-AI LOGIC (RAG & Translation Prompt) ---
        system_prompt = f"""
        You are 'A·chik AI Brain', the world's most advanced Garo AI, created by Pingrak G Momin.
        You have a 2-step thinking process:
        Step 1: Understand the user's query and find the answer from your vast global knowledge (Science, Math, Philosophy, etc.).
        Step 2: Translate that exact answer into pure, fluent, and emotionally intelligent Garo (A·chik Ku·chik).
        
        RULES:
        - NEVER reply in Roman Hindi. 
        - NEVER explain your 2-step process. Just give the final Garo answer.
        - Be respectful, helpful, and act like a local teacher/friend.
        - Reference Database: {st.session_state.garo_knowledge}
        
        User's question: {user_query}
        """

        with st.chat_message("assistant"):
            with st.spinner("Chanchienga... (Thinking...)"):
                try:
                    response = model.generate_content(system_prompt)
                    ai_reply = response.text
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    st.error("Network Error. Please try again.")

# --- MAIN LOGIC ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.role == "Admin":
            admin_panel()
        else:
            user_panel()

if __name__ == "__main__":
    main()
