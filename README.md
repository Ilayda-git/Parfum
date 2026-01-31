# 🌸 PROJET PARFUM — Web Scraping & Machine Learning  
**Analyse et prédiction du positionnement prix des parfums**

---

## 1. INTRODUCTION

Le prix d’un parfum ne dépend pas uniquement de ses caractéristiques olfactives ou de sa composition. Il est également influencé par des éléments immatériels tels que la notoriété de la marque, le marketing ou le positionnement commercial. Ces facteurs rendent souvent difficile la compréhension des écarts de prix entre des parfums pourtant comparables.

Ce projet a pour objectif de proposer une **approche plus objective du marché du parfum**, en s’appuyant exclusivement sur les **caractéristiques intrinsèques** des produits. À partir de données collectées automatiquement sur le web (famille olfactive, ingrédients, concepts, origine, année, genre), un modèle de **Machine Learning** prédit la **catégorie de prix** d’un parfum.

Le modèle classe les parfums selon trois segments représentatifs du marché : **mass market, prestige et niche**. La variable *marque* est volontairement exclue de la modélisation afin d’éviter un biais lié au branding et de se concentrer sur la valeur du produit indépendamment de son image commerciale.

L’application développée dans ce projet permet ainsi à l’utilisateur de comparer des parfums sur une base neutre, d’identifier des parfums potentiellement **sur- ou sous-positionnés** en termes de prix, et de mieux comprendre les **logiques de segmentation** du marché du parfum. Elle peut également servir d’outil d’aide au positionnement pour un nouveau parfum, en estimant la catégorie de prix cohérente avec ses caractéristiques.

Les résultats fournis par l’application sont des **estimations analytiques** et ne constituent pas des prix de vente réels. Ils doivent être interprétés comme un **outil d’éclairage économique et pédagogique** sur la formation des prix dans le secteur du parfum.


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
