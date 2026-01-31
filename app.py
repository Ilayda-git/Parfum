"""
Application Streamlit pour explorer et prédire les catégories de prix des parfums.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

try:
    import plotly.express as px

    # Palette alignée sur scr/app/style/style.css
    _PLOTLY_COLORS = [
        "#c0392b",  
        "#803d3d", 
        "#f38b96",  
        "#651e2c",  
        "#b56576",
        "#e6d2c4", 
    ]
    _PLOTLY_TEMPLATE = {
        "layout": {
            "paper_bgcolor": "#faf0e6",
            "plot_bgcolor": "#faf0e6",
            "font": {"family": "Noto Sans, sans-serif", "color": "#651e2c"},
            "title": {"font": {"family": "Rubik, sans-serif", "color": "#651e2c"}},
            "colorway": _PLOTLY_COLORS,
            "xaxis": {
                "gridcolor": "#e6d2c4",
                "zerolinecolor": "#e6d2c4",
                "linecolor": "#803d3d",
                "tickfont": {"color": "#651e2c"},
                "title": {"font": {"color": "#651e2c"}},
            },
            "yaxis": {
                "gridcolor": "#e6d2c4",
                "zerolinecolor": "#e6d2c4",
                "linecolor": "#803d3d",
                "tickfont": {"color": "#651e2c"},
                "title": {"font": {"color": "#651e2c"}},
            },
            "legend": {"font": {"color": "#651e2c"}},
        }
    }

    _PLOTLY_OK = True
except Exception:
    px = None 
    _PLOTLY_COLORS = [] 
    _PLOTLY_TEMPLATE = None 
    _PLOTLY_OK = False

from src.app.module.fonction_filtre import filter_df, options, opts_no_all
from src.app.module.fonction_prettycard import pretty_cards
from src.app.module.fonction_filtre_2 import filter_by_terms
from src.app.module.fonction_tableau import show_terms_table
from src.app.module.fonction_cache import load_data, load_model, build_term_stats
from src.app.module.fonction_css import local_css
from src.app.module.fonction_stats import (
    distribution,
    origins_choropleth,
    origins_geo,
    price_by_year,
    yearly_counts,
)

st.set_page_config(page_title="Parfums — Explorer & Prédire", page_icon="🌸", layout="wide")
st.title("🌸 Parfums : Explorer & Prédire la catégorie de prix")

local_css("style.css")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "parfums_data_base_machineLearning.csv"
MODEL_PATH = ROOT / "src" / "Machine_learning" / "best_model.pkl"

df = load_data(DATA_PATH)

# --- INTERFACE PRINCIPALE ---
tab5, tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Présentation",
    "🔎 Explorer (catalogue)",
    "🔮 Prédire",
    "🧾 Ingrédients & Concepts",
    "📊 Stats",
])


#------------------------------------------------------------------------------------------------------------------------------------------


# ONGLET 1 : EXPLORER
with tab1:
    col1, col2 = st.columns([3, 1])

    ing_terms_all = build_term_stats(df, "Ingredients_txt")["Terme"].tolist() if not df.empty else []
    con_terms_all = build_term_stats(df, "Concepts_txt")["Terme"].tolist() if not df.empty else []

    with col2:
        st.subheader("Filtres")
        with st.container(border=True):
            prix = st.selectbox("Catégorie de prix", options(df, "Prix_Categorie"))
            marque = st.selectbox("Marque", options(df, "Marque"))
            famille = st.selectbox("Famille", options(df, "Famille"))
            sous_famille = st.selectbox("Sous_famille", options(df, "Sous_famille"))
            origine = st.selectbox("Origine", options(df, "Origine"))
            genre = st.selectbox("Genre", options(df, "Genre"))
            parfumeur = st.selectbox("Parfumeur", options(df, "Parfumeur"))
            
            annee_min, annee_max = (1900, 2100)
            if "Année" in df.columns:
                annee_min, annee_max = int(df["Année"].min()), int(df["Année"].max())
            annee_range = st.slider("Année", annee_min, annee_max, (annee_min, annee_max))
            
            ingredients_pick = st.multiselect(
                "Ingrédients",
                options=ing_terms_all
            )
            concepts_pick = st.multiselect(
                "Concepts",
                options=con_terms_all
            )

    # Résultats
    with col1:
        filters = {
            "Prix_Categorie": prix, "Marque": marque, "Famille": famille,
            "Sous_famille": sous_famille, "Origine": origine, "Genre": genre, "Parfumeur": parfumeur
        }
        df_f = filter_df(df, filters)
        if "Année" in df_f.columns:
            df_f = df_f[(df_f["Année"] >= annee_range[0]) & (df_f["Année"] <= annee_range[1])]

        df_f = filter_by_terms(df_f, "Ingredients_txt", ingredients_pick)
        df_f = filter_by_terms(df_f, "Concepts_txt", concepts_pick)

        st.info(f"✨ **{len(df_f)}** parfums trouvés")
        
        limit = min(50, len(df_f))
        
        c_view, c_sort, c_limit = st.columns([2, 2, 3])
        with c_view: 
            view_mode = st.radio("Vue", ["Cartes", "Tableau"], horizontal=True)
        with c_sort: 
            sort_by = st.selectbox("Trier par", ["Années (récent)", "Marques (A-Z)"])
        with c_limit: 
            if limit > 0:
                if limit >= 5:
                    max_cards = st.slider("Nombre de parfums", 5, limit, 5)
                else:
                    max_cards = st.slider("Nombre de parfums", 1, limit, limit)
            else:
                st.caption("Aucun résultat")
                max_cards = 0

        if sort_by == "Années (récent)" and "Année" in df_f.columns:
            df_f = df_f.sort_values("Année", ascending=False)
        elif sort_by == "Marques (A-Z)" and "Marque" in df_f.columns:
            df_f = df_f.sort_values("Marque", ascending=True)

        st.divider()

        if len(df_f) == 0:
            st.warning("Aucun résultat ne correspond à votre recherche.")
        elif view_mode == "Tableau":
            st.dataframe(df_f.head(max_cards), use_container_width=True, height=600)
        else:
            if limit == 0:
                st.warning("Aucun résultat à afficher.")
            elif limit == 1:
                pretty_cards(df_f, max_cards=1)
            else:
                pretty_cards(df_f, max_cards=max_cards)

    
#------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 : Prédire (ML)

with tab2:
    sub1, sub2 = st.tabs(["🔮 Prédire", "📌 Comparer"])
    # Sous-onglet 1 : Prédire
    with sub1:
        st.subheader("Prédire une catégorie de prix (ML)")

        model = load_model(MODEL_PATH)

        if model is None:
            st.error("Le modèle n'a pas pu être chargé. Vérifie le fichier .pkl et les versions (numpy/sklearn).")
            st.stop()

        if "ml_pred" not in st.session_state:
            st.session_state["ml_pred"] = None
        if "ml_proba_df" not in st.session_state:
            st.session_state["ml_proba_df"] = None

        c1, c2, c3 = st.columns(3)

        with c1:
            famille = st.selectbox("Famille", opts_no_all(df, "Famille"), index=0, key="pred_famille")
            sous_famille = st.selectbox("Sous_famille", opts_no_all(df, "Sous_famille"), index=0, key="pred_sous_famille")
            parfumeur = st.selectbox("Parfumeur", opts_no_all(df, "Parfumeur"), index=0, key="pred_parfumeur")

        with c2:
            origine = st.selectbox("Origine", opts_no_all(df, "Origine"), index=0, key="pred_origine")
            genre = st.selectbox("Genre", opts_no_all(df, "Genre"), index=0, key="pred_genre")

            if "Année" in df.columns:
                annee = st.selectbox("Année", opts_no_all(df, "Année"), index=0, key="pred_annee")
            else:
                annee = 0
                st.info("Colonne Année indisponible dans la base.")

        with c3:
            ing_terms_all = build_term_stats(df, "Ingredients_txt")["Terme"].tolist() if not df.empty else []
            con_terms_all = build_term_stats(df, "Concepts_txt")["Terme"].tolist() if not df.empty else []

            ingredients = st.multiselect("Sélectionner des ingrédients", options=ing_terms_all, key="pred_ingredients")
            concepts = st.multiselect("Sélectionner des concepts", options=con_terms_all, key="pred_concepts")

            if st.button("Prédire", type="primary", key="pred_button"):
                X_new = pd.DataFrame([{
                    "Famille": famille,
                    "Sous_famille": sous_famille,
                    "Parfumeur": parfumeur,
                    "Origine": origine,
                    "Genre": genre,
                    "Année": int(annee) if str(annee).isdigit() else 0,
                    "Ingredients_txt": (" ".join(ingredients) if ingredients else "").strip().lower(),
                    "Concepts_txt": (" ".join(concepts) if concepts else "").strip().lower(),
                }])

                st.session_state["ml_pred"] = model.predict(X_new)[0]

                proba_df = None
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(X_new)[0]
                    classes = list(getattr(model, "classes_", []))
                    if classes:
                        proba_df = (
                            pd.DataFrame({"Classe": classes, "Probabilité": proba})
                            .sort_values("Probabilité", ascending=False)
                        )
                st.session_state["ml_proba_df"] = proba_df

        st.divider()
        st.markdown("### Résultat")
        if st.session_state.get("ml_pred") is None:
            st.caption("Choisis les paramètres puis clique sur **Prédire**.")
        else:
            st.success(f"Catégorie de prix prédite : **{st.session_state['ml_pred']}**")
            proba_df = st.session_state.get("ml_proba_df")
            if isinstance(proba_df, pd.DataFrame) and not proba_df.empty:
                st.dataframe(proba_df, use_container_width=True)

    # Sous-onglet 2 : Comparer (réel vs ML)
    with sub2:
        st.subheader("Comparer la catégorie de prix : réelle vs prédite")

        model = load_model(MODEL_PATH)
        if model is None:
            st.error("Le modèle n'a pas pu être chargé. Vérifie le fichier .pkl et les versions (numpy/sklearn).")
            st.stop()

        if "Fragrance" not in df.columns or "Prix_Categorie" not in df.columns:
            st.info("Comparaison impossible : colonnes manquantes (Fragrance / Prix_Categorie).")
            st.stop()

        df_cmp = df.copy()
        df_cmp["Label"] = df_cmp["Marque"].astype(str) + " — " + df_cmp["Fragrance"].astype(str)

        label_pick = st.selectbox(
            "Choisir un parfum (dans la base)",
            options=df_cmp["Label"].sort_values().unique().tolist(),
            key="compare_perfume_select",
        )

        row = df_cmp[df_cmp["Label"] == label_pick].iloc[0]

        y_true = row["Prix_Categorie"]

        X_row = pd.DataFrame([{
            "Famille": row.get("Famille", ""),
            "Sous_famille": row.get("Sous_famille", ""),
            "Parfumeur": row.get("Parfumeur", ""),
            "Origine": row.get("Origine", ""),
            "Genre": row.get("Genre", ""),
            "Année": int(row["Année"]) if ("Année" in row and pd.notna(row["Année"])) else 0,
            "Ingredients_txt": str(row.get("Ingredients_txt", "")).strip().lower(),
            "Concepts_txt": str(row.get("Concepts_txt", "")).strip().lower(),
        }])

        y_pred = model.predict(X_row)[0]

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Catégorie réelle", str(y_true))
        with k2:
            st.metric("Catégorie prédite", str(y_pred))
        with k3:
            st.metric("Match ?", "✅ Oui" if str(y_true) == str(y_pred) else "❌ Non")

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_row)[0]
            classes = list(getattr(model, "classes_", []))
            if classes:
                proba_df2 = (
                    pd.DataFrame({"Classe": classes, "Probabilité": proba})
                    .sort_values("Probabilité", ascending=False)
                )
                st.dataframe(proba_df2, use_container_width=True)


#------------------------------------------------------------------------------------------------------------------------------------------


# TAB 3 : Ingrédients & Concepts
with tab3:
    st.subheader("Lister les ingrédients et concepts")


    ing_stats = build_term_stats(df, "Ingredients_txt")
    con_stats = build_term_stats(df, "Concepts_txt")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Parfums", len(df))
    with k2:
        st.metric("Ingrédients", int(len(ing_stats)))
    with k3:
        st.metric("Concepts ", int(len(con_stats)))
    with k4:
        if len(ing_stats) and len(con_stats):
            both = int(len(set(ing_stats["Terme"]).intersection(set(con_stats["Terme"]))))
        else:
            both = 0
        st.metric("Termes communs", both)

    c_ing, c_con = st.columns(2)

    with c_ing:
        st.markdown("### Ingrédients")
        selected_ings = st.multiselect(
            "Sélection",
            options=ing_stats["Terme"].tolist()
            )
        ing_sort = st.selectbox("Trier", ["Fréquence", "A → Z"], key="ing_sort")
        ing_top = st.slider("Afficher", 20, 500, 100, key="ing_top")

        ing_view = ing_stats
        if selected_ings:
            ing_view = ing_view[ing_view["Terme"].isin(selected_ings)]
        if ing_sort == "A → Z":
            ing_view = ing_view.sort_values("Terme", ascending=True)
        else:
            ing_view = ing_view.sort_values(["Parfums", "Occurrences", "Terme"], ascending=[False, False, True])
        show_terms_table(ing_view.head(ing_top), height=520)

        

    with c_con:
        st.markdown("### Concepts")
        selected_cons = st.multiselect(
            "Sélection",
            options=con_stats["Terme"].tolist()
        )

        con_sort = st.selectbox("Trier", ["Fréquence", "A → Z"], key="con_sort")
        con_top = st.slider("Afficher", 20, 500, 100, key="con_top")

        con_view = con_stats
        if selected_cons:
            con_view = con_view[con_view["Terme"].isin(selected_cons)]
        if con_sort == "A → Z":
            con_view = con_view.sort_values("Terme", ascending=True)
        else:
            con_view = con_view.sort_values(["Parfums", "Occurrences", "Terme"], ascending=[False, False, True])
        show_terms_table(con_view.head(con_top), height=520)


#------------------------------------------------------------------------------------------------------------------------------------------


# TAB 4 : Stats
with tab4:
    st.subheader("Statistiques du catalogue")


    c_f1, c_f2, c_f3, c_f4 = st.columns([2, 2, 2, 3])
    with c_f1:
        stats_prix = st.selectbox("Filtrer par catégorie de prix", options(df, "Prix_Categorie"), key="stats_prix")
    with c_f2:
        stats_genre = st.selectbox("Filtrer par genre", options(df, "Genre"), key="stats_genre")
    with c_f3:
        stats_origine = st.selectbox("Filtrer par origine", options(df, "Origine"), key="stats_origine")
    with c_f4:
        top_n = st.slider("Top N (catégories)", 5, 15, 10, key="stats_top_n")

    st.markdown("#### Que voulez-vous consulter ?")
    view = st.selectbox(
        "",
        [
            "Histogramme des années",
            "Répartition des prix",
            "Genre",
            "Origine",
            "Famille",
            "Sous-famille",
        ],
        key="stats_view",
    )

    df_stats = filter_df(
        df,
        {
            "Prix_Categorie": stats_prix,
            "Genre": stats_genre,
            "Origine": stats_origine,
        },
    )

    if "Année" in df_stats.columns:
        a_min, a_max = int(df_stats["Année"].min()), int(df_stats["Année"].max())
        a_range = st.slider("Période", a_min, a_max, (a_min, a_max), key="stats_year_range")
        df_stats = df_stats[(df_stats["Année"] >= a_range[0]) & (df_stats["Année"] <= a_range[1])]

    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Parfums", int(len(df_stats)))
    with k2:
        st.metric("Marques", int(df_stats["Marque"].nunique()) if "Marque" in df_stats.columns else 0)
    with k3:
        st.metric("Origines", int(df_stats["Origine"].nunique()) if "Origine" in df_stats.columns else 0)
    with k4:
        st.metric("Années", int(df_stats["Année"].nunique()) if "Année" in df_stats.columns else 0)


    def _plot_bar(dist_df: pd.DataFrame, title: str):
        if dist_df is None or dist_df.empty:
            st.info("Aucune donnée à afficher.")
            return
        if not _PLOTLY_OK:
            st.bar_chart(dist_df.set_index("Valeur")["Count"], height=360)
            return
        fig = px.bar(
            dist_df,
            x="Count",
            y="Valeur",
            orientation="h",
            text="Count",
            title=title,
            template=_PLOTLY_TEMPLATE,
        )
        fig.update_layout(
            height=480,
            margin=dict(l=10, r=10, t=60, b=10),
            yaxis_title=None,
            xaxis_title=None,
        )
        fig.update_traces(marker_color="#c0392b")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})


    def _year_tick_step(year_min: int, year_max: int) -> int:
        span = max(0, int(year_max) - int(year_min))
        if span <= 25:
            return 1
        if span <= 50:
            return 2
        if span <= 120:
            return 5
        return 10

    if view == "Histogramme des années":
        if "Année" not in df_stats.columns:
            st.info("Colonne Année indisponible.")
        else:
            color_opts = ["Aucun"]
            for c in ["Prix_Categorie", "Genre", "Origine", "Famille"]:
                if c in df_stats.columns:
                    color_opts.append(c)
            c1, c2 = st.columns([2, 2])
            with c1:
                color_by = st.selectbox("Colorer par", color_opts, key="stats_year_color")

            if not _PLOTLY_OK:
                y_df = yearly_counts(df_stats)
                if y_df.empty:
                    st.info("Pas de données année à afficher.")
                else:
                    st.line_chart(y_df.set_index("Année")["Count"], height=320)
            else:
                df_stats_plot = df_stats.copy()
                df_stats_plot["Année"] = pd.to_numeric(df_stats_plot["Année"], errors="coerce")
                df_stats_plot = df_stats_plot.dropna(subset=["Année"])  # évite les ticks bizarres
                df_stats_plot["Année"] = df_stats_plot["Année"].astype(int)

                fig = px.histogram(
                    df_stats_plot,
                    x="Année",
                    color=None if color_by == "Aucun" else color_by,
                    nbins=10,
                    marginal="box",
                    template=_PLOTLY_TEMPLATE,
                    color_discrete_sequence=_PLOTLY_COLORS,
                    title="Distribution des années",
                )
                if "Année" in df_stats_plot.columns and not df_stats_plot.empty:
                    y_min = int(df_stats_plot["Année"].min())
                    y_max = int(df_stats_plot["Année"].max())
                    step = _year_tick_step(y_min, y_max)
                    tickvals = list(range(y_min, y_max + 1, step))
                    fig.update_xaxes(
                        tickmode="array",
                        tickvals=tickvals,
                        ticktext=[str(v) for v in tickvals],
                    )
                fig.update_layout(height=520, margin=dict(l=10, r=10, t=60, b=10))
                st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

                py = price_by_year(df_stats)
                if isinstance(py, pd.DataFrame) and not py.empty:
                    fig2 = px.area(
                        py, template=_PLOTLY_TEMPLATE, 
                        color_discrete_sequence=_PLOTLY_COLORS,
                        title="Catégories de prix par année",)
                    if "Année" in df_stats.columns and not df_stats.empty:
                        y_min = int(pd.to_numeric(df_stats["Année"], errors="coerce").dropna().min())
                        y_max = int(pd.to_numeric(df_stats["Année"], errors="coerce").dropna().max())
                        step = _year_tick_step(y_min, y_max)
                        tickvals = list(range(y_min, y_max + 1, step))
                        fig2.update_xaxes(
                            tickmode="array",
                            tickvals=tickvals,
                            ticktext=[str(v) for v in tickvals],
                        )
                    fig2.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig2, use_container_width=True, config={"displaylogo": False})

    elif view == "Répartition des prix":
        dist = distribution(df_stats, "Prix_Categorie", top_n=top_n).df
        if dist.empty:
            st.info("Colonne Prix_Categorie indisponible.")
        else:
            _plot_bar(dist, "Répartition des catégories de prix")

    elif view == "Genre":
        dist = distribution(df_stats, "Genre", top_n=top_n).df
        if dist.empty:
            st.info("Colonne Genre indisponible.")
        else:
            _plot_bar(dist, "Répartition par genre")

    elif view == "Famille":
        dist = distribution(df_stats, "Famille", top_n=top_n).df
        if dist.empty:
            st.info("Colonne Famille indisponible.")
        else:
            _plot_bar(dist, "Répartition par famille")

    elif view == "Sous-famille":
        dist = distribution(df_stats, "Sous_famille", top_n=top_n).df
        if dist.empty:
            st.info("Colonne Sous_famille indisponible.")
        else:
            _plot_bar(dist, "Répartition par sous-famille")

    else:  # Origine
        st.markdown("### Origine")
        origine_dist = distribution(df_stats, "Origine", top_n=top_n).df
        if origine_dist.empty:
            st.info("Colonne Origine indisponible.")
        else:
            _plot_bar(origine_dist, "Top origines")

            st.caption("Carte (pays colorés)")
            showed_choro = False
            if _PLOTLY_OK:
                ch = origins_choropleth(df_stats, top_n=30)
                if ch is not None and not ch.empty:
                    figm = px.choropleth(
                        ch,
                        locations="iso_alpha",
                        color="Origine",
                        hover_name="Origine",
                        hover_data={"Count": True, "iso_alpha": False},
                        projection="natural earth",
                        template="plotly_dark",
                        color_discrete_sequence=(getattr(px.colors.qualitative, "Set3", []) + _PLOTLY_COLORS)
                        if hasattr(px, "colors")
                        else None,
                    )
                    figm.update_layout(
                        height=520,
                        margin=dict(l=10, r=10, t=10, b=10),
                        legend_title_text=None,
                    )
                    figm.update_geos(
                        showcountries=True,
                        countrycolor="#E9E8E8",
                        showcoastlines=False,
                        showframe=False,
                        bgcolor="#E9E8E8",
                    )
                    st.plotly_chart(figm, use_container_width=True, config={"displaylogo": False})
                    showed_choro = True
                else:
                    st.info(
                        "Impossible de construire la choroplèthe (codes pays manquants). "
                        "Je peux ajouter des correspondances ISO3 si tu me donnes des valeurs exactes de la colonne Origine."
                    )

            if (not _PLOTLY_OK) or (not showed_choro):
                geo = origins_geo(df_stats, top_n=top_n)
                if geo.empty:
                    st.info(
                        "Aucune origine n'a pu être placée sur la carte (libellés non reconnus). "
                        "Dis-moi quelques valeurs exactes de la colonne Origine et j'ajoute les coordonnées."
                    )
                else:
                    st.map(geo, latitude="lat", longitude="lon", size="Count")


#------------------------------------------------------------------------------------------------------------------------------------------


# TAB 5 : Présentation

with tab5:
        st.markdown(
                """
<div class="presentation-hero">
    <div class="presentation-hero-title">Objectif de l’application</div>
    <div class="presentation-hero-subtitle">
        Le prix d’un parfum ne dépend pas uniquement de son odeur ou de sa composition : il est aussi influencé par des éléments
        <b>non observables</b> (notoriété de la marque, marketing…).<br/>
        Cette application propose une lecture <b>objective et analytique</b> du marché du parfum, basée sur des données collectées automatiquement sur le web.
    </div>
    <div class="presentation-badges">
        <span class="presentation-pill accent">Machine Learning</span>
        <span class="presentation-pill">Données Web</span>
        <span class="presentation-pill">Analyse</span>
    </div>
</div>
                """,
                unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1.45, 1])
        with c1:
                st.markdown(
                        """
<div class="presentation-card">
    <h3>Que fait le modèle de Machine Learning ?</h3>
    <p class="presentation-muted">
        À partir des caractéristiques intrinsèques des parfums (famille olfactive, ingrédients, concepts, origine, année, genre…),
        le modèle prédit une <b>catégorie de prix</b>.
    </p>
    <div class="presentation-badges" style="margin-top: 12px;">
        <span class="presentation-pill">Mass market</span>
        <span class="presentation-pill">Prestige</span>
        <span class="presentation-pill">Niche</span>
    </div>
    <p class="presentation-muted" style="margin-top: 12px;">
        La <b>marque</b> est volontairement exclue du modèle afin d’éviter un biais lié au branding et de se concentrer sur le produit lui-même.
    </p>
