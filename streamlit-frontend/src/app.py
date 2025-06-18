import streamlit as st
import os
from streamlit import sidebar
import urllib.parse
import requests

BACKEND_URL = "http://127.0.0.1:1234/api/chat"


def create_watermark():
    if not st.session_state.get("chat_history"):
        st.markdown(
            """
            <div style="text-align: center; opacity: 0.8; font-size: 30px; padding-top: 100px; padding-bottom: 35px;">
                Explore TechOp Knowledge Graph
            </div>
            """,
            unsafe_allow_html=True,
        )


def handle_user_input(user_input):
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Create the payload for the backend request
    chat_history = [
        {
            "role": msg["role"] if msg["role"] != "bot" else "assistant",
            "content": msg["content"],
        }
        for msg in st.session_state.chat_history
    ]
    payload = {
        "history": chat_history,
        "question": user_input,
        "model": st.session_state.selected_model,
    }

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Assume backend returns {"answer": "..."}
        answer = data.get("answer", "No answer returned.")
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.chat_history.append({"role": "bot", "content": answer})


def create_chat_input():
    with st.form(key="chat_form", clear_on_submit=True, border=False):
        user_input = st.text_area(
            "", key="chat_input", height=100, placeholder="Ask anything"
        )

        col2_1, col2_2, col2_3 = st.columns([4, 2, 1])  # 添加 col2 做间距

        with col2_3:
            submit_button = st.form_submit_button(
                "Send", icon=":material/send:", use_container_width=True
            )


def create_sidebar(clear_chat_callback, model_options, select_model_callback):
    # Sidebar for options
    sidebar.title("Options")
    # Button to clear chat history
    if sidebar.button("Clear Chat History"):
        clear_chat_callback()
    # Dropdown to select model
    selected_model = sidebar.selectbox("Select Model", model_options, index=0)
    select_model_callback(selected_model)


def main():
    # Set the page configuration
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    # Display the Boeing logo at the top
    logo_path = os.path.join(curr_dir, "assets", "boeing_logo.svg")
    round_logo_path = os.path.join(curr_dir, "assets", "boeing_round_logo.png")

    st.set_page_config(page_title="GraphRAG", page_icon=round_logo_path, layout="wide")

    with open(logo_path, "r") as f:
        svg_data = f.read()

    encoded_svg = urllib.parse.quote(svg_data)

    st.markdown(
        f"""
        <div style="display: flex; justify-content: left;">
            <img src="data:image/svg+xml;utf8,{encoded_svg}" width="200"/>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history and selected model in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "GPT-4"
    model_options = ["GPT-4o", "OpenELM"]

    # Define callback to clear chat history
    def clear_chat():
        st.session_state.chat_history = []

    # Define callback to select model
    def select_model(model):
        st.session_state.selected_model = model

    # Create sidebar with options
    create_sidebar(clear_chat, model_options, select_model)

    # Display chat history
    for msg in st.session_state.chat_history:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

    # Display watermark in the center
    create_watermark()

    # Create chat input box at the bottom
    create_chat_input()


if __name__ == "__main__":
    main()
