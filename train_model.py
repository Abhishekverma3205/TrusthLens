import os
import pickle

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# -------------------------------
# Load Dataset
# -------------------------------

fake = pd.read_csv("data/Fake.csv")
true = pd.read_csv("data/True.csv")

fake["label"] = 0
true["label"] = 1

df = pd.concat([fake, true], ignore_index=True)

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# -------------------------------
# Feature
# -------------------------------

X = df["text"]
y = df["label"]

# -------------------------------
# Train Test Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

# -------------------------------
# TF-IDF
# -------------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7
)

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# -------------------------------
# Model
# -------------------------------

model = PassiveAggressiveClassifier(max_iter=100)

model.fit(X_train, y_train)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("\n===============================")
print("Model Training Complete")
print("===============================")
print(f"Accuracy : {accuracy*100:.2f}%")
print("===============================\n")

# -------------------------------
# Save Model
# -------------------------------

os.makedirs("models", exist_ok=True)

pickle.dump(model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("Model Saved Successfully.")


import json
import os

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)

metrics = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2)
}

os.makedirs("models", exist_ok=True)

with open("models/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

os.makedirs("reports", exist_ok=True)

with open("reports/classification_report.txt", "w") as f:
    f.write(classification_report(y_test, pred))


    import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

disp = ConfusionMatrixDisplay(
    confusion_matrix=confusion_matrix(y_test, pred),
    display_labels=["Fake", "Real"]
)

disp.plot()

plt.savefig("reports/confusion_matrix.png")

plt.close()