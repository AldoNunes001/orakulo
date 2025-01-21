import streamlit as st


MESSAGES_EXAMPLE = [
    ("user", "Hello!"),
    ("assistant", "Hello!"),
    ("user", "How are you?"),
    ("assistant", "I am fine, thank you!"),
    ("user", "What is your name?"),
    ("assistant", "My name is Orakulo!"),
]

VALID_FILE_TYPES = ["Site", "Youtube", "PDF", "CSV", "TXT"]

MODELS_CONFIG = {
    "Groq": {
        "models": ["llama-3.3-70b-versatile", "gemma2-9b-it", "mixtral-8x7b-32768"]
    },
    "OpenAI": {"models": ["chatgpt-4o-latest", "gpt-4o-mini", "o1", "o1-mini"]},
}


def chat_page():
    # st.title('Orakulo')
    st.header("🤖 Welcome to the Orakulo!", divider=True)

    # messages = st.session_state.get('messages', [])
    messages = st.session_state.get("messages", MESSAGES_EXAMPLE)

    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    user_input = st.chat_input("Talk to me...")

    if user_input:
        messages.append(("user", user_input))
        st.session_state.messages = messages
        st.rerun()


def sidebar():
    tabs = st.tabs(["File Upload", "Model Selection"])

    with tabs[0]:
        file_type = st.selectbox("Select file type", VALID_FILE_TYPES)

        if file_type == "Site":
            file = st.text_input("Enter the URL of the site")
        elif file_type == "Youtube":
            file = st.text_input("Enter the URL of the video")
        elif file_type == "PDF":
            file = st.file_uploader("Upload a PDF file", type="pdf")
        elif file_type == "CSV":
            file = st.file_uploader("Upload a CSV file", type="csv")
        elif file_type == "TXT":
            file = st.file_uploader("Upload a TXT file", type="txt")

    with tabs[1]:
        provider = st.selectbox("Select the model provider", MODELS_CONFIG.keys())
        model = st.selectbox("Select the model", MODELS_CONFIG[provider]["models"])
        api_key = st.text_input(
            "Enter the API key", value=st.session_state.get(f"api_key_{provider}", "")
        )

        st.session_state[f"api_key_{provider}"] = api_key


def main():
    chat_page()
    with st.sidebar:
        sidebar()


if __name__ == "__main__":
    main()
