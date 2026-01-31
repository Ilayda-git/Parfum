"""
Helpers pour l'onglet Stats (Streamlit).

Objectif: fournir des agrégations robustes (comptes, parts, séries temporelles)
à partir du DataFrame principal, et de quoi afficher les origines en cartes + carte.

Aucune dépendance externe n'est requise (hors streamlit/pandas déjà utilisés).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import pandas as pd
import streamlit as st

try:
    # Déjà utilisé dans le projet pour les cartes parfums
    from streamlit_extras.stylable_container import stylable_container
except Exception:  # pragma: no cover
    stylable_container = None


# Coordonnées (lat, lon) approximatives par pays (libellés FR du dataset).
# Permet d'afficher une carte simple via st.map sans géocodage/dépendances.
ORIGIN_COORDS: Dict[str, Tuple[float, float]] = {
    "France": (46.2276, 2.2137),
    "Allemagne": (51.1657, 10.4515),
    "Royaume-Uni": (55.3781, -3.4360),
    "Espagne": (40.4637, -3.7492),
    "Italie": (41.8719, 12.5674),
    "Suisse": (46.8182, 8.2275),
    "États-Unis d'Amérique": (39.8283, -98.5795),
    "États-Unis": (39.8283, -98.5795),
    "Canada": (56.1304, -106.3468),
    "Belgique": (50.5039, 4.4699),
    "Pays-Bas": (52.1326, 5.2913),
    "Suède": (60.1282, 18.6435),
    "Norvège": (60.4720, 8.4689),
    "Danemark": (56.2639, 9.5018),
    "Irlande": (53.1424, -7.6921),
    "Portugal": (39.3999, -8.2245),
    "Autriche": (47.5162, 14.5501),
    "Grèce": (39.0742, 21.8243),
    "Turquie": (38.9637, 35.2433),
    "Maroc": (31.7917, -7.0926),
    "Tunisie": (33.8869, 9.5375),
    "Algérie": (28.0339, 1.6596),
    "Égypte": (26.8206, 30.8025),
    "Émirats arabes unis": (23.4241, 53.8478),
    "Arabie saoudite": (23.8859, 45.0792),
    "Inde": (20.5937, 78.9629),
    "Indonésie": (-0.7893, 113.9213),
    "Chine": (35.8617, 104.1954),
    "Japon": (36.2048, 138.2529),
    "Corée du Sud": (35.9078, 127.7669),
    "Australie": (-25.2744, 133.7751),
    "Brésil": (-14.2350, -51.9253),
    "Argentine": (-38.4161, -63.6167),
    "Mexique": (23.6345, -102.5528),
}


# Codes ISO-3 pour une carte choroplèthe Plotly.
# Clés = libellés d'origine tels qu'ils apparaissent dans le dataset.
ORIGIN_ISO3: Dict[str, str] = {
    "France": "FRA",
    "Allemagne": "DEU",
    "Royaume-Uni": "GBR",
    "Espagne": "ESP",
    "Italie": "ITA",
    "Suisse": "CHE",
    "États-Unis d'Amérique": "USA",
    "États-Unis": "USA",
    "Canada": "CAN",
    "Belgique": "BEL",
    "Pays-Bas": "NLD",
    "Suède": "SWE",
    "Norvège": "NOR",
    "Danemark": "DNK",
    "Irlande": "IRL",
    "Portugal": "PRT",
    "Autriche": "AUT",
    "Grèce": "GRC",
    "Turquie": "TUR",
    "Maroc": "MAR",
    "Tunisie": "TUN",
    "Algérie": "DZA",
    "Égypte": "EGY",
    "Émirats arabes unis": "ARE",
    "Arabie saoudite": "SAU",
    "Inde": "IND",
    "Indonésie": "IDN",
    "Chine": "CHN",
    "Japon": "JPN",
    "Corée du Sud": "KOR",
    "Australie": "AUS",
    "Brésil": "BRA",
    "Argentine": "ARG",
    "Mexique": "MEX",
}


@dataclass(frozen=True)
class DistResult:
    """Distribution triée avec effectifs + parts."""

    df: pd.DataFrame  # colonnes: Valeur, Count, Part


def _clean_series(s: pd.Series) -> pd.Series:
    return s.fillna("Inconnu").astype(str).str.strip().replace({"": "Inconnu"})


@st.cache_data
def distribution(df: pd.DataFrame, col: str, *, top_n: Optional[int] = None) -> DistResult:
    """Retourne une distribution (counts + parts) pour une colonne catégorielle."""
    if df is None or df.empty or col not in df.columns:
        return DistResult(pd.DataFrame(columns=["Valeur", "Count", "Part"]))

    s = _clean_series(df[col])
    # On force un schéma stable: série des comptes nommée "Count"
    vc = s.value_counts(dropna=False).rename("Count")

    if top_n is not None and top_n > 0 and len(vc) > top_n:
        top = vc.head(top_n)
        other = vc.iloc[top_n:].sum()
        vc = pd.concat([top, pd.Series({"Autres": other}, name="Count")]).rename("Count")

    tmp = vc.reset_index()

    # Après reset_index(), la colonne des catégories s'appelle souvent "index".
    # On la renomme systématiquement en "Valeur".
    if "Valeur" not in tmp.columns:
        if "index" in tmp.columns:
            tmp = tmp.rename(columns={"index": "Valeur"})
        else:
            non_count_cols = [c for c in tmp.columns if c != "Count"]
            if non_count_cols:
                tmp = tmp.rename(columns={non_count_cols[0]: "Valeur"})

    # Sécure: Count numérique
    out = (
        tmp[[c for c in ["Valeur", "Count"] if c in tmp.columns]]
        .assign(Count=lambda d: pd.to_numeric(d["Count"], errors="coerce").fillna(0).astype(int))
        .assign(Part=lambda d: (d["Count"] / max(int(d["Count"].sum()), 1)).round(4))
    )

    # Garantie de colonnes attendues
    if "Valeur" not in out.columns:
        out["Valeur"] = "Inconnu"
    if "Count" not in out.columns:
        out["Count"] = 0
    if "Part" not in out.columns:
        out["Part"] = 0.0

    return DistResult(out[["Valeur", "Count", "Part"]])


@st.cache_data
def yearly_counts(df: pd.DataFrame, year_col: str = "Année") -> pd.DataFrame:
    """Série temporelle: nb de parfums par année."""
    if df is None or df.empty or year_col not in df.columns:
        return pd.DataFrame(columns=[year_col, "Count"])

    y = pd.to_numeric(df[year_col], errors="coerce").dropna().astype(int)
    vc = y.value_counts().sort_index()
    return vc.rename("Count").reset_index().rename(columns={"index": year_col})


@st.cache_data
def price_by_year(df: pd.DataFrame, *, year_col: str = "Année", price_col: str = "Prix_Categorie") -> pd.DataFrame:
    """Table pivot: index=année, colonnes=catégorie de prix, valeurs=counts."""
    if df is None or df.empty or year_col not in df.columns or price_col not in df.columns:
        return pd.DataFrame()

    tmp = df[[year_col, price_col]].copy()
    tmp[year_col] = pd.to_numeric(tmp[year_col], errors="coerce")
    tmp[price_col] = _clean_series(tmp[price_col])
    tmp = tmp.dropna(subset=[year_col])
    tmp[year_col] = tmp[year_col].astype(int)

    pivot = (
        tmp.groupby([year_col, price_col])
        .size()
        .rename("Count")
        .reset_index()
        .pivot(index=year_col, columns=price_col, values="Count")
        .fillna(0)
        .astype(int)
        .sort_index()
    )
    return pivot


@st.cache_data
def origins_geo(df: pd.DataFrame, *, origin_col: str = "Origine", top_n: int = 30) -> pd.DataFrame:
    """Construit un DataFrame avec lat/lon pour afficher les origines sur une carte."""
    if df is None or df.empty or origin_col not in df.columns:
        return pd.DataFrame(columns=["Origine", "Count", "lat", "lon"])  # st.map attend lat/lon

    s = _clean_series(df[origin_col])
    vc = s.value_counts().head(max(int(top_n), 1))

    rows = []
    for origin, count in vc.items():
        if origin in ORIGIN_COORDS:
            lat, lon = ORIGIN_COORDS[origin]
            rows.append({"Origine": origin, "Count": int(count), "lat": lat, "lon": lon})

    if not rows:
        return pd.DataFrame(columns=["Origine", "Count", "lat", "lon"])

    return pd.DataFrame(rows).sort_values("Count", ascending=False)


@st.cache_data
def origins_choropleth(df: pd.DataFrame, *, origin_col: str = "Origine", top_n: int = 30) -> pd.DataFrame:
    """Construit un DataFrame (Origine/Count/iso_alpha) pour une carte choroplèthe Plotly."""
    if df is None or df.empty or origin_col not in df.columns:
        return pd.DataFrame(columns=["Origine", "Count", "iso_alpha"])

    s = _clean_series(df[origin_col])
    vc = s.value_counts().head(max(int(top_n), 1))

    rows = []
    for origin, count in vc.items():
        iso = ORIGIN_ISO3.get(origin)
        if iso:
            rows.append({"Origine": origin, "Count": int(count), "iso_alpha": iso})

    if not rows:
        return pd.DataFrame(columns=["Origine", "Count", "iso_alpha"])

    return pd.DataFrame(rows).sort_values("Count", ascending=False)


def render_origin_cards(dist_df: pd.DataFrame, *, max_cards: int = 12):
    """Affiche la distribution d'origines sous forme de cartes (top N)."""
    if dist_df is None or dist_df.empty:
        st.info("Aucune donnée d'origine à afficher.")
        return

    view = dist_df.head(max(int(max_cards), 1)).copy()
    cols = st.columns(3)

    for i, (_, r) in enumerate(view.iterrows()):
        origin = str(r.get("Valeur", ""))
        count = int(r.get("Count", 0))
        part = float(r.get("Part", 0.0))

        container_ctx = None
        if stylable_container is not None:
            container_ctx = stylable_container(
                key=f"origin_card_{i}_{origin}",
                css_styles="""
                {
                    background-color: #fff8f5;
                    border: 1px solid #e6d2c4;
                    border-radius: 14px;
                    padding: 14px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.18);
                    margin-bottom: 10px;
                }
                """,
            )

        with cols[i % 3]:
            if container_ctx is None:
                st.markdown(f"**{origin}**")
                st.caption(f"{count} parfums — {part * 100:.1f}%")
            else:
                with container_ctx:
                    st.markdown(f"**{origin}**")
                    st.caption(f"{count} parfums — {part * 100:.1f}%")
