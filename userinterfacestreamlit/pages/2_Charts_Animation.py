import streamlit as st
import os
import pandas as pd
import plotly.express as px

from utils.charts import (
    bar_chart,
    line_chart,
    scatter_chart,
    pie_chart,
    heatmap_corr,
    scatter_3d_chart,
    animated_bar_chart,
    animated_scatter_chart,
    bar_race_chart,
    line_with_forecast,
)

st.set_page_config(
    page_title="Smart Analytics & Charts | Auto Data Explorer",
    layout="wide"
)

# ================== Common helpers ==================

def load_css():
    css_files = ["assets/style.css", "assets/animation.css"]
    for css in css_files:
        if os.path.exists(css):
            with open(css) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_chart_with_download(fig, name: str):
    """Show chart + download button (user friendly)."""
    st.plotly_chart(fig, use_container_width=True)
    html_bytes = fig.to_html(full_html=False, include_plotlyjs="cdn").encode("utf-8")
    st.download_button(
        label="⬇ Download chart (HTML)",
        data=html_bytes,
        file_name=f"{name}.html",
        mime="text/html",
    )


def _filter_single(df: pd.DataFrame, col: str, op: str, val):
    """One filter – like df.loc[…]"""
    try:
        if op == "==":
            return df.loc[df[col] == val]
        if op == "!=":
            return df.loc[df[col] != val]
        if op == ">":
            return df.loc[df[col] > val]
        if op == "<":
            return df.loc[df[col] < val]
        if op == ">=":
            return df.loc[df[col] >= val]
        if op == "<=":
            return df.loc[df[col] <= val]
        if op == "contains":
            return df.loc[df[col].astype(str).str.contains(str(val), case=False, na=False)]
    except Exception:
        return df
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Simple 2-filter panel, but concept = df.loc[…]"""
    with st.expander("🔎 Optional Filters (uses loc-style idea)", expanded=False):
        st.caption("Example logic: df.loc[df['Gender'] == 'Male']")

        # Filter 1
        enable_1 = st.checkbox("Enable Filter 1")
        if enable_1:
            c1, c2, c3 = st.columns(3)
            with c1:
                f1_col = st.selectbox("Column 1", df.columns, key="f1_col")
            with c2:
                f1_op = st.selectbox("Operator 1", ["==", "!=", ">", "<", ">=", "<=", "contains"], key="f1_op")
            with c3:
                if pd.api.types.is_numeric_dtype(df[f1_col]):
                    f1_val = st.number_input("Value 1", key="f1_val")
                else:
                    f1_val = st.text_input("Value 1", key="f1_val")

            df = _filter_single(df, f1_col, f1_op, f1_val)

        # Filter 2
        enable_2 = st.checkbox("Enable Filter 2")
        if enable_2:
            c1, c2, c3 = st.columns(3)
            with c1:
                f2_col = st.selectbox("Column 2", df.columns, key="f2_col")
            with c2:
                f2_op = st.selectbox("Operator 2", ["==", "!=", ">", "<", ">=", "<=", "contains"], key="f2_op")
            with c3:
                if pd.api.types.is_numeric_dtype(df[f2_col]):
                    f2_val = st.number_input("Value 2", key="f2_val")
                else:
                    f2_val = st.text_input("Value 2", key="f2_val")

            df = _filter_single(df, f2_col, f2_op, f2_val)

    return df


# ================== PAGE START ==================

load_css()

st.markdown("<h1 class='page-title slide-in'>📈 Smart Analytics & Charts</h1>", unsafe_allow_html=True)
st.caption("Upload • Analyze • Visualize – A fast business insights platform")

if "df" not in st.session_state:
    st.warning("⚠️ No dataset found. Please upload a file in the **Home** page first.")
    st.stop()

df = st.session_state["df"]

numeric_cols = df.select_dtypes(include="number").columns.tolist()
all_cols = df.columns.tolist()
cat_cols = [c for c in all_cols if c not in numeric_cols]

if not all_cols:
    st.error("Dataset has no columns.")
    st.stop()

st.markdown("<div class='glass-card animated-float'>", unsafe_allow_html=True)

# ============= STEP 1 – Select Mode (Simple) =============

mode = st.radio(
    "🧠 What do you want to do?",
    [
        "⭐ Auto Analysis (recommended)",
        "📊 Simple Chart",
        "📌 Group & Aggregate (sum / mean / count)",
        "📈 Pivot Table (rows × columns × values)",
        "🎞 Advanced / Animated Charts",
    ],
    horizontal=False,
)

# =========================================================
# MODE 1 – AUTO ANALYSIS (Beginner friendly, 1-click)
# =========================================================
if mode.startswith("⭐ Auto Analysis"):
    st.subheader("⭐ Auto Analysis – important insights in one click")

    work_df = apply_filters(df.copy())

    # ---------- Basic summary (table, not a chart) ----------
    st.write("### 1) Basic summary of your data")
    st.write(f"Rows: {work_df.shape[0]} | Columns: {work_df.shape[1]}")

    try:
        desc = work_df.describe(include="all").T
    except Exception:
        desc = work_df.describe().T
    st.dataframe(desc)

    st.write("---")
    st.write("### 2) Auto generated charts (simple to read)")

    # Detect column types again for safety
    num_cols = work_df.select_dtypes(include="number").columns.tolist()
    cat_cols = [c for c in work_df.columns if c not in num_cols]

    # Common index for some charts
    if len(work_df) > 0:
        work_df["Auto_Index"] = range(len(work_df))

    chart_no = 1  # for chart numbering

    # ---------- Chart 1: Histogram ----------
    if num_cols:
        col = num_cols[0]
        st.write(f"#### Chart {chart_no}: Histogram of `{col}`")
        st.caption("Shows how the values of this column are spread.")
        fig = px.histogram(work_df, x=col, nbins=20)
        show_chart_with_download(fig, f"AUTO_hist_{col}")
        chart_no += 1

    # ---------- Chart 2: Density (KDE style) ----------
    if num_cols:
        col = num_cols[0]
        st.write(f"#### Chart {chart_no}: Density of `{col}`")
        st.caption("Smooth curve that shows where most values are concentrated.")
        fig = px.density_contour(work_df, x=col)
        show_chart_with_download(fig, f"AUTO_density_{col}")
        chart_no += 1

    # ---------- Chart 3: Box Plot (Outliers) ----------
    if num_cols:
        col = num_cols[0]
        st.write(f"#### Chart {chart_no}: Box plot of `{col}`")
        st.caption("Helps you see minimum, maximum, median and outliers.")
        fig = px.box(work_df, y=col)
        show_chart_with_download(fig, f"AUTO_box_{col}")
        chart_no += 1

    # ---------- Chart 4: Trend Line over index ----------
    if num_cols and "Auto_Index" in work_df.columns:
        col = num_cols[0]
        st.write(f"#### Chart {chart_no}: Trend of `{col}` over data order")
        st.caption("Shows whether values go up or down as we move through the rows.")
        fig = px.line(work_df, x="Auto_Index", y=col)
        show_chart_with_download(fig, f"AUTO_trend_{col}")
        chart_no += 1

    # ---------- Chart 5: Area Chart ----------
    if num_cols and "Auto_Index" in work_df.columns:
        col = num_cols[0]
        st.write(f"#### Chart {chart_no}: Area chart of `{col}`")
        st.caption("Similar to a line chart, but filled area makes pattern more visible.")
        fig = px.area(work_df, x="Auto_Index", y=col)
        show_chart_with_download(fig, f"AUTO_area_{col}")
        chart_no += 1

    # ---------- Chart 6: Numeric vs Numeric Scatter ----------
    if len(num_cols) >= 2:
        x_col, y_col = num_cols[0], num_cols[1]
        st.write(f"#### Chart {chart_no}: Relationship between `{x_col}` and `{y_col}`")
        st.caption("Each point shows how these two number columns move together.")
        fig = px.scatter(work_df, x=x_col, y=y_col)
        show_chart_with_download(fig, f"AUTO_scatter_{x_col}_{y_col}")
        chart_no += 1

    # ---------- Chart 7: Bubble Chart ----------
    if len(num_cols) >= 3:
        x_col, y_col, size_col = num_cols[0], num_cols[1], num_cols[2]
        st.write(f"#### Chart {chart_no}: Bubble chart using `{x_col}`, `{y_col}`, `{size_col}`")
        st.caption("Bigger bubbles mean larger values in the size column.")
        fig = px.scatter(work_df, x=x_col, y=y_col, size=size_col, size_max=40, opacity=0.8)
        show_chart_with_download(fig, f"AUTO_bubble_{x_col}_{y_col}_{size_col}")
        chart_no += 1

    # ---------- Chart 8: Correlation Heatmap ----------
    if len(num_cols) >= 2:
        st.write(f"#### Chart {chart_no}: Correlation heatmap")
        st.caption("Shows which numeric columns are strongly related to each other.")
        fig = heatmap_corr(work_df)
        if fig:
            show_chart_with_download(fig, "AUTO_heatmap")
        chart_no += 1

    # ---------- Chart 9: Scatter Matrix (Mini pair-plot) ----------
    if len(num_cols) >= 3:
        st.write(f"#### Chart {chart_no}: Scatter matrix of numeric columns")
        st.caption("Multiple scatter plots to compare all numeric columns together.")
        fig = px.scatter_matrix(work_df[num_cols[:4]])
        show_chart_with_download(fig, "AUTO_scatter_matrix")
        chart_no += 1

    # ---------- Chart 10: Top 10 categories (Bar) ----------
    if cat_cols:
        cat = cat_cols[0]
        st.write(f"#### Chart {chart_no}: Top 10 values in `{cat}`")
        st.caption("Shows which categories appear most often.")
        vc = work_df[cat].value_counts().head(10).reset_index()
        vc.columns = [cat, "Count"]
        fig = px.bar(vc, x=cat, y="Count")
        show_chart_with_download(fig, f"AUTO_top10_{cat}")
        chart_no += 1

    # ---------- Chart 11: Top 5 categories (Pie) ----------
    if cat_cols:
        cat = cat_cols[0]
        st.write(f"#### Chart {chart_no}: Share of top 5 values in `{cat}`")
        st.caption("Pie chart that shows the proportion of main categories.")
        vc = work_df[cat].value_counts().head(5).reset_index()
        vc.columns = [cat, "Count"]
        fig = px.pie(vc, names=cat, values="Count", hole=0.3)
        show_chart_with_download(fig, f"AUTO_pie_{cat}")
        chart_no += 1

    # ---------- Chart 12: Category-wise SUM ----------
    if cat_cols and num_cols:
        cat, num = cat_cols[0], num_cols[0]
        st.write(f"#### Chart {chart_no}: Total `{num}` by `{cat}`")
        st.caption("Shows which category contributes the highest total value.")
        g = work_df.groupby(cat)[num].sum().reset_index()
        fig = px.bar(g, x=cat, y=num)
        show_chart_with_download(fig, f"AUTO_sum_{cat}_{num}")
        chart_no += 1

    # ---------- Chart 13: Category-wise AVERAGE ----------
    if cat_cols and num_cols:
        cat, num = cat_cols[0], num_cols[0]
        st.write(f"#### Chart {chart_no}: Average `{num}` by `{cat}`")
        st.caption("Shows which category has higher or lower average value.")
        g = work_df.groupby(cat)[num].mean().reset_index()
        g.rename(columns={num: f"Avg_{num}"}, inplace=True)
        fig = px.bar(g, x=cat, y=f"Avg_{num}")
        show_chart_with_download(fig, f"AUTO_avg_{cat}_{num}")
        chart_no += 1

    # ---------- Chart 14: Stacked bar (2 categories) ----------
    if len(cat_cols) >= 2 and num_cols:
        cat1, cat2, num = cat_cols[0], cat_cols[1], num_cols[0]
        st.write(f"#### Chart {chart_no}: Stacked bar of `{num}` by `{cat1}` and `{cat2}`")
        st.caption("Shows how a second category is distributed inside each main category.")
        fig = px.bar(work_df, x=cat1, y=num, color=cat2)
        show_chart_with_download(fig, f"AUTO_stacked_{cat1}_{cat2}_{num}")
        chart_no += 1

    # ---------- Chart 15: Simple forecast line ----------
    if num_cols and "Auto_Index" in work_df.columns:
        num = num_cols[0]
        st.write(f"#### Chart {chart_no}: Simple forecast of `{num}` (next few points)")
        st.caption("Line with basic prediction based on the current pattern.")
        # Use Auto_Index as x for forecast
        fig = line_with_forecast(work_df, "Auto_Index", num, periods=10)
        show_chart_with_download(fig, f"AUTO_forecast_{num}")
        chart_no += 1




# =========================================================
# MODE 2 – SIMPLE CHART (any chart, very easy)
# =========================================================
elif mode.startswith("📊 Simple Chart"):
    st.subheader("📊 Simple Chart Builder (any chart in 3 clicks)")

    work_df = apply_filters(df.copy())

    chart_kind = st.selectbox(
        "Choose chart type",
        ["Bar", "Line", "Scatter", "Pie"],
    )

    if chart_kind == "Pie":
        if not numeric_cols or not cat_cols:
            st.error("Pie needs one category + one numeric column.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                names_col = st.selectbox("Category (names)", cat_cols)
            with c2:
                values_col = st.selectbox("Values (numeric)", numeric_cols)

            if st.button("Generate Pie Chart"):
                fig = pie_chart(work_df, names_col=names_col, values_col=values_col)
                show_chart_with_download(fig, "simple_pie")
    else:
        if not numeric_cols:
            st.error("Need at least one numeric column for Bar/Line/Scatter.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                x_col = st.selectbox("X-axis", all_cols)
            with c2:
                y_col = st.selectbox("Y-axis (numeric)", numeric_cols)

            color_col = None
            if chart_kind == "Scatter":
                color_col = st.selectbox("Color by (optional)", [None] + all_cols)

            if st.button("Generate Chart"):
                if chart_kind == "Bar":
                    fig = bar_chart(work_df, x_col, y_col)
                    name = "simple_bar"
                elif chart_kind == "Line":
                    fig = line_chart(work_df, x_col, y_col)
                    name = "simple_line"
                else:
                    fig = scatter_chart(work_df, x_col, y_col, color_col)
                    name = "simple_scatter"

                show_chart_with_download(fig, name)

# =========================================================
# MODE 3 – GROUP & AGG (age-wise, gender-wise, etc.)
# =========================================================
elif mode.startswith("📌 Group & Aggregate"):
    st.subheader("📌 Group & Aggregate – age-wise / gender-wise / city-wise etc.")

    work_df = apply_filters(df.copy())

    group_col = st.selectbox("Group by (category column)", all_cols)
    if not numeric_cols:
        st.error("At least one numeric column needed for aggregation.")
    else:
        value_col = st.selectbox("Numeric column", numeric_cols)
        agg_func = st.selectbox("Aggregation", ["sum", "mean", "count", "min", "max", "median"])

        if st.button("Run Group & Aggregate"):
            # pandas groupby + agg
            st.code(
                f"df.groupby('{group_col}')['{value_col}'].agg('{agg_func}')",
                language="python"
            )
            agg = work_df.groupby(group_col)[value_col].agg(agg_func).reset_index()
            agg.columns = [group_col, f"{agg_func}_{value_col}"]

            st.write("📋 Result of groupby + agg")
            st.dataframe(agg)

            # chart
            st.write("📊 Chart")
            fig = bar_chart(agg, x_col=group_col, y_col=f"{agg_func}_{value_col}")
            show_chart_with_download(fig, "group_agg_chart")

# =========================================================
# MODE 4 – PIVOT TABLE (Excel / PowerBI feel)
# =========================================================
elif mode.startswith("📈 Pivot Table"):
    st.subheader("📈 Pivot Table – rows × columns × values")

    work_df = apply_filters(df.copy())

    if not numeric_cols:
        st.error("Need at least one numeric column for pivot.")
    else:
        row_col = st.selectbox("Rows (index)", all_cols, key="pv_row")
        col_col = st.selectbox("Columns", all_cols, key="pv_col")
        val_col = st.selectbox("Values (numeric)", numeric_cols, key="pv_val")
        aggfunc = st.selectbox("Aggregation", ["sum", "mean", "count", "min", "max", "median"])

        if st.button("Generate Pivot Table"):
            st.code(
                f"pd.pivot_table(df, index='{row_col}', columns='{col_col}', "
                f"values='{val_col}', aggfunc='{aggfunc}')",
                language="python",
            )
            pv = pd.pivot_table(
                work_df,
                index=row_col,
                columns=col_col,
                values=val_col,
                aggfunc=aggfunc,
            )
            st.write("📋 Pivot result")
            st.dataframe(pv)

            # heatmap chart
            st.write("📊 Pivot Heatmap")
            fig = px.imshow(
                pv,
                aspect="auto",
                text_auto=True,
                color_continuous_scale="Blues",
                origin="lower",
            )
            fig.update_layout(transition_duration=500)
            show_chart_with_download(fig, "pivot_heatmap")

# =========================================================
# MODE 5 – ADVANCED / ANIMATED
# =========================================================
elif mode.startswith("🎞 Advanced"):
    st.subheader("🎞 Advanced & Animated Charts")

    work_df = apply_filters(df.copy())

    sub = st.selectbox(
        "Select advanced chart type",
        [
            "Correlation Heatmap",
            "3D Scatter",
            "Animated Bar",
            "Animated Scatter",
            "Bar Race",
            "Line + Forecast",
        ],
    )

    if sub == "Correlation Heatmap":
        if len(numeric_cols) < 2:
            st.error("Need at least 2 numeric columns.")
        else:
            if st.button("Generate Heatmap"):
                fig = heatmap_corr(work_df)
                if fig:
                    show_chart_with_download(fig, "adv_heatmap")

    elif sub == "3D Scatter":
        if len(numeric_cols) < 3:
            st.error("Need at least 3 numeric columns for 3D scatter.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                x_col = st.selectbox("X-axis", numeric_cols, key="adv3_x")
            with c2:
                y_col = st.selectbox("Y-axis", [c for c in numeric_cols if c != x_col], key="adv3_y")
            with c3:
                z_col = st.selectbox(
                    "Z-axis",
                    [c for c in numeric_cols if c not in [x_col, y_col]],
                    key="adv3_z",
                )
            color_col = st.selectbox("Color by (optional)", [None] + all_cols)

            if st.button("Generate 3D Scatter"):
                fig = scatter_3d_chart(work_df, x_col, y_col, z_col, color_col)
                show_chart_with_download(fig, "adv_3d_scatter")

    elif sub in ["Animated Bar", "Animated Scatter", "Bar Race"]:
        if len(numeric_cols) < 1 or len(all_cols) < 2:
            st.error("Need more columns for animated charts.")
        else:
            frame_col = st.selectbox("Frame (time/step)", all_cols, key="adv_frame")
            c1, c2 = st.columns(2)
            with c1:
                x_col = st.selectbox("X-axis", all_cols, key="adv_anim_x")
            with c2:
                y_col = st.selectbox("Y-axis (numeric)", numeric_cols, key="adv_anim_y")

            size_col = None
            color_col = None
            if sub == "Animated Scatter":
                size_col = st.selectbox("Size by (optional numeric)", [None] + numeric_cols)
                color_col = st.selectbox("Color by (optional)", [None] + all_cols)

            if st.button("Generate Animated Chart"):
                if sub == "Animated Bar":
                    fig = animated_bar_chart(work_df, x_col, y_col, frame_col)
                    name = "adv_animated_bar"
                elif sub == "Bar Race":
                    fig = bar_race_chart(work_df, x_col, y_col, frame_col)
                    name = "adv_bar_race"
                else:
                    fig = animated_scatter_chart(
                        work_df,
                        x_col,
                        y_col,
                        frame_col,
                        size_col=size_col,
                        color_col=color_col,
                    )
                    name = "adv_animated_scatter"

                show_chart_with_download(fig, name)

    elif sub == "Line + Forecast":
        if not numeric_cols:
            st.error("Need at least one numeric column.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                x_col = st.selectbox("X-axis (time/index)", all_cols, key="adv_for_x")
            with c2:
                y_col = st.selectbox("Y-axis (numeric)", numeric_cols, key="adv_for_y")

            periods = st.slider("Future points (forecast length)", 3, 30, 10)

            if st.button("Generate Forecast Line"):
                fig = line_with_forecast(work_df, x_col, y_col, periods=periods)
                show_chart_with_download(fig, "adv_line_forecast")

st.markdown("</div>", unsafe_allow_html=True)
