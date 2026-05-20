import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(page_title="A·chik AI Brain", page_icon="🧠", layout="centered")

# --- DATABASE MOCKUP (Offline Storage System) ---
if "garo_knowledge" not in st.session_state:
    st.session_state.garo_knowledge = {
        "Nok": "House / Ghar",
        "Chii": "Water / Pani",
        "A.a": "Earth / Mitti"
    }

# --- LOGIN SYSTEM ---
def login_page():
    st.title("🔐 Login to A·chik AI")
    st.write("Duniya ke sabse powerful Garo AI mein aapka swagat hai.")
    
    email = st.text_input("Apna Email id likhein:")
    
    if st.button("Login"):
        if email == "pingrak@owner.com":  
            st.session_state.role = "Admin"
            st.session_state.logged_in = True
            st.rerun()
        elif email != "":
            st.session_state.role = "User"
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Kripya email id dalein!")

# --- ADMIN PANEL (Pingrak's Control Room) ---
def admin_panel():
    st.title("👑 Owner Control Room (Pingrak G Momin)")
    st.success("Welcome Boss! Aapka AI Training mode on hai.")
    
    st.subheader("📚 Train the AI (Upload PDF or Book)")
    uploaded_file = st.file_uploader("Yahan Garo Book/PDF upload karein", type=["pdf", "txt", "csv"])
    
    if uploaded_file is not None:
        st.info(f"File '{uploaded_file.name}' successfully upload ho gayi! AI ab isey padh raha hai...")
        
    st.subheader("⚡ Quick Train (Manual Data Entry)")
    col1, col2 = st.columns(2)
    with col1:
        new_garo_word = st.text_input("New Garo Word:")
    with col2:
        new_meaning = st.text_input("Meaning in English/Hindi:")
        
    if st.button("AI ko Sikhao (Update Brain)"):
        if new_garo_word and new_meaning:
            st.session_state.garo_knowledge[new_garo_word] = new_meaning
            st.success(f"Naya word '{new_garo_word}' AI ke dimaag mein save ho gaya! (Offline)")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- USER PANEL (Garo AI Chat for Public) ---
def user_panel():
    st.title("🤖 A·chik AI Assistant")
    st.write("Hello! Anga Pingrak ni tariaha Garo AI ong.a. Sing.bo! (Mujhse kuch bhi poocho)")
    
    user_query = st.text_input("Garo word likhein (e.g., Nok, Chii):")
    
    if st.button("Jawab Do (Search)"):
        if user_query in st.session_state.garo_knowledge:
            st.success(f"🧠 AI Reply: '{user_query}' ni ortoara '{st.session_state.garo_knowledge[user_query]}' ong.a! Nambatgipa sing.ani.")
        else:
            st.warning("Kema ka.bo, angni skigipa (Pingrak) angna iani gimin skikuja. Admin isey jaldi update karenge!")
            
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- MAIN APP LOGIC ---
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
