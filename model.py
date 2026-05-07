import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

def train_and_save():

    df = pd.read_csv("dataset.csv")

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=20,
        random_state=42
    )

    model.fit(X, y)

    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

def load_model():

    with open("model.pkl", "rb") as file:
        return pickle.load(file)
