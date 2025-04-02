import streamlit as st
from cycling_dynamics import load_data

from menus import main_menu
from plots import plot_kph_100np_vs_distance, plot_kph_100watts_vs_distance

st.set_page_config(
    page_title="Efficiency",
    page_icon="\u1f6b2",
    layout="wide",
    initial_sidebar_state="auto",
)
main_menu()
"""
## Efficiency

"""

st.markdown("### Speed per 100 watts")

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

        st.dataframe(df)
        st.plotly_chart(plot_kph_100watts_vs_distance(df))
        st.plotly_chart(plot_kph_100np_vs_distance(df))
