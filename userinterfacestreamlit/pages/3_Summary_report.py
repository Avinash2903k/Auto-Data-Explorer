import streamlit as st
import os
from utils.report import generate_pdf_report
from utils.analysis import get_basic_info

st.set_page_config(page_title="Summary Report | Auto Data Explorer", layout="wide")

def load_css():
    css_files = ["assets/style.css", "assets/animation.css"]
    for css in css_files:
        if os.path.exists(css):
            with open(css) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 class='page-title slide-in'>📑 Summary Report</h1>", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.warning("⚠️ No dataset found. Please upload a file in the **Home** page first.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state.get("file_name", "Uploaded Dataset")

info = get_basic_info(df)

st.markdown("<div class='glass-card animated-float'>", unsafe_allow_html=True)
st.write(f"### 🗂 File: **{file_name}**")
st.write(f"Rows: {info['rows']} | Columns: {info['columns']}")
st.markdown("</div>", unsafe_allow_html=True)

default_summary = f"""
This report summarizes the dataset **{file_name}**.

- Total rows: {info['rows']}
- Total columns: {info['columns']}
- Columns: {', '.join(info['column_names'][:10])}{'...' if len(info['column_names']) > 10 else ''}

Key insights:
- Add your observations about outliers, trends, and patterns.
- Mention any business-related insights from charts.
"""

summary_text = st.text_area(
    "✏️ Edit your summary (this will go into the PDF):",
    value=default_summary,
    height=200
)

if st.button("📄 Generate PDF Report"):
    pdf_buffer = generate_pdf_report(df, summary_text)
    st.success("✅ PDF report generated! Download below.")
    st.download_button(
        label="⬇️ Download Report",
        data=pdf_buffer,
        file_name="data_summary_report.pdf",
        mime="application/pdf"
    )
