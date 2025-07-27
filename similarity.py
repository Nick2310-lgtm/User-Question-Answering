from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_most_similar(question, data, threshold=0.7):
    if not data:
        return None, None

    questions = [q[0] for q in data]
    answers = [q[1] for q in data]

    vectorizer = TfidfVectorizer().fit_transform([question] + questions)
    similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    max_sim_index = similarities.argmax()
    if similarities[max_sim_index] >= threshold:
        return questions[max_sim_index], answers[max_sim_index]
    return None, None
