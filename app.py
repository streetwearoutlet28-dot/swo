import streamlit as st
import google.generativeai as genai

# --- Configurare Pagină ---
st.set_page_config(page_title="Asistent Streetwear", page_icon="👟")
st.title("Asistent Streetwear Outlet")

# --- Verificare API Key ---
# Verificăm dacă cheia există în secretele Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Cheia API nu a fost găsită. Te rog configureaz-o în Streamlit Secrets.")
    st.stop()

# --- Configurare AI ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Gestionare Istoric Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afișare mesaje anterioare
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input Utilizator ---
if prompt := st.chat_input("Cu ce te pot ajuta astăzi?"):
    # 1. Afișează mesajul utilizatorului
    with st.chat_message("user"):
        st.markdown(prompt)
    # Salvăm în istoric
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Obține răspunsul de la AI
    try:
        with st.spinner('Mă gândesc...'):
            response = model.generate_content(prompt)
            text_response = response.text
            
        # 3. Afișează răspunsul AI
        with st.chat_message("assistant"):
            st.markdown(text_response)
        # Salvăm în istoric
        st.session_state.messages.append({"role": "assistant", "content": text_response})
        
    except Exception as e:
        st.error(f"A apărut o eroare: {e}")
