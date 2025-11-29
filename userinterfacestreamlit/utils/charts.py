import plotly.express as px
import pandas as pd
import numpy as np

# ========== Basic Charts ==========

def bar_chart(df: pd.DataFrame, x_col: str, y_col: str):
    fig = px.bar(df, x=x_col, y=y_col)
    fig.update_layout(transition_duration=500)
    return fig

def line_chart(df: pd.DataFrame, x_col: str, y_col: str):
    fig = px.line(df, x=x_col, y=y_col)
    fig.update_traces(mode="lines+markers")
    fig.update_layout(transition_duration=500)
    return fig

def scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, color_col: str | None = None):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
    fig.update_traces(marker=dict(size=9, opacity=0.8))
    fig.update_layout(transition_duration=500)
    return fig

def pie_chart(df: pd.DataFrame, names_col: str, values_col: str):
    fig = px.pie(df, names=names_col, values=values_col, hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# ========== Advanced Charts ==========

def heatmap_corr(df: pd.DataFrame):
    num_df = df.select_dtypes(include="number")
    if num_df.shape[1] < 2:
        return None

    corr = num_df.corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu"
    )
    fig.update_layout(
        title="Correlation Heatmap",
        transition_duration=500
    )
    return fig

def scatter_3d_chart(df: pd.DataFrame, x_col: str, y_col: str, z_col: str, color_col: str | None = None):
    fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, color=color_col)
    fig.update_traces(marker=dict(size=5, opacity=0.8))
    fig.update_layout(
        title="3D Scatter",
        transition_duration=600
    )
    return fig

# ========== Animated Charts ==========

def animated_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, frame_col: str):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        animation_frame=frame_col,
        range_y=[0, df[y_col].max() * 1.2]
    )
    fig.update_layout(
        transition={'duration': 600, 'easing': 'cubic-in-out'},
        xaxis_title=x_col,
        yaxis_title=y_col,
    )
    return fig

def bar_race_chart(df: pd.DataFrame, x_col: str, y_col: str, frame_col: str):
    # sort by frame + value for smooth race
    df_sorted = df.sort_values(by=[frame_col, y_col])
    fig = px.bar(
        df_sorted,
        x=x_col,
        y=y_col,
        color=x_col,
        animation_frame=frame_col,
        range_y=[0, df[y_col].max() * 1.2]
    )
    fig.update_layout(
        transition={'duration': 700, 'easing': 'cubic-in-out'},
        xaxis_title=x_col,
        yaxis_title=y_col,
    )
    return fig

def animated_scatter_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    frame_col: str,
    size_col: str | None = None,
    color_col: str | None = None,
):
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        animation_frame=frame_col,
        size=size_col if size_col else None,
        color=color_col if color_col else None,
        size_max=40,
        opacity=0.8
    )
    fig.update_layout(
        transition={'duration': 600, 'easing': 'cubic-in-out'},
        xaxis_title=x_col,
        yaxis_title=y_col,
    )
    return fig

# ========== Simple Forecast (Line + Prediction) ==========

def line_with_forecast(df: pd.DataFrame, x_col: str, y_col: str, periods: int = 10):
    """
    Simple forecast using linear regression (numpy polyfit).
    Not hardcore ML, but interview ku explain panna easy.
    """
    temp = df[[x_col, y_col]].dropna()
    if temp.empty:
        # fallback to normal line chart
        return line_chart(df, x_col, y_col)

    x = temp[x_col]
    y = temp[y_col].astype(float).values

    # x numeric / datetime / others handle pannrom
    if np.issubdtype(x.dtype, np.number):
        x_idx = x.values.astype(float)
    else:
        x_idx = np.arange(len(x), dtype=float)

    # linear fit
    try:
        m, b = np.polyfit(x_idx, y, deg=1)
    except Exception:
        return line_chart(df, x_col, y_col)

    last_idx = x_idx[-1]
    future_idx = np.arange(last_idx + 1, last_idx + periods + 1, dtype=float)
    future_y = m * future_idx + b

    # future x build
    if np.issubdtype(x.dtype, np.number):
        future_x = future_idx
    elif np.issubdtype(x.dtype, np.datetime64):
        step = (x.iloc[-1] - x.iloc[0]) / max(len(x) - 1, 1)
        future_x = [x.iloc[-1] + step * (i + 1) for i in range(periods)]
    else:
        future_x = [f"{x_col}_t+{i+1}" for i in range(periods)]

    hist_df = pd.DataFrame({"x": x, "y": y, "type": "History"})
    fut_df = pd.DataFrame({"x": future_x, "y": future_y, "type": "Forecast"})

    plot_df = pd.concat([hist_df, fut_df], ignore_index=True)

    fig = px.line(plot_df, x="x", y="y", color="type")
    fig.update_traces(mode="lines+markers")
    fig.update_layout(
        title=f"{y_col} with simple forecast",
        transition_duration=600,
        legend_title="Series"
    )
    return fig
