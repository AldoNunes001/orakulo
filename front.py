import streamlit as st


MESSAGES_EXAMPLE = [
    ('user', 'Hello!'),
    ('assistant', 'Hello!'),
    ('user', 'How are you?'),
    ('assistant', 'I am fine, thank you!'),
    ('user', 'What is your name?'),
    ('assistant', 'My name is Orakulo!'),
]


def chat_page():
    # st.title('Orakulo')
    st.header('🤖 Welcome to the Orakulo!', divider=True)

    # messages = st.session_state.get('messages', [])
    messages = st.session_state.get('messages', MESSAGES_EXAMPLE)

    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    user_input = st.chat_input('Talk to me...')

    if user_input:
        messages.append(('user', user_input))
        st.session_state.messages = messages
        st.rerun()


def main():
    chat_page()


if __name__ == '__main__':
    main()
