import streamlit as st
import os
import json
import urllib.parse
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_chat import message


BACKEND_URL = "http://127.0.0.1:1234/api/chat"
CHAT_HISTORY_FILE = "chat_history.json"


def load_all_histories():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_all_histories(histories):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(histories, f, indent=2)


def handle_user_input(user_input):
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input, "image_url": ""}
    )
    chat_history = [
        {
            "role": msg["role"] if msg["role"] != "bot" else "assistant",
            "content": msg["content"],
            "image_url": msg.get("image_url", ""),
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
        print(response.text)  # Debugging line to see the response
        data = response.json()
        answer = data.get("answer", "No answer returned.")
        image_url = data.get("image_url", "")
    except Exception as e:
        answer = f"Error: {e}"
    st.session_state.chat_history.append(
        {"role": "bot", "content": answer, "image_url": image_url}
    )
    # Save the updated chat history
    all_histories = load_all_histories()
    all_histories[st.session_state.current_conversation_id] = (
        st.session_state.chat_history
    )
    save_all_histories(all_histories)
    st.rerun()


def create_watermark():
    if not st.session_state.get("chat_history"):
        st.markdown(
            """
            <div style="text-align: center; opacity: 0.9; font-size: 30px; padding-top: 100px; padding-bottom: 30px;">
                What can I do for you today?
            </div>
            """,
            unsafe_allow_html=True,
        )


def create_chat_input():
    with st.form(key="chat_form", clear_on_submit=True, border=False):
        user_input = st.text_area(
            "", key="chat_input", height=100, placeholder="Ask anything"
        )
        col2_1, col2_2, col2_3 = st.columns([5, 5, 1])
        with col2_3:
            submit_button = st.form_submit_button(
                "", icon=":material/send:", use_container_width=True
            )
    if submit_button and user_input:
        handle_user_input(user_input)


def conversation_page(conversation_id):
    all_histories = load_all_histories()
    chat_history = all_histories.get(conversation_id, [])
    st.session_state.current_conversation_id = conversation_id
    st.session_state.chat_history = chat_history
    # Show the history
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    round_logo_path = os.path.join(curr_dir, "assets", "boeing_round_logo.png")
    user_path = os.path.join(curr_dir, "assets", "user.png")
    st.markdown(
        """
            <div style="text-align: center; opacity: 0.9; font-size: 30px; padding-top: 60px; padding-bottom: 0px;">
            </div>
            """,
        unsafe_allow_html=True,
    )
    conversation_container = st.container()
    with conversation_container:
        for msg in chat_history:
            with st.chat_message(
                "user" if msg["role"] == "user" else "assistant",
                avatar=(user_path if msg["role"] == "user" else round_logo_path),
            ):
                st.markdown(msg["content"])
                if msg["role"] == "bot" and msg["image_url"] != "":
                    st.image(msg["image_url"], use_container_width=True)
    create_watermark()
    create_chat_input()


def make_conversation_page(cid):
    def page():
        conversation_page(cid)

    try:
        dt = datetime.strptime(cid, "%Y%m%d%H%M%S")
        page.__name__ = "Conversation at " + dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        page.__name__ = f"{cid}"
    return page


def select_model(model):
    st.session_state.selected_model = model


def get_next_conversation_id():
    # Use the current Vancouver time to generate a unique ID
    vancouver_time = datetime.now(ZoneInfo("America/Vancouver"))
    return vancouver_time.strftime("%Y%m%d%H%M%S")


def main():

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(curr_dir, "assets", "boeing_logo.svg")
    round_logo_png_path = os.path.join(curr_dir, "assets", "boeing_round_logo.png")
    round_logo_svg_path = os.path.join(curr_dir, "assets", "boeing_round_logo.svg")
    kg_svg_path = os.path.join(curr_dir, "assets", "kg.svg")
    kg_long_svg_path = os.path.join(curr_dir, "assets", "kg_long.svg")

    st.set_page_config(
        page_title="GraphRAG", page_icon=round_logo_png_path, layout="wide"
    )
    st.logo(logo_path, size="large")
    with open(kg_long_svg_path, "r") as f:
        svg_data = f.read()
    encoded_svg = urllib.parse.quote(svg_data)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: left;">
            <img src="data:image/svg+xml;utf8,{encoded_svg}" width="180"/>
            
        </div>
        """,
        unsafe_allow_html=True,
    )
    ## <h5>&nbsp;&nbsp;&nbsp;&nbsp;TechOp Knowledge Graph</h5>

    st.sidebar.markdown("### Chat options")
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "GPT-4o"

    all_histories = load_all_histories()
    conversation_ids = sorted(all_histories.keys(), reverse=True)

    # Create a new chat session if no histories exist
    if not conversation_ids:
        new_id = get_next_conversation_id()
        all_histories[new_id] = []
        save_all_histories(all_histories)
        st.session_state.current_conversation_id = new_id
        st.session_state.chat_history = []
        st.rerun()

    if st.sidebar.button("New chat", icon=":material/edit_square:"):
        new_id = get_next_conversation_id()
        all_histories[new_id] = []
        save_all_histories(all_histories)
        st.session_state.current_conversation_id = new_id
        st.session_state.chat_history = []
        st.rerun()

    if st.sidebar.button("Delete current chat", icon=":material/delete:"):
        cid = st.session_state.get("current_conversation_id")
        if cid and cid in all_histories:
            del all_histories[cid]
            save_all_histories(all_histories)
            remaining = sorted(all_histories.keys(), reverse=True)
            if remaining:
                st.session_state.current_conversation_id = remaining[0]
                st.session_state.chat_history = all_histories[remaining[0]]
            else:
                new_id = get_next_conversation_id()
                all_histories[new_id] = []
                save_all_histories(all_histories)
                st.session_state.current_conversation_id = new_id
                st.session_state.chat_history = []
            st.rerun()

    model_options = ["GPT-4o", "OpenELM"]
    selected_model = st.sidebar.selectbox(
        "Select Model", model_options, key="selected_model"
    )

    # navigation only shows the conversations
    all_histories = load_all_histories()
    conversation_ids = sorted(all_histories.keys(), reverse=True)
    pages = [make_conversation_page(cid) for cid in conversation_ids]

    if pages:
        pg = st.navigation(pages, position="sidebar")
        pg.run()


if __name__ == "__main__":
    main()
