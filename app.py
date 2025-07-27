import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Question Answering System", layout="wide")

# Load transformer pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

st.title("📄 Upload Document + ❓ Ask Questions")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

context = ""
if uploaded_file:
    context = uploaded_file.read().decode("utf-8")
    st.success("Document uploaded successfully!")

if context:
    question = st.text_input("Enter your question:")
    if question:
        result = qa_pipeline({"context": context, "question": question})
        st.subheader("📌 Answer")
        st.markdown(f"**{result['answer']}**")
        st.caption(f"Confidence: {result['score']:.4f}")
else:
    st.info("Please upload a text file to begin.")
