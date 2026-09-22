from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "outputs" / "agetech_regional" / "harmonized" / "regional.parquet"

st.set_page_config(page_title="AgeTech Regional Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.warning(
            "No se encontró la salida armonizada. Descarga los microdatos autorizados de SABE y MHAS, colócalos en la estructura local indicada en el README y ejecuta el pipeline antes de abrir el dashboard."
        )
        return pd.DataFrame()

    df = pd.read_parquet(DATA_PATH)
    df = df.copy()
    df["value_numeric"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    source_options = ["All"] + sorted(df["source"].dropna().unique().tolist())
    selected_source = st.sidebar.selectbox("Fuente", source_options)
    selected_variable = st.sidebar.selectbox(
        "Variable canónica",
        ["All"] + sorted(df["variable_canonical"].dropna().unique().tolist()),
    )
    selected_window = st.sidebar.selectbox(
        "Ventana temporal",
        ["All"] + sorted(df["time_window"].dropna().unique().tolist()),
    )

    filtered = df.copy()
    if selected_source != "All":
        filtered = filtered[filtered["source"] == selected_source]
    if selected_variable != "All":
        filtered = filtered[filtered["variable_canonical"] == selected_variable]
    if selected_window != "All":
        filtered = filtered[filtered["time_window"] == selected_window]
    return filtered


def render_summary(df: pd.DataFrame) -> None:
    cols = st.columns(4)
    cols[0].metric("Filas", f"{len(df):,}")
    cols[1].metric("Fuentes", df["source"].nunique())
    cols[2].metric("Variables canónicas", df["variable_canonical"].nunique())
    cols[3].metric("Ventanals", df["time_window"].nunique())


def render_charts(df: pd.DataFrame) -> None:
    source_counts = df["source"].value_counts().reset_index()
    source_counts.columns = ["source", "count"]
    fig_source = px.bar(
        source_counts,
        x="source",
        y="count",
        color="source",
        title="Registros por fuente",
        template="plotly_white",
    )
    st.plotly_chart(fig_source, use_container_width=True)

    variable_counts = df["variable_canonical"].value_counts().reset_index().head(10)
    variable_counts.columns = ["variable_canonical", "count"]
    fig_variable = px.bar(
        variable_counts,
        x="count",
        y="variable_canonical",
        orientation="h",
        color="variable_canonical",
        title="Top variables canónicas",
        template="plotly_white",
    )
    st.plotly_chart(fig_variable, use_container_width=True)

    comparable_counts = df["comparable"].value_counts(dropna=False).reset_index()
    comparable_counts.columns = ["comparable", "count"]
    fig_compare = px.pie(
        comparable_counts,
        names="comparable",
        values="count",
        title="Variables comparables vs no comparables",
        hole=0.35,
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    time_counts = df["time_window"].value_counts(dropna=False).reset_index()
    time_counts.columns = ["time_window", "count"]
    fig_time = px.bar(
        time_counts,
        x="time_window",
        y="count",
        color="time_window",
        title="Ventanas temporales presentes",
        template="plotly_white",
    )
    st.plotly_chart(fig_time, use_container_width=True)

    st.subheader("Distribución de una variable seleccionada")
    variable_choice = st.selectbox(
        "Elegir variable para inspección",
        sorted(df["variable_canonical"].dropna().unique().tolist()),
    )
    selected = df[df["variable_canonical"] == variable_choice].copy()
    numeric_vals = selected["value_numeric"].dropna()
    if not numeric_vals.empty:
        hist = px.histogram(
            selected,
            x="value_numeric",
            nbins=30,
            color="source",
            title=f"Distribución numérica de {variable_choice}",
            template="plotly_white",
        )
        st.plotly_chart(hist, use_container_width=True)
    else:
        counts = selected["value"].dropna().astype(str).value_counts().reset_index()
        counts.columns = ["value", "count"]
        fig_values = px.bar(
            counts.head(15),
            x="value",
            y="count",
            title=f"Frecuencia de valores para {variable_choice}",
            template="plotly_white",
        )
        st.plotly_chart(fig_values, use_container_width=True)


def main() -> None:
    st.title("AgeTech Regional Results Explorer")
    st.caption("Visualización del parquet armonizado de SABE y MHAS")

    df = load_data()
    filtered = render_filters(df)
    render_summary(filtered)

    with st.expander("Ver tabla filtrada", expanded=False):
        st.dataframe(filtered.head(200), use_container_width=True)

    render_charts(filtered)

    st.subheader("Resumen técnico")
    st.write(
        "Este dashboard lee la salida armonizada en "
        f"`{DATA_PATH}` y permite explorar la estructura regional antes de modelar."
    )


if __name__ == "__main__":
    main()
