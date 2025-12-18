import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Coder Fix", page_icon="")
st.title(" Pranay AI ")

try:
    # Gemini API configure
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Model select logic
    if "final_model" not in st.session_state:
        available_models = [
            m.name for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]

        if any("gemini-1.5-flash" in m for m in available_models):
            st.session_state.final_model = "gemini-1.5-flash"
        else:
            st.session_state.final_model = (
                available_models[0] if available_models else "gemini-pro"
            )

    model = genai.GenerativeModel(st.session_state.final_model)
    

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input
    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        st.chat_message("user").write(prompt)

        response = model.generate_content(prompt)

        if response.text:
            st.session_state.messages.append(
                {"role": "assistant", "content": response.text}
            )
            st.chat_message("assistant").write(response.text)

except Exception as e:
    st.error(f"Error: {e}")