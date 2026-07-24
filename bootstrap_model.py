"""
Bootstrap script: trains a TruthLens model.
- If data/Fake.csv and data/True.csv exist, uses those.
- Otherwise trains on built-in seed samples so the app starts.
Run once before deploying:  python bootstrap_model.py
"""

import os
import json
import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# ─── Load Data ───────────────────────────────────────────────

def load_data():
    fake_path = os.path.join(BASE_DIR, "data", "Fake.csv")
    true_path = os.path.join(BASE_DIR, "data", "True.csv")

    if os.path.exists(fake_path) and os.path.exists(true_path):
        import pandas as pd
        print("📂 Loading real dataset...")
        fake = pd.read_csv(fake_path)
        true = pd.read_csv(true_path)
        fake["label"] = 0
        true["label"] = 1
        df = pd.concat([fake, true], ignore_index=True).sample(frac=1, random_state=42)
        texts = df["text"].fillna("").tolist()
        labels = df["label"].tolist()
        return texts, labels

    # Seed samples for bootstrap (app works without real CSVs)
    print("⚡ No dataset found — using seed samples for bootstrap model.")
    fake_samples = [
        "BREAKING: Scientists confirm that drinking bleach cures cancer, government hiding cure.",
        "Exclusive: President secretly reptilian alien, whistleblower claims with no evidence.",
        "SHOCKING: Vaccines contain microchips to track population says anonymous source.",
        "Deep state plot exposed: moon landing was filmed in Hollywood basement studio.",
        "Chemtrails proven to contain mind-control chemicals by rogue chemist.",
        "ALERT: 5G towers cause coronavirus, thousands sign petition demanding removal.",
        "Secret leaked document reveals climate change is a hoax invented by China.",
        "Hollywood elites running underground child trafficking operation in pizza shop.",
        "New world order plans to reduce population by 90 percent revealed in leaked memo.",
        "FBI whistleblower claims election was stolen using quantum voting machines.",
        "Doctors admit flu shots contain live viruses to make people sick for profit.",
        "Experts warn that eating avocados causes immediate mind control in humans.",
        "Anonymous hacker reveals that Google is secretly recording all conversations.",
        "Bombshell report: Mars already colonized by secret shadow government since 1950.",
        "Breaking news: Water fluoridation confirmed to lower IQ according to secret study.",
        "Urgent warning: New phone update installs spyware directly into your brain cells.",
        "Leaked files show Bill Gates planned pandemic years ago to depopulate earth.",
        "Scientists paid by pharma companies to lie about dangers of natural medicine.",
        "EXPOSED: Major bank CEO admits fractional reserve banking is legal counterfeiting.",
        "Conspiracy confirmed: Flat earth society gets banned from internet by tech giants.",
    ] * 10

    real_samples = [
        "Federal Reserve raises interest rates by 25 basis points amid inflation concerns.",
        "NASA successfully launches new satellite to monitor climate change from orbit.",
        "WHO reports global measles cases increased by 45 percent in 2023 compared to 2022.",
        "Supreme Court issues landmark ruling on digital privacy and data protection rights.",
        "New study published in Nature finds link between air pollution and cognitive decline.",
        "Tech company announces quarterly earnings exceeding analyst expectations by 12 percent.",
        "United Nations climate summit reaches agreement on reducing carbon emissions by 2030.",
        "Local government approves budget increase for public school infrastructure repairs.",
        "Scientists at CERN confirm discovery of new subatomic particle after years of research.",
        "Economic report shows unemployment rate drops to 3.5 percent, lowest since 2019.",
        "Health officials urge vaccination after measles outbreak detected in three counties.",
        "City council votes to expand public transportation network to underserved neighborhoods.",
        "University researchers develop new battery technology that charges in under five minutes.",
        "Stock market closes higher as investors respond positively to jobs report data.",
        "International trade agreement signed between fifteen nations to reduce tariff barriers.",
        "Medical journal publishes findings on effectiveness of new diabetes treatment approach.",
        "Government agency reports significant decrease in water pollution levels since 2020.",
        "Tech startup raises 50 million in Series B funding round led by venture capital firms.",
        "Annual census data reveals population growth concentrated in southern and western states.",
        "Public health department reports 20 percent decline in opioid overdose deaths this year.",
    ] * 10

    texts = fake_samples + real_samples
    labels = [0] * len(fake_samples) + [1] * len(real_samples)
    return texts, labels


# ─── Train ───────────────────────────────────────────────────

def train():
    texts, labels = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7, max_features=50000)
    X_train_v = vectorizer.fit_transform(X_train)
    X_test_v  = vectorizer.transform(X_test)

    model = PassiveAggressiveClassifier(max_iter=200, random_state=42)
    model.fit(X_train_v, y_train)

    pred = model.predict(X_test_v)
    acc  = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred, zero_division=0)
    rec  = recall_score(y_test, pred, zero_division=0)
    f1   = f1_score(y_test, pred, zero_division=0)

    print(f"\n✅ Accuracy:  {acc*100:.2f}%")
    print(f"   Precision: {prec*100:.2f}%")
    print(f"   Recall:    {rec*100:.2f}%")
    print(f"   F1 Score:  {f1*100:.2f}%\n")

    # Save model & vectorizer
    with open(os.path.join(MODELS_DIR, "model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    # Save metrics
    metrics = {
        "accuracy":  round(acc*100, 2),
        "precision": round(prec*100, 2),
        "recall":    round(rec*100, 2),
        "f1_score":  round(f1*100, 2)
    }
    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    print("💾 Model saved to models/")


if __name__ == "__main__":
    train()
