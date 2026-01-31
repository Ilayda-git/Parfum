"""
Module pour le nettoyage de la base de données de parfums en vue de l'apprentissage automatique.
"""

from pathlib import Path
import polars as pl
from src.Machine_learning.module.load_data import load_data
from src.Machine_learning.module.nettoyage import nettoyage

root = Path(__file__).resolve().parents[2]
in_path = root / "Data" / "parfums_data_base.json"
out_path = root / "Data" / "parfums_data_base_machineLearning.csv"

def main():
    """    
    Télécharge les données brutes, les nettoie, et enregistre les données nettoyées dans un fichier CSV.
    """ 
    df_brut = load_data(in_path)
    df_clean = nettoyage(df_brut)
    df_clean.write_csv(out_path)

    print( df_clean.shape)
    print(df_clean.select(pl.all().is_null().sum()))

if __name__ == "__main__":
    main()
