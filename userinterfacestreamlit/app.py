import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Auto Data Explorer",
    page_icon="📊",
    layout="wide"
)

# ===== Helper: Load CSS =====
def load_css():
    css_files = ["assets/style.css", "assets/animation.css"]
    for css in css_files:
        if os.path.exists(css):
            with open(css) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ===== Sidebar =====
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>⚙️ Controls</h2>", unsafe_allow_html=True)
    st.write("1. Upload CSV / Excel file")
    st.write("2. Go to pages: Data Overview, Charts, Summary Report")
    st.markdown("---")
    st.write("👨‍💻 *Project: Auto Data Explorer*")

st.markdown("<h1 class='main-title'>📊 Auto Data Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload • Analyze • Visualize – All in one place</p>", unsafe_allow_html=True)

# ===== File Uploader =====
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
    help="Choose any tabular dataset file"
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state["df"] = df
        st.session_state["file_name"] = uploaded_file.name

        st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.write("### 👀 Quick Preview")
        st.dataframe(df.head())
        st.write("**Shape:** ", df.shape)
        st.markdown("</div>", unsafe_allow_html=True)

        st.info("➡️ Now go to **Data Overview**, **Charts & Animation**, or **Summary Report** from the left sidebar `Pages` section.")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.markdown(
        """
        <div class='glass-card animated-pulse'>
            <h3>🚀 Start Here</h3>
            <p>Upload any CSV/Excel file to begin automatic exploration.</p>
            <ul>
                <li>Preview your data</li>
                <li>Check summary & missing values</li>
                <li>Create animated charts</li>
                <li>Download PDF summary report</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
