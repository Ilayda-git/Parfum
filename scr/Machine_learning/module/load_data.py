"""
Module pour charger les données depuis un fichier JSON et les convertir en DataFrame Polars.
"""

from pathlib import Path
import json
import polars as pl

def load_data(path: Path) -> pl.DataFrame:
    """
    Charge les données depuis un fichier JSON et les convertit en DataFrame Polars.
    
    :param path: Chemin vers le fichier JSON contenant les données.
    :type path: Path
    :return: DataFrame Polars contenant les données chargées.
    :rtype: pl.DataFrame
    """
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    return pl.from_dicts(obj["contenu"])