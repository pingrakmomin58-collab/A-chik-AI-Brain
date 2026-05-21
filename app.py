import streamlit as st
import google.generativeai as genai

# --- APP CONFIGURATION ---
st.set_page_config(page_title="A·chik AI Brain", page_icon="🧠", layout="centered")

# --- DATABASE & MEMORY ---
if "garo_knowledge" not in st.session_state:
    st.session_state.garo_knowledge = "Nok: House, Chii: Water, Sal: Sun, Mikka: Rain"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- LOGIN SYSTEM (ULTRA HACKER PROOF) ---
def login_page():
    st.title("🔐 A·chik AI-ona Rimchaksoa")
    st.write("A·gilsakni bilakbatgipa A·chik AI. Pingrak G Momin-ni tariaha.")
    
    email = st.text_input("Na·ni Email ID-ko sebo:")
    # YAHAN HAI TUMHARA SUPER STRONG PASSWORD
    correct_password = """Abcsdem.o"a"AIaGA:kt,iA2002227ta;a"',25bts3:30;ba",,"""
    
    password = st.text_input("Password (Nokgipasan):", type="password")
    
    if st.button("Napbo (Login)"):
        if email == "kasarasank@gmail.com":
            if password == correct_password:
                st.session_state.role = "Admin"
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Password guala! Access Denied!")
        elif email != "":
            st.session_state.role = "User"
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Kripya Email ID-ko sebo!")

# --- ADMIN PANEL (Pingrak's API Control Room) ---
def admin_panel():
    st.title("👑 Pingrak-ni Control Room")
    st.success("Rimchaksoa Boss! Yahan se AI ka dimaag control karo.")
    
    st.subheader("🔑 AI Engine Connection (API Key)")
    api_key_input = st.text_input("Google Gemini API Key yahan daalein (Free):", type="password")
    if st.button("Connect AI Engine"):
        st.session_state.api_key = api_key_input
        st.success("AI Engine Connected Successfully! 🚀")

    st.subheader("📚 A·chik Katta Skiani (Train AI)")
    new_word = st.text_input("Garo Word = Meaning:")
    if st.button("AI-na Skibo"):
        st.session_state.garo_knowledge += f", {new_word}"
        st.success("Data Saved! AI ab isey yaad rakhega.")
        
    st.write("Current Memory:", st.session_state.garo_knowledge)
        
    if st.button("Ong·katbo (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

# --- USER PANEL (The 2-AI Magic Translator) ---
def user_panel():
    st.title("🤖 A·chik AI Assistant")
    st.caption("Pingrak G Momin ni tariaha.")
    
    if not st.session_state.api_key:
        st.warning("⚠️ AI Engine abhi Admin dwara on nahi kiya gaya hai. Kripya wait karein.")
        if st.button("Ong·katbo (Logout)"):
            st.session_state.logged_in = False
            st.rerun()
        return

    # Set up Gemini AI
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Chat history display
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    user_query = st.chat_input("Sing·ani ba aganani dongama? (Poocho kuch bhi...)")
    
    if user_query:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        # The MAGIC PROMPT (Garo Emotional Translator)
        system_prompt = f"""
        You are an advanced AI Assistant named "A·chik AI Brain" created by Pingrak G Momin from Meghalaya.
        You MUST reply ONLY in the Garo (A·chik Ku·chik) language. 
        Be very polite, use emotional intelligence, and act like a local Garo friend/teacher.
        If the user asks something outside Garo, search your global knowledge, but translate the final answer to fluent Garo.
        Use this local Garo dictionary for reference: {st.session_state.garo_knowledge}.
        User's message: {user_query}
        """

        # Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Chanchienga... (Thinking...)"):
                try:
                    response = model.generate_content(system_prompt)
                    ai_reply = response.text
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    st.error("AI Network error! Check API Key.")

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
