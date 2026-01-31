import pandas as pd
import streamlit as st



def contains_term(series: pd.Series, term: str) -> pd.Series:
    """Vrai si la colonne texte contient le terme comme mot (matching simple par espaces)."""
    s = (" " + series.fillna("").astype(str).str.lower() + " ")
    return s.str.contains(f" {str(term).lower()} ", regex=False)


def filter_by_terms(df_: pd.DataFrame, col: str, terms: list[str]) -> pd.DataFrame:
    """Filtre `df_` en conservant les lignes qui contiennent tous les termes donnés."""
    if not terms or df_.empty or col not in df_.columns:
        return df_
    out = df_
    for t in terms:
        out = out[contains_term(out[col], t)]
    return out


def add_terms_to_session_text(session_key: str, terms: list[str]):
    """Ajoute des termes au texte (stocké dans st.session_state) sans doublons."""
    current = (st.session_state.get(session_key) or "").strip().lower()
    current_tokens = current.split() if current else []
    current_set = set(current_tokens)
    to_add = [str(t).strip().lower() for t in (terms or []) if str(t).strip()]
    merged = current_tokens + [t for t in to_add if t not in current_set]
    st.session_state[session_key] = " ".join(merged).strip()