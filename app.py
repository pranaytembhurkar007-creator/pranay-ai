import streamlit as st
import google.generativeai as genai
# import os  <-- Iski zaroorat nahi hai agar hum st.secrets use karein

# 1. Page Config sabse pehle hona chahiye
st.set_page_config(page_title="AI Coder Fix", page_icon="")
st.title(" Pranay AI")

# 2. API Configuration (Sirf ek tarika use karein)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ API Key not found! Go to Settings > Secrets and add GEMINI_API_KEY")
    st.stop()

try:
    # 3. Model Select Logic (Simplified)
    if "final_model" not in st.session_state:
        st.session_state.final_model = "gemini-1.5-flash"

    model = genai.GenerativeModel(st.session_state.final_model)
    st.sidebar.success(f"Connected to: {st.session_state.final_model}")

    # 4. Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 5. User Input
    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
            if response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.chat_message("assistant").write(response.text)

except Exception as e:
    st.error(f"Error: {e}")