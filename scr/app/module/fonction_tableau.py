import pandas as pd
import streamlit as st


def show_perfumes_table(df_show: pd.DataFrame, *, height: int = 520):
    """Affiche un tableau de parfums avec colonnes compactes."""
    if df_show is None or df_show.empty:
        st.warning("Aucun parfum ne correspond aux filtres.")
        return

    col_cfg = {}
    if "Année" in df_show.columns:
        col_cfg["Année"] = st.column_config.NumberColumn("Année", format="%d")
    if "Prix_Categorie" in df_show.columns:
        col_cfg["Prix_Categorie"] = st.column_config.TextColumn("Prix")
    if "Ingredients_txt" in df_show.columns:
        col_cfg["Ingredients_txt"] = st.column_config.TextColumn("Ingrédients", width="large", max_chars=80)
    if "Concepts_txt" in df_show.columns:
        col_cfg["Concepts_txt"] = st.column_config.TextColumn("Concepts", width="large", max_chars=80)

    st.dataframe(
        df_show,
        use_container_width=True,
        height=height,
        hide_index=True,
        column_config=col_cfg if col_cfg else None,
    )


def show_terms_table(df_terms: pd.DataFrame, *, height: int = 520):
    """Affiche un tableau 'termes' avec une mise en forme plus lisible."""
    if df_terms is None or df_terms.empty:
        st.info("Aucun terme à afficher.")
        return

    max_perfumes = int(df_terms["Parfums"].max()) if "Parfums" in df_terms.columns else 1
    max_occ = int(df_terms["Occurrences"].max()) if "Occurrences" in df_terms.columns else 1

    st.dataframe(
        df_terms,
        use_container_width=True,
        height=height,
        hide_index=True,
        column_config={
            "Terme": st.column_config.TextColumn("Terme", help="Terme extrait du texte"),
            "Parfums": st.column_config.ProgressColumn(
                "Parfums",
                help="Nombre de parfums contenant ce terme",
                min_value=0,
                max_value=max_perfumes,
                format="%d",
            ),
            "Occurrences": st.column_config.ProgressColumn(
                "Occurrences",
                help="Nombre total d'occurrences du terme dans tout le dataset",
                min_value=0,
                max_value=max_occ,
                format="%d",
            ),
        },
    )
