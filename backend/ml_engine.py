import os
import io
import zipfile
import requests
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
MODEL_PATH = "spam_model.joblib"
DATASET_PATH = "SMSSpamCollection"

class SpamClassifier:
    def __init__(self):
        self.pipeline = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            print(f"Loading existing model from {MODEL_PATH}...")
            self.pipeline = joblib.load(MODEL_PATH)
        else:
            print("Model not found. Training a new one...")
            self.train()

    def download_data(self):
        if os.path.exists(DATASET_PATH):
            return

        print(f"Downloading dataset from {DATA_URL}...")
        r = requests.get(DATA_URL)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(".")
        print("Dataset downloaded and extracted.")

    def train(self):
        self.download_data()
        
        # Load dataset
        # The dataset is tab-separated with 'label' and 'message'
        df = pd.read_csv(DATASET_PATH, sep='\t', header=None, names=['label', 'message'])
        
        X = df['message']
        y = df['label'].apply(lambda x: 1 if x == 'spam' else 0)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', LogisticRegression(solver='liblinear'))
        ])

        print("Training model...")
        self.pipeline.fit(X_train, y_train)

        # Evaluate
        preds = self.pipeline.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"Model trained. Accuracy: {acc:.4f}")

        # Save model
        joblib.dump(self.pipeline, MODEL_PATH)

    def predict(self, text):
        if not self.pipeline:
            raise Exception("Model not loaded")
        
        # return probability of being spam (class 1)
        proba = self.pipeline.predict_proba([text])[0][1]
        return proba
