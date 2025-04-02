import numpy as np
import plotly.graph_objects as go
import streamlit as st
from cycling_dynamics import load_data

from menus import main_menu

st.set_page_config(
    page_title="HR Decoupling",
    page_icon="\u1f6b2",
    layout="wide",
    initial_sidebar_state="auto",
)
main_menu()
"""
## HR Decoupling

"""

with st.form(key="FIT file upload"):
    uploaded_file = st.file_uploader("Upload a FIT file", type=["fit", "FIT"], key="fit_file1")
    submit_button = st.form_submit_button(label="Submit")
if submit_button:
    with st.spinner("Processing..."):
        filename = f"uploaded_{uploaded_file.name}"
        with open(filename, "wb") as f:
            f.write(uploaded_file.read())
        df = load_data.load_fit_file(filename)
        df["seconds"] = df.index + 1
        if "altitude" not in df.columns:
            df["altitude"] = 0

        df["power_4th"] = df["power"] ** 4
        df["NP_15"] = df["power_4th"].rolling(window=15, min_periods=1).mean() ** 0.25
        df["NP"] = df["power_4th"].rolling(window=30, min_periods=1).mean() ** 0.25
        df["NP_60"] = df["power_4th"].rolling(window=60, min_periods=1).mean() ** 0.25

        # Fix high heartrate values
        df["prev_heartrate"] = df["heart_rate"].shift(1)
        # Replace values > 200 with their previous values
        df["heart_rate"] = np.where(df["heart_rate"] > 200, df["prev_heartrate"], df["heart_rate"])
        # Drop the temporary column if you don't need it anymore
        df = df.drop("prev_heartrate", axis=1)

        # Drop rows with NP_15 > 1
        df = df[df["heart_rate"] / df["NP_15"] < 1]

    st.dataframe(df)

    # Create a plotly figure for original ratios
    fig = go.Figure()
    fig.update_layout(height=600)

    # Add the three lines to the plot
    fig.add_trace(go.Scatter(x=df["seconds"], y=df["heart_rate"] / df["NP"], mode="lines", name="heartrate/NP"))

    # Second line (same as first line based on the request)
    fig.add_trace(
        go.Scatter(
            x=df["seconds"],
            y=df["heart_rate"] / df["NP_15"],
            mode="lines",
            name="heartrate/np_15",
            line=dict(dash="dash"),  # Making the line dashed to distinguish from the first one
        )
    )

    # Third line
    fig.add_trace(go.Scatter(x=df["seconds"], y=df["heart_rate"] / df["NP_60"], mode="lines", name="heartrate/NP_60"))

    # Update layout with title and axis labels
    fig.update_layout(
        title="Heart Rate to Normalized Power Ratios vs Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Heart Rate to NP Ratio",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Create a new column for (shifted heart_rate) / heart_rate
    df["shifted_hr_ratio"] = (
        df["heart_rate"].shift(-1).rolling(window=60).mean() / df["heart_rate"].rolling(window=60).mean()
    )

    # Create a new plotly figure for shifted heart rate ratio
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df["seconds"], y=df["shifted_hr_ratio"], mode="lines", name="(shifted HR) / HR"))
    fig3.update_layout(
        title="Shifted Heart Rate / Heart Rate vs Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Shifted Heart Rate to Heart Rate Ratio",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Display the shifted heart rate ratio plot
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

    fig2 = go.Figure()
    fig2.update_layout(height=600)

    # Add the three lines to the plot
    # fig2.add_trace(go.Scatter(x=df["seconds"], y=(df["heart_rate"] / df["NP"]) - (df["heart_rate"] / df["NP"]), mode="lines", name="heartrate/NP"))

    # Second line (same as first line based on the request)
    fig2.add_trace(
        go.Scatter(
            x=df["seconds"],
            y=df["heart_rate"] / df["NP_15"],
            mode="lines",
            name="HR NP_15 - HR NP",
            line=dict(dash="dash"),  # Making the line dashed to distinguish from the first one
        )
    )

    # Third line
    fig2.add_trace(
        go.Scatter(
            x=df["seconds"],
            y=(df["heart_rate"] / df["NP"]) - (df["heart_rate"] / df["NP_60"]),
            mode="lines",
            name="HR NP - HR NP_60",
        )
    )

    # Update layout with title and axis labels
    fig2.update_layout(
        title="Heart Rate to Normalized Power Ratios Diferances vs Time",
        xaxis_title="Time (seconds)",
        yaxis_title="Heart Rate to NP Ratio",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
