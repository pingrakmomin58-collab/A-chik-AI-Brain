import streamlit as st
import google.generativeai as genai
import sqlite3
import PyPDF2

# --- APP CONFIGURATION ---
st.set_page_config(page_title="A·chik AI Brain", page_icon="🧠", layout="wide")

# --- DATABASE SETUP (PERMANENT STORAGE) ---
# Ye database ek file banayega jo kabhi delete nahi hogi
conn = sqlite3.connect('garo_brain.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS api_keys (id INTEGER PRIMARY KEY, key TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS dictionary (word TEXT PRIMARY KEY, meaning TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS pdf_memory (filename TEXT PRIMARY KEY, text_content TEXT)')
conn.commit()

# --- HELPER FUNCTIONS (Save & Load Data) ---
def save_api_key(key):
    c.execute("DELETE FROM api_keys") # Puraani key delete
    c.execute("INSERT INTO api_keys (key) VALUES (?)", (key,))
    conn.commit()

def get_api_key():
    c.execute("SELECT key FROM api_keys")
    result = c.fetchone()
    return result[0] if result else ""

def save_word(word, meaning):
    c.execute("REPLACE INTO dictionary (word, meaning) VALUES (?, ?)", (word, meaning))
    conn.commit()

def save_pdf_text(filename, text):
    c.execute("REPLACE INTO pdf_memory (filename, text_content) VALUES (?, ?)", (filename, text))
    conn.commit()

def get_all_knowledge():
    c.execute("SELECT word, meaning FROM dictionary")
    dict_data = ", ".join([f"{row[0]}: {row[1]}" for row in c.fetchall()])
    
    c.execute("SELECT text_content FROM pdf_memory")
    pdf_data = "\n".join([row[0] for row in c.fetchall()])
    
    return f"DICTIONARY: {dict_data}\n\nPDF BOOKS DATA: {pdf_data}"

# --- LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = "User"

def login_page():
    st.title("🔐 A·chik AI Login")
    email = st.text_input("Email ID:")
    password = st.text_input("Password (Admin Only):", type="password")
    
    if st.button("Login"):
        if email == "kasarasank@gmail.com" and password == "Abcsdem.o\"a\"AIaGA:kt,iA2002227ta;a\"',25bts3:30;ba\",,":
            st.session_state.role = "Admin"
            st.session_state.logged_in = True
            st.rerun()
        elif email != "" and password == "":
            st.session_state.role = "User"
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Credentials!")

# --- CHATBOT LOGIC (Used by Admin & User) ---
def ai_chat_interface():
    st.subheader("💬 Chat with A·chik AI")
    api_key = get_api_key()
    
    if not api_key:
        st.warning("⚠️ API Key is missing. Admin needs to set it up.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Sawal poocho (Ask something)...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Fetching ALL permanent data (Dictionary + PDFs)
        knowledge_base = get_all_knowledge()
        
        system_prompt = f"""
        You are a Garo AI Assistant created by Pingrak G Momin.
        Reply ONLY in Garo (A·chik) language. Be polite.
        Use this knowledge base to answer:
        {knowledge_base}
        User's Question: {user_input}
        """

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(system_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("API Error. Check Key or Internet.")

# --- ADMIN PANEL ---
def admin_panel():
    st.title("⚙️ Admin Control Room (Permanent Storage)")
    
    st.write("---")
    # API KEY SECTION (Permanent)
    st.subheader("1. API Key Setup")
    current_key = get_api_key()
    if current_key:
        st.success("API Key is saved in database.")
    
    new_key = st.text_input("Enter New API Key (Gemini):", type="password")
    if st.button("Save API Key"):
        save_api_key(new_key)
        st.success("API Key Permanently Saved!")
        st.rerun()

    st.write("---")
    # PDF UPLOAD SECTION (Real Scanning)
    st.subheader("2. Upload PDF Books (Machine Learning)")
    pdf_file = st.file_uploader("Upload Garo Book (PDF)", type=["pdf"])
    if st.button("Scan & Extract Text"):
        if pdf_file:
            with st.spinner("Extracting text from PDF..."):
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                extracted_text = ""
                for page in range(len(pdf_reader.pages)):
                    extracted_text += pdf_reader.pages[page].extract_text()
                
                # Save to Database
                save_pdf_text(pdf_file.name, extracted_text)
                st.success(f"PDF '{pdf_file.name}' permanently saved to AI Brain!")
        else:
            st.error("Please select a PDF first.")

    st.write("---")
    # ADMIN TESTING CHAT
    st.subheader("3. Admin Testing Room")
    st.info("Test the AI here before users see it.")
    ai_chat_interface()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- USER PANEL ---
def user_panel():
    st.title("🤖 A·chik AI Assistant")
    st.caption("Created by Pingrak G Momin")
    ai_chat_interface()
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- MAIN RUNNER ---
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "Admin":
        admin_panel()
    else:
        user_panel()
