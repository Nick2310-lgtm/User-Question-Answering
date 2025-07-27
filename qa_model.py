from transformers import pipeline

# Load pre-trained QA pipeline once
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(context: str, question: str) -> str:
    if not context.strip() or not question.strip():
        return "Context or question is empty."
    try:
        result = qa_pipeline(question=question, context=context)
        return result["answer"]
    except Exception as e:
        return f"Error: {str(e)}"
