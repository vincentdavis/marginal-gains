import streamlit as st

from menus import main_menu

st.set_page_config(page_title="Home", page_icon="🚴", layout="wide", initial_sidebar_state="expanded")

main_menu()

st.markdown("""### Performance modeling, metrics and charts\n
#### Critical Power\n
- __Create Ramp Test:__ _Convert a power profile to a ramp test workout_\n
""")


