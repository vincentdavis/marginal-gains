"""Contains functions for plotting used throught the project"""

import plotly.express as px


def plot_critical_power_intensity(
    critical_power, width: int = 15, intervals: list[int, ...] = [15, 30, 60, 120, 300, 600, 900, 1200]
):
    """Plot the critical power intensity"""
    if "seconds" not in critical_power.columns:
        critical_power["seconds"] = critical_power.index + 1
    number_of_intervals = len(intervals)
    diff_cols_bar = [f"percent_cp_{interval}sec" for interval in intervals]
    diff_cols_bar.reverse()

    every_x_row = critical_power.iloc[::width].copy()
    every_x_row["percent_total_cp"] = every_x_row["percent_total_cp"] * number_of_intervals
    fig = px.bar(
        every_x_row,
        x="seconds",
        y=diff_cols_bar,
        title="Critical Power Intensity",
        labels={"value": "Percent Critical Power", "variable": "% Critical Power"},
        color_discrete_sequence=px.colors.sequential.Plasma,
    )
    fig.add_scatter(
        x=every_x_row["seconds"],
        y=every_x_row["percent_total_cp"],
        mode="lines",
        name="percent_total_cp",
        line=dict(color="red", width=2),
    )
    return fig


def plot_kph_100watts_vs_distance(df):
    """Plot speed/(power/100) vs distance with 30sec rolling average for power and speed"""
    if "speed" not in df.columns or "power" not in df.columns or "distance" not in df.columns:
        raise ValueError("The dataframe must contain 'speed', 'power', and 'distance' columns.")

    # Create 30-second rolling averages for power and speed
    power_30s_avg = df["power"].rolling(window=30, min_periods=1).mean()
    speed_30s_avg = df["speed"].rolling(window=30, min_periods=1).mean()

    # Create a new DataFrame to avoid modifying the original
    plot_df = df.copy()
    plot_df["power_30s_avg"] = power_30s_avg
    plot_df["speed_30s_avg"] = speed_30s_avg

    # Calculate the speed per watts using 30s averages
    plot_df["Speed_per_watts"] = 3.6 * plot_df["speed_30s_avg"] / (plot_df["power_30s_avg"] / 100)

    fig = px.line(
        plot_df,
        x="distance",
        y="Speed_per_watts",
        title="KPH per 100 watts vs Distance (30s avg)",
        labels={"distance": "Distance (m)", "Speed_per_watts": "KPH / 100watts (30s avg)"},
        line_shape="linear",
    )
    return fig


def plot_kph_100np_vs_distance(df):
    """Plot speed/(power/100) vs distance with 30sec rolling average for power and speed"""
    if "speed" not in df.columns or "power" not in df.columns or "distance" not in df.columns:
        raise ValueError("The dataframe must contain 'speed', 'power', and 'distance' columns.")

    # Create 30-second rolling averages for power and speed
    df["power_4th"] = df["power"] ** 4
    np = df["power_4th"].rolling(window=30, min_periods=1).mean() ** 0.25
    speed_30s_avg = df["speed"].rolling(window=30, min_periods=1).mean()

    # Create a new DataFrame to avoid modifying the original
    plot_df = df.copy()
    plot_df["np"] = np
    plot_df["Speed_per_NP"] = speed_30s_avg

    # Calculate the speed per watts using 30s averages
    plot_df["Speed_per_watts"] = 3.6 * plot_df["Speed_per_NP"] / (plot_df["np"] / 100)

    fig = px.line(
        plot_df,
        x="distance",
        y="Speed_per_NP",
        title="KPH per 100 NP watts vs Distance",
        labels={"distance": "Distance (m)", "Speed_per_watts": "KPH / 100watts (30s avg)"},
        line_shape="linear",
    )
    return fig
