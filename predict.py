import os
import pickle
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)


def explain_prediction(news_vector, top_n=10):
    """
    Returns the most important words in the input based on TF-IDF values.
    """
    feature_names = vectorizer.get_feature_names_out()

    indices = news_vector.nonzero()[1]

    values = news_vector.data

    if len(values) == 0:
        return []

    pairs = list(zip(indices, values))

    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    important = []

    for index, score in pairs[:top_n]:
        important.append({
            "word": feature_names[index],
            "score": round(float(score), 3)
        })

    return important


def predict_news(news):

    vector = vectorizer.transform([news])

    prediction = model.predict(vector)[0]

    if hasattr(model, "decision_function"):
        confidence = abs(model.decision_function(vector)[0])
        confidence = min(99.9, 50 + confidence * 8)
    else:
        confidence = 95

    label = "REAL NEWS" if prediction == 1 else "FAKE NEWS"

    explanation = explain_prediction(vector)

    return {
        "prediction": label,
        "confidence": round(confidence,2),
        "explanation": explanation
    }