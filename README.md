# 🌸 PROJET PARFUM : Web Scraping & Machine Learning  
**Analyse et prédiction du positionnement prix des parfums**

---

## 1. INTRODUCTION

Le prix d’un parfum ne dépend pas uniquement de ses caractéristiques olfactives ou de sa composition. Il est également influencé par des éléments immatériels tels que la notoriété de la marque, le marketing ou le positionnement commercial. Ces facteurs rendent souvent difficile la compréhension des écarts de prix entre des parfums pourtant comparables.

Ce projet a pour objectif de proposer une **approche plus objective du marché du parfum**, en s’appuyant exclusivement sur les **caractéristiques intrinsèques** des produits. À partir de données collectées automatiquement sur le [web](https://www.wikiparfum.com/fr/fragrances/) (famille olfactive, ingrédients, concepts, origine, année, genre), un modèle de **Machine Learning** prédit la **catégorie de prix** d’un parfum.

Le modèle classe les parfums selon trois segments représentatifs du marché : **mass market, prestige et niche**. La variable *marque* est volontairement exclue de la modélisation afin d’éviter un biais lié au branding et de se concentrer sur la valeur du produit indépendamment de son image commerciale.

L’application développée dans ce projet permet ainsi à l’utilisateur de comparer des parfums sur une base neutre, d’identifier des parfums potentiellement **sur ou sous-positionnés** en termes de prix, et de mieux comprendre les **logiques de segmentation** du marché du parfum. Elle peut également servir d’outil d’aide au positionnement pour un nouveau parfum, en estimant la catégorie de prix cohérente avec ses caractéristiques.

Les résultats fournis par l’application sont des **estimations analytiques** et ne constituent pas des prix de vente réels. Ils doivent être interprétés comme un **outil d’éclairage économique et pédagogique** sur la formation des prix dans le secteur du parfum.


---
## 2. OBJECTIFS DU PROJET

- Collecter automatiquement des données sur les parfums à partir du site [Wikiparfum](https://www.wikiparfum.com/fr/fragrances/) 
- Construire un dataset structuré et exploitable pour l’analyse  
- Mettre en place un pipeline reproductible de traitement des données  
- Entraîner des modèles de **Machine Learning** pour prédire la catégorie de prix des parfums  
- Predire Comparer la **catégorie réelle** d’un parfum à celle **prédite par le modèle**  
- Proposer une application interactive pour explorer et interpréter les résultats  

---

## 3. FONCTIONNALITÉS PRINCIPALES

- Web scraping automatisé de données produits  
- Nettoyage et transformation des données  
- Modèles de classification pour le positionnement prix (*mass market, prestige, niche*)  
- Predire la catégorie d'un parfum en fonction de ces caractéristiques et comparaison réel vs prédiction  
- Visualisations statistiques et exploratoires  
- Application Streamlit interactive  
- Tests unitaires pour certaines briques fonctionnelles  

---

## 4. STRUCTURE DU PROJET

Le projet est organisé de manière modulaire afin de séparer clairement les différentes étapes du pipeline :

```text
parfum/
│
├── data/
│   ├── parfums_liste_url.json          # URLs des pages à scraper
│   ├── parfums_data_base.json          # Données brutes scraper via les URLs
│   └── parfums_data_base_ml.csv        # Données prêtes pour le ML
│
├── src/
│   ├── app/
│   │   ├── module/                     # Fonctions 
│   │   └── style/                      # Style CSS de l’application
│   │
│   ├── Machine_Learning/
│   │   ├── module/                     # Fonctions 
│   │   ├── Nettoyage_base_ml.py        # Prétraitement des données
│   │   ├── Model_GB.py                 # Script ML du modèle sélectionner (Gradient Boosting)
│   │   ├── Liste_modele.ipynb          # Comparaison des modèles
│   │   └── best_model.pkl              # Modèle sélectionné
│   │
│   └── scraping/
│       ├── module/                     # Fonctions 
│       ├── Scraping_Data.py            # Scraping des données brutes pour chaque Fragrance
│       └── Scraping_URL.py             # Scraping des URLs
│
├── tests/
│   └── test_*.py                       # Tests unitaires
│
├── app.py                              # Lancement de l’application Streamlit
├── README.md
└── pyproject.toml

```
---

## 5. PRÉREQUIS

Python3.11

---


## 6. INSTALLATION
Via le clonage et Poetry

```text
(base) NomDeUtilisateur git clone <url-du-repository>
cd parfum
(base) NomDeUtilisateur python -m poetry install
(base) NomDeUtilisateur python -m poetry env activate
```
- Lorsque l’environnement virtuel est activé, toutes les commandes Python s’exécutent dans un environnement isolé, garantissant la reproductibilité du projet.

Alternative via pip

```text
(base) NomDeUtilisateur pip install -r requirements.txt
```

## 7. COMMENT EXÉCUTER LE PROJET ?
Lancer l’application Streamlit

```text 
(base) yilmazilayda@MacBookAir Parfum %  streamlit run app.py
```

Lancer les tests unitaires
```text
(base) yilmazilayda@MacBookAir Parfum % pytest
```

## 8. UTILISATION DE L’APPLICATION

L’application Streamlit permet d’interagir avec l’ensemble du pipeline du projet, depuis l’exploration des données jusqu’à la prédiction et la comparaison des catégories de prix.

Elle est structurée autour de plusieurs onglets, chacun répondant à un objectif précis.

### Introduction
Cet onglet présente le **scénario du projet** et la logique générale de l’application.  
Il explique pourquoi la prédiction se fait en **catégories de prix** (*mass market, prestige, niche*), ainsi que le choix méthodologique d’exclure la variable *marque* afin d’éviter un biais lié au branding.

### Explorer (catalogue)
Cet onglet permet d’explorer le catalogue de parfums collectés via le scraping.
L’utilisateur peut filtrer les parfums selon différentes caractéristiques :
- catégorie de prix,
- famille et sous-famille olfactive,
- origine, genre, parfumeur,
- ingrédients et concepts,
- année de sortie.

Les résultats peuvent être visualisés sous forme de **cartes** ou de **tableau**, facilitant la comparaison entre parfums.

### Prédire
Dans cet onglet, l’utilisateur peut renseigner les caractéristiques d’un parfum (famille, ingrédients, concepts, origine, etc.).
Le modèle de Machine Learning prédit alors la **catégorie de prix** la plus probable, accompagnée des **probabilités associées** à chaque segment.

Cette prédiction correspond à un **positionnement théorique**, indépendant de la marque.

### Comparer
Cet onglet permet de comparer :
- la **catégorie réelle** d’un parfum issu du catalogue,
- la **catégorie prédite** par le modèle à partir de ses caractéristiques.

L’objectif est d’identifier des écarts de positionnement (parfum potentiellement sur ou sous-positionné) et de mieux comprendre la logique de segmentation du marché.

### Ingrédients & Concepts
Cet onglet propose une analyse descriptive des ingrédients et concepts présents dans la base :
- fréquence d’apparition,
- répartition par nombre de parfums,
- exploration des termes les plus représentatifs.

### Stats
Cet onglet regroupe des statistiques descriptives et des visualisations interactives :
- répartition des catégories de prix,
- distribution par genre, famille ou origine,
- évolution temporelle des parfums,
- cartes de provenance.

---

## 10. AUTEURS

- **Thomas Barat**
- **Ilayda Yilmaz**  

