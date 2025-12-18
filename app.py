import streamlit as st
import google.generativeai as genai

# 1. Page Config (Must be first line of Streamlit code)
st.set_page_config(page_title="Pranay AI", page_icon="🚀")

# 2. API Configuration (Using Streamlit Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key missing! Add GEMINI_API_KEY in Streamlit Cloud Secrets.")
    st.stop()

st.title(" Pranay AI")

# 3. Stable Model Selection (Fixed 404 Error)
# 'models/' prefix hatakar seedha name use karein
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Model Load Error: {e}")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Chat Input logic
if prompt := st.chat_input("Kaise madad karoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Response generation
        with st.spinner("Pranay AI is thinking..."):
            response = model.generate_content(prompt)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.write(response.text)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")