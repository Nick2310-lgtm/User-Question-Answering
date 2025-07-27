import streamlit as st
from qa_model import answer_question

st.set_page_config(page_title="User Question Answering", layout="centered")

st.title("📘 User Question Answering System")
st.write("Ask a question based on the given context.")

context = st.text_area("📄 Enter context passage:", height=250, placeholder="Paste your context here...")
question = st.text_input("❓ Enter your question:", placeholder="Type your question here...")

if st.button("Get Answer"):
    with st.spinner("Generating answer..."):
        answer = answer_question(context, question)
        st.success(f"🧠 Answer: {answer}")
