"""
Main UI driver for project

Author: Conor Carmichael
"""
import sys, os

sys.path.append(os.getcwd())


from src.theory import *
from src.settings import dev_mode
from src.ui.display import *
from src.ui.state_mgmt import *

# from time import time
import streamlit as st
from copy import deepcopy

check_and_init_state()

st.set_page_config(layout="wide")

page_title = ":musical_score: Create Your Chord Progressions "

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()


# ****************************************** #
#                 Run Display
# ****************************************** #
set_sidebar()
display_song(
    get_state_val("song"), get_state_val("current_progression")
)

# Input where all chords shown as option
with st.container():
    show_progression_controls()


with st.container():
    if get_state_val("input_method").upper() == "FREE":
        # Handle chord input according to input method
        if get_state_val("adding_chord"):
            chord_args = free_chord_input_form()
            if chord_args:
                set_chord_from_args(*chord_args)

    elif get_state_val("input_method").upper() == "TEXT":
        st.markdown("Text input", unsafe_allow_html=True)

    else:
        scale_prog_bar = st.progress(0)
        scale_factory, scale_root, scale_mode = scale_selection()

        set_state_val("scale_type", scale_factory)
        set_state_val("scale_mode", scale_mode)
        set_state_val("scale_root", scale_root)

        # Get the appopriate scale type give the base scale and mode choices
        set_state_val("scale_type",
            get_state_val("scale_type").get_mode_definition(mode_name=get_state_val("scale_mode"))
            if not get_state_val("scale_mode") is None
            else scale_factory
        )


        scale = get_state_val("scale_type").generate_scale(root_note=get_state_val("scale_root"))

        scale_prog_bar.progress(100)
        scale_prog_bar.empty()

        if get_state_val("input_method").upper() == "GENERIC":

            if get_state_val("adding_chord"):
                generic_input_form(scale)

        elif get_state_val("input_method").upper() == "DIATONIC":
            st.markdown("Diatonic input is a work in progress", unsafe_allow_html=True)
