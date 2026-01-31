import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import  GridSearchCV, train_test_split
from sklearn.metrics import f1_score
from scr.Scrapping.Scrapping_Data import ROOT


def main():
    ROOT = Path(__file__).resolve().parents[2]            
    DATA_DIR = ROOT / "Data"
    CSV_PATH = DATA_DIR / "parfums_data_base_machineLearning.csv"

    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    y = df["Prix_Categorie"]
    X = df.drop(columns=["Prix_Categorie","Fragrance", "Marque"])
    text_cols = ["Ingredients_txt", "Concepts_txt"]
    cat_cols = [ "Famille", "Sous_famille", "Parfumeur", "Origine", "Genre"]
    num_cols = ["Année"]

    X["Ingredients_txt"] = X["Ingredients_txt"].fillna("") 
    X["Concepts_txt"] = X["Concepts_txt"].fillna("")
    for c in cat_cols:
        X[c] = X[c].fillna("Inconnu")
    X["Année"] = X["Année"].fillna(X["Année"].median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, random_state=1)

    preprocess = ColumnTransformer(
        transformers=[
            ("ing", TfidfVectorizer(min_df=5, ngram_range=(1, 2)), "Ingredients_txt"),
            ("con", TfidfVectorizer(min_df=5, ngram_range=(1, 2)), "Concepts_txt"),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )


    gbc = Pipeline([
    ("prep", preprocess),
    ("clf", GradientBoostingClassifier()),])

    bost_grid = {
    "clf__n_estimators": np.arange(50, 250, 50),
    "clf__learning_rate": [0.1, 1, 0.1],
    "clf__max_depth": np.arange(2, 10, 1),
    "clf__subsample": np.arange(0.5, 1.0, 0.1),}

    grid_gbc = GridSearchCV(
    gbc,
    param_grid=bost_grid,
    scoring="f1_macro",
    cv=5,
    n_jobs=-1,
    error_score=0.0)

    grid_gbc.fit(X_train, y_train)
    y_pred = grid_gbc.predict(X_test)
    print("F1 macro GradientBoostingClassifier :", f1_score(y_test, y_pred, average="macro"))
    print("Meilleurs paramètres GradientBoostingClassifier :", grid_gbc.best_params_)
    
    
    best_model = grid_gbc.best_estimator_
    joblib.dump(best_model, "best_model.pkl")


#-----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()