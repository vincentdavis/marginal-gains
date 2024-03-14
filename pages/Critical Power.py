import plotly.express as px
import streamlit as st
from cycling_dynamics import load_data
from cycling_dynamics.critical_power import critical_power, get_critical_power_intensity
from cycling_dynamics.plots import plot_activity_critical_power, plot_critical_power_intensity

from menus import main_menu

st.set_page_config(
    page_title="Critical Power",
    page_icon="\u1f6b2",
    layout="wide",
    initial_sidebar_state="auto",
)
main_menu()
"""### Critical Power (CP) curve and CP intensity
- Critical power intensity for an activity is the the % of CP at each point in the activity and the total (average) for 
the entire activity
You can download an csv file of the calculated Critical Power curve (CP) as a csv file.

### Plots:
1. This is a plot of the CP curve with the standard deviation of the power observed withing the time period the CP value
 was seen.
2. CP intensity
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

        st.download_button(
            label="Download FIT file as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="fit_to_csv.csv",
            mime="text/csv",
        )

        st.markdown("### Critical Power Curve with Standard Deviation")
        cp = critical_power(df)["df"]
        st.download_button(
            label="Download csv of CP data",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="Critical_Power.csv",
            mime="text/csv",
        )
        fig1 = plot_activity_critical_power(cp)
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

        total_cp, cp_df = get_critical_power_intensity(df, cp=None)
        st.markdown(f"### Critical Power Activity Intensity: {total_cp*100:.1f}%")
        cp_df["seconds"] = cp_df.index + 1
        df_with_cp = df.merge(cp_df, on="seconds")
        st.download_button(
            label="Download csv of FIT with CP_intensity",
            data=df_with_cp.to_csv(index=False).encode("utf-8"),
            file_name="CP_Intensity.csv",
            mime="text/csv",
        )
        fig2 = plot_critical_power_intensity(cp_df)
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

        cp["end-start"] = cp["cp"] + cp["slope"]
        fig3 = px.line(cp, x="seconds", y=["cp", "end-start"], title="Critical Power with end-start power split")
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