</div>
                        """,
                        unsafe_allow_html=True,
                )

        with c2:
                st.markdown(
                        """
<div class="presentation-card">
    <h3>À quoi ça sert ?</h3>
    <ul>
        <li>Comparer des parfums sur une base <b>neutre</b> et standardisée</li>
        <li>Repérer des parfums <b>sur-</b> ou <b>sous-positionnés</b> en termes de prix</li>
        <li>Mieux comprendre la <b>segmentation économique</b> du marché</li>
        <li>Tester le positionnement théorique d’un parfum <b>indépendamment</b> de sa marque</li>
    </ul>
</div>
                        """,
                        unsafe_allow_html=True,
                )

        st.markdown("## Comment utiliser l’application ?")

        s1, s2, s5, s3, s4 = st.columns(5)
        with s1:
                st.markdown(
                        """
<div class="presentation-step">
    <div class="presentation-step-title">🔎 Explorer</div>
    <p class="presentation-step-text">Parcourir et filtrer le catalogue de parfums.</p>
</div>
                        """,
                        unsafe_allow_html=True,
                )
        with s2:
                st.markdown(
                        """
<div class="presentation-step">
    <div class="presentation-step-title">🔮 Prédire </div>
    <p class="presentation-step-text">Estimer la catégorie de prix à partir des caractéristiques du parfum.</p>
</div>
                        """,
                        unsafe_allow_html=True,
                )

        with s5:
                st.markdown(
                        """
<div class="presentation-step">
    <div class="presentation-step-title">🔮 Comparer</div>
    <p class="presentation-step-text">Confronter la catégorie réelle d’un parfum à celle prédite par le modèle.</p>
</div>
                        """,
                        unsafe_allow_html=True,
                )
        with s3:
                st.markdown(
                        """
<div class="presentation-step">
    <div class="presentation-step-title">🧾 Ingrédients / Concepts</div>
    <p class="presentation-step-text">Liste des ingrédients et concepts associés aux parfums.</p>
</div>
                        """,
                        unsafe_allow_html=True,
                )
        with s4:
                st.markdown(
                        """
<div class="presentation-step">
    <div class="presentation-step-title">📊 Statistiques</div>
    <p class="presentation-step-text">Analyser la structure, les tendances du marcher.</p>
</div>
                        """,
                        unsafe_allow_html=True,
                )

st.divider()
with st.container():
        st.warning(
                "Les résultats fournis sont des estimations analytiques et ne constituent pas des prix de vente réels."
        )