# 🌸 PROJET PARFUM — Web Scraping & Machine Learning  
**Analyse et prédiction du positionnement prix des parfums**

---

## 1. INTRODUCTION

Ce projet vise à analyser le **marché du parfum** à partir de données produits collectées automatiquement sur des sites spécialisés (notamment *Wikiparfum*), puis à exploiter ces données à l’aide de techniques de **Machine Learning** afin de **prédire et comparer le positionnement prix** des parfums.

Le marché du parfum est structuré autour de plusieurs segments (*mass market, prestige, niche*), dont les frontières sont parfois floues pour le consommateur. L’objectif du projet est de proposer une **lecture objective de ces segments**, fondée sur les **caractéristiques intrinsèques** des parfums (famille olfactive, ingrédients, concepts, origine, année, genre, etc.).

La variable *marque* est volontairement exclue des modèles afin d’éviter un biais lié au branding et de se concentrer sur la logique économique du produit lui-même.

---

## 2. OBJECTIFS DU PROJET

- Collecter des données parfums via le **web scraping**
- Construire un dataset structuré et exploitable
- Mettre en place un pipeline reproductible de traitement des données
- Entraîner des modèles de **classification** pour prédire la catégorie de prix
- Comparer la **catégorie réelle** d’un parfum à celle **prédite par le modèle**
- Proposer une **application interactive** pour explorer et interpréter les résultats

---

## 3. FONCTIONNALITÉS PRINCIPALES

- Scraping automatisé de données produits
- Nettoyage et transformation des données
- Modèles de Machine Learning pour la prédiction du positionnement prix
- Comparaison réel vs prédiction
- Visualisations statistiques et exploratoires
- Application Streamlit interactive
- Tests unitaires pour certaines briques fonctionnelles

Ce projet illustre les enjeux économiques liés à la **segmentation prix** dans un marché fortement influencé par des facteurs immatériels.

---

## 4. STRUCTURE DU PROJET

Le projet est organisé de manière modulaire afin de séparer clairement les différentes étapes du pipeline :

```text
parfum/
│
├── data/
│       ├── parfums_liste_url.json
│       └── parfums_data_base.json
│       └── parfums_data_base_ml.csv
│
├── src/
│   ├── app/
│   │   ├── module/
│   │   └── style/
│   │
│   ├── Machine_Learning/
│   │   ├── module/
│   │   ├── Nettoyage_base_ml.py
│   │   ├── Model_GB.py
│   │   ├── Liste_modele.ipynb
│   │   └── best_model.pkl
│   │
│   └── scraping/
│       ├── module/
│       ├── Scraping_Data.py
│       └── Scraping_URL.py
│
├── tests/
│   └── test_*.py
│
├── app.py
├── README.md
└── pyproject.toml
```
