"""
Module de nettoyage des données pour le Machine Learning.
"""

import polars as pl

def nettoyage(df: pl.DataFrame) -> pl.DataFrame:
    """
    Nettoyage dez données pour le Machine Learning.
    
    :param df: DataFrame Polars à nettoyer.
    :type df: pl.DataFrame
    :return: DataFrame Polars nettoyé.
    :rtype: pl.DataFrame
    """
    return (
        df
        # Ingredients : list[str] -> texte
        .with_columns(
            pl.col("Ingredients")
                .list.eval(pl.element().str.strip_chars())
                .list.drop_nulls()
                .list.unique()
                .list.join(" ")
                .alias("Ingredients_txt")
        )
        # Concepts : string -> texte
        .with_columns(
            pl.col("Concepts")
                .fill_null("")
                .str.replace_all(r"\s*,\s*", " ")
                .str.replace_all(r"\s+", " ")
                .str.strip_chars()
                .str.to_lowercase()
                .alias("Concepts_txt")
        )
        # Nettoyage texte (ingredients + concepts)
        .with_columns(
            pl.col("Ingredients_txt")
                .str.to_lowercase()
                .str.replace_all(r"[()–+/]", " ")
                .str.replace_all(r"[^a-zàâäçéèêëîïôöùûüÿñæœ\s]", "")
                .str.replace_all(r"\s+", " ")
                .str.strip_chars()
                .alias("Ingredients_txt"),

            pl.col("Concepts_txt")
                .str.to_lowercase()
                .str.replace_all(r"[()–+/]", " ")
                .str.replace_all(r"[^a-zàâäçéèêëîïôöùûüÿñæœ\s]", "")
                .str.replace_all(r"\s+", " ")
                .str.strip_chars()
                .alias("Concepts_txt"),
        )
        # Valeurs manquantes
        .with_columns(
            pl.col("Parfumeur").fill_null("Inconnu"),
            pl.col("Origine").fill_null("Inconnu"),
            pl.col("Fragrance").fill_null("Inconnu"),
            pl.col("Genre").fill_null("Unisexe"),
            pl.col("Concepts_txt").fill_null(""),
            pl.col("Prix_Categorie").str.strip_chars(),
        )
        # Année
        .with_columns(
            pl.col("Année")
                .fill_null(pl.col("Année").median())
                .round(0)
                .cast(pl.Int64)
        )
        # Suppression colonnes inutiles
        .drop(["Ingredients", "Concepts"])
    )