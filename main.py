import streamlit as st
from rag_model import create_rag_chain

st.set_page_config(page_title="PyAssistant", page_icon="assets/py_ass_logo.png")                    

st.title("PyAssistant")
st.write("AI-powered beginners guide to learn Python programming.")

@st.cache_resource
def get_rag_chain():
    return create_rag_chain()

rag_chain = get_rag_chain()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about Python!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})   
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = rag_chain.invoke({"input": prompt})
            response = result["answer"]
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})