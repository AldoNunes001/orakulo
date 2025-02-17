import tempfile

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

import loaders

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


def load_file(file_type, file):
    if file_type == "Site":
        document = loaders.load_site(file)

    elif file_type == "Youtube":
        document = loaders.load_youtube(file)

    elif file_type == "PDF":
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        document = loaders.load_pdf(temp_file_path)

    elif file_type == "CSV":
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        document = loaders.load_csv(temp_file_path)

    elif file_type == "TXT":
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        document = loaders.load_txt(temp_file_path)

    return document


def load_model(provider, model, api_key, file_type, file):
    document = load_file(file_type, file)
    
    # Adicione estas 2 linhas para escapar as chaves
    document = document.replace("{", "{{")
    document = document.replace("}", "}}")

    system_prompt = f"""Você é um assistente amigável chamado Oráculo.
Você possui acesso às seguintes informações vindas de um documento {file_type}:

####
{document}
####

Utilize as informações fornecidas para basear as suas respostas.

Sempre que houver $ na sua saída, substitua por S.

Se a informação do documento for algo como "Just a moment... Enable JavaScript and cookies to continue"
sugira ao usuário carregar novamente o Orakulo!

"""

    template = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("user", "{user_input}"),
        ],
        # template_format="f-string",
    )

    chat = MODELS_CONFIG[provider]["chat"](model=model, api_key=api_key)
    chat_chain = template | chat

    return chat_chain


def chat_page():
    # st.title('Orakulo')
    st.header("🤖 Welcome to the Orakulo!", divider=True)

    chat_model = st.session_state.get("chat", None)

    if chat_model is None:
        st.error("Please load a file, select a model and start the Orakulo.")
        st.stop()

    # messages = st.session_state.get('messages', [])
    chat_memory = st.session_state.get("chat_memory", CHAT_MEMORY)

    for message in chat_memory.buffer_as_messages:
        chat = st.chat_message(message.type)
        chat.markdown(message.content)

    user_input = st.chat_input("Talk to me...")

    if user_input:
        chat = st.chat_message("human")
        chat.markdown(user_input)

        chat = st.chat_message("ai")
        response = chat.write_stream(
            chat_model.stream(
                {
                    "user_input": user_input,
                    "chat_history": chat_memory.buffer_as_messages,
                }
            )
        )

        # response = chat_model.invoke(user_input).content
        chat_memory.chat_memory.add_user_message(user_input)
        chat_memory.chat_memory.add_ai_message(response)
        st.session_state["chat_memory"] = chat_memory
        # st.rerun()


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
        chat = load_model(provider, model, api_key, file_type, file)
        st.session_state["chat"] = chat


def main():
    with st.sidebar:
        sidebar()
    chat_page()


if __name__ == "__main__":
    main()
