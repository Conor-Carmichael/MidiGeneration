"""
Main UI driver for project

Author: Conor Carmichael
"""

from src.theory import *
from src.settings import dev_mode
from src.ui.display import *
from src.ui.state_mgmt import *

# from time import time
import streamlit as st
from copy import deepcopy

check_and_init_state()

st.set_page_config(layout="wide")

page_title = ":musical_score:  Chord Progressions "

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()


# ****************************************** #
#                 Run Display
# ****************************************** #
display_state()

set_sidebar()
display_song(
    chord_disp_container, st.session_state.song, st.session_state.current_progression
)


with st.container():
    # Display buttons
    cols = st.columns(4)
    temp = cols[0].button(":heavy_plus_sign: Add Chord")
    st.session_state.adding_chord = temp if temp else st.session_state.adding_chord
    cols[1].button("Start Next Progression", on_click=start_next_progression)
    cols[2].button("Clear All Progressions", on_click=clear_all_progressions)
    cols[3].button(
        ":heavy_minus_sign: Clear Current Progression", on_click=clear_progression
    )


if st.session_state.adding_chord:
    container = st.container()
    chord_args = chord_input_form(container)
    if chord_args:
        set_chord_from_args(*chord_args)
