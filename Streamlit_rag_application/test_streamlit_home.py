import streamlit as st
from dotenv import load_dotenv

def css():
  css = '''
  <style>
  .chat-message {
      padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
  }
  .chat-message.user {
      background-color: #2b313e
  }
  .chat-message.bot {
      background-color: #475063
  }
  .chat-message .avatar {
    width: 20%;
  }
  .chat-message .avatar img {
     max-width: 78px;
     max-height: 78px;
     border-radius: 50%;
     object-fit: cover;
  }
  .chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
  }
'''

def bot_template():
  bot_template = '''
  <div class="chat-message bot">
      <div class="avatar">
          <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
      </div>
      <div class="message">{{MSG}}</div>
  </div>
'''

def user_template():
  user_template = """
  <div class="chat-message user">
      <div class="avatar">
          <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
      </div>
      <div class="message">{{MSG}}</div>
  </div>
  """

def handle_userinput(user_question):
    response = st.session_state.conversation({'chat_history':user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Streamlit RAG Application",
                       page_icon=":computer:")  # Page title and icon
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Streamlit RAG Application :computer:")  # Header of the app
    user_question = st.text_input("what's on your mind ?")
    if user_question:
        handle_userinput(user_question)


if __name__ == '__main__':
    main()