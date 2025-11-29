import streamlit as st
from utils.analysis import (
    get_basic_info,
    get_missing_values,
    get_column_types,
    get_descriptive_stats,
)

import os

st.set_page_config(page_title="Data Overview | Auto Data Explorer", layout="wide")

def load_css():
    css_files = ["assets/style.css", "assets/animation.css"]
    for css in css_files:
        if os.path.exists(css):
            with open(css) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 class='page-title slide-in'>📊 Data Overview</h1>", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.warning("⚠️ No dataset found. Please upload a file in the **Home** page first.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state.get("file_name", "Uploaded Dataset")

st.markdown(f"<p class='subtitle'>File: <b>{file_name}</b></p>", unsafe_allow_html=True)

basic = get_basic_info(df)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='glass-card animated-float'>", unsafe_allow_html=True)
    st.write("### 📏 Shape")
    st.write(f"Rows: {basic['rows']}")
    st.write(f"Columns: {basic['columns']}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card animated-float'>", unsafe_allow_html=True)
    st.write("### 🧾 Columns")
    st.write(basic["column_names"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 🔍 Data Preview")
st.dataframe(df.head())

with st.expander("📌 Column Types"):
    st.dataframe(get_column_types(df))

with st.expander("❗ Missing Values"):
    st.dataframe(get_missing_values(df))

with st.expander("📊 Descriptive Statistics"):
    st.dataframe(get_descriptive_stats(df))
