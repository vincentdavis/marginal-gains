"""Contains functions for plotting used throught the project"""

import plotly.express as px


def plot_critical_power_intensity(critical_power, width: int = 15,
                                  intervals: list[int, ...] = [15, 30, 60, 120, 300, 600, 900, 1200]):
    """Plot the critical power intensity"""
    if 'seconds' not in critical_power.columns:
        critical_power['seconds'] = critical_power.index + 1
    number_of_intervals = len(intervals)
    diff_cols_bar = [f"percent_cp_{interval}sec" for interval in intervals]
    diff_cols_bar.reverse()

    every_x_row = critical_power.iloc[::width].copy()
    every_x_row['percent_total_cp'] = every_x_row['percent_total_cp'] * number_of_intervals
    fig = px.bar(every_x_row, x="seconds", y=diff_cols_bar, title="Critical Power Intensity",
                 labels={'value': 'Percent Critical Power', 'variable': '% Critical Power'},
                 color_discrete_sequence=px.colors.sequential.Plasma)
    fig.add_scatter(x=every_x_row['seconds'], y=every_x_row['percent_total_cp'], mode='lines', name='percent_total_cp',
                    line=dict(color='red', width=2))
    return fig