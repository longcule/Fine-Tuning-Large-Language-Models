from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def find_answer(question):
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    question_list = [item['question'] for item in data]
    question_list.append(question)


    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(question_list)
    similarity_matrix = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    max_similarity_index = similarity_matrix.argmax()
    max_similarity = similarity_matrix[max_similarity_index]
    print(max_similarity)
    if max_similarity > 0.7:
        return data[max_similarity_index]['answer']
    else:
        return None
    
