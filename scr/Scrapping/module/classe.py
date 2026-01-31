"""
Module définissant les classes de données pour le scrapping des parfums.
"""

from typing import Optional
from pydantic import BaseModel


class Donnée_Parfum(BaseModel):
    Marque: Optional[str] = None
    Famille : Optional[str] = None
    Sous_famille : Optional[str] = None
    Parfumeur : Optional[str] = None
    Ingredients : Optional[list[str]] = None
    Prix_Categorie : Optional[str] = None
    Fragrance : Optional[str] = None
    Origine : Optional[str] = None
    Genre : Optional[str] = None
    Année : Optional[int] = None
    Concepts : Optional[str]  = None


class Data_base(BaseModel):
    contenu: list[Donnée_Parfum]


class Parfum(BaseModel):
    nom_brut: str
    url: str


class Catalogue(BaseModel):
    contenu: list[Parfum]