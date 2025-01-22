import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

CHAT_MEMORY = ConversationBufferMemory()
# CHAT_MEMORY.chat_memory.add_user_message("Hello!")
# CHAT_MEMORY.chat_memory.add_ai_message("Hi! How can I help you today?")

VALID_FILE_TYPES = ["Site", "Youtube", "PDF", "CSV", "TXT"]

MODELS_CONFIG = {
    "Groq": {
        "models": ["llama-3.3-70b-versatile", "gemma2-9b-it", "mixtral-8x7b-32768"],
        "chat": ChatGroq,
    },
    "OpenAI": {
        "models": ["chatgpt-4o-latest", "gpt-4o-mini", "o1", "o1-mini"],
        "chat": ChatOpenAI,
    },
}


def load_model(provider, model, api_key):
    chat = MODELS_CONFIG[provider]["chat"](model=model, api_key=api_key)
    return chat


def chat_page():
    # st.title('Orakulo')
    st.header("🤖 Welcome to the Orakulo!", divider=True)

    chat_model = st.session_state.get("chat", None)

    # messages = st.session_state.get('messages', [])
    chat_memory = st.session_state.get("chat_memory", CHAT_MEMORY)

    for message in chat_memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)

    user_input = st.chat_input("Talk to me...")

    if user_input:
        chat_memory.chat_memory.add_user_message(user_input)
        response = chat_model.invoke(user_input).content
        chat_memory.chat_memory.add_ai_message(response)
        st.session_state["chat_memory"] = chat_memory
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
            f"Enter the API key for the {provider}",
            value=st.session_state.get(f"api_key_{provider}", ""),
        )

        st.session_state[f"api_key_{provider}"] = api_key

    if st.button("Start Orakulo", use_container_width=True):
        chat = load_model(provider, model, api_key)
        st.session_state["chat"] = chat


def main():
    chat_page()
    with st.sidebar:
        sidebar()


if __name__ == "__main__":
    main()
