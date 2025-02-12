import streamlit as st

# Title of the app
st.title("Echo Bot with RAG")

# Initializing chat history with session state, session state will enable chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Displaying chat messages from history on app return
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

'''
The values in "role" and "content" are the keys 
in the dictionary of chat_history. Hence, chat_history is a 
dictionary variable.
'''

# Receiving user input
prompt = st.text_input("What's on your mind?")  # Prompt message for user input
if prompt:
    # Displaying the user message/input
    with st.chat_message("user"):
        st.markdown(prompt)
    # Adding the user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Simulating a RAG response (for demonstration purposes)
    # In a real application, this would involve retrieving relevant documents and generating a response
    response = f"Echo: {prompt}"  # Echoing the user message

    # Displaying the bot response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Adding the bot response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
