import streamlit as st
import main
def load_css():
    with open("static/style.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


# Configuration
st.set_page_config(page_title="WikiPlants", layout="centered")
load_css()
st.markdown('<div class="title">WikiPlants</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tout savoir sur les plantes</div>', unsafe_allow_html=True)
st.markdown("---")


if "bot_response" not in st.session_state:
    st.session_state["bot_response"] = []

if "user_input" not in st.session_state:
    st.session_state["user_input"] = []
    

def handle_submit():
    user_input_text = st.session_state.input_text
    if user_input_text:

        output = user_input_text[::-1]

        st.session_state.user_input.append(user_input_text)
        st.session_state.bot_response.append(output)
        st.session_state.input_text = ""

def response():
    user_input_text = st.session_state.input_text
    if user_input_text:
        output = main.chatbot3(user_input_text)

        st.session_state.user_input.append(user_input_text)
        st.session_state.bot_response.append(output)
        st.session_state.input_text = ""


if st.session_state["bot_response"]:
    chat_messages = ""
    for i in reversed(range(len(st.session_state["bot_response"]))):
        chat_messages += f'<div class="bot-message">{st.session_state["bot_response"][i]}</div>'
        chat_messages += f'<div class="user-message">{st.session_state["user_input"][i]}</div>'
    st.markdown(f'<div class="chat-history">{chat_messages}</div>', unsafe_allow_html=True)


with st.form("form"):
    st.text_input("Vous :", key="input_text", autocomplete=None , placeholder="Posez-moi une question sur une plante")
    st.form_submit_button("Envoyer", on_click=response)
