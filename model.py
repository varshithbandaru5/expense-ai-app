import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("expenses.csv")

# Features and labels
X = data["text"]
y = data["category"]

# Better text vectorization
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Better model
model = LogisticRegression()
model.fit(X_vectorized, y)

# Prediction function
def predict_category(text):
    text_vec = vectorizer.transform([text])
    return model.predict(text_vec)[0]