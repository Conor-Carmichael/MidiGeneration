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

page_title = ":musical_score:  Chord Progressions "

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()


# ****************************************** #
#                 Run Display
# ****************************************** #
set_sidebar()
display_song(
    chord_disp_container, st.session_state.song, st.session_state.current_progression
)

# Input where all chords shown as option
with st.container():
    show_progression_controls()


with st.container():
    if st.session_state.input_method.upper() == "FREE":
        # Handle chord input according to input method
        if st.session_state.adding_chord:
            container = st.container()
            chord_args = free_chord_input_form(container)
            if chord_args:
                set_chord_from_args(*chord_args)

    elif st.session_state.input_method.upper() == "TEXT":
        st.markdown("Text input", unsafe_allow_html=True)

    else:
        scale_factory, scale_root, scale_mode = scale_selection()

        set_state("scale_type", scale_factory.name)
        set_state("scale_mode", scale_mode)
        set_state("scale_root", scale_root)

        scale_factory = (
            scale_factory.get_mode_definition(mode_name=get_state_val("scale_mode"))
            if not get_state_val("scale_mode") is None
            else scale_factory
        )
        scale = scale_factory.generate_scale(root_note=get_state_val("scale_root"))

        if st.session_state.input_method.upper() == "GENERIC":
            display_list([n.name for n in scale.get_notes()])

            if st.session_state.adding_chord:
                generic_input_form(scale)

        elif st.session_state.input_method.upper() == "DIATONIC":
            st.markdown("Diatonic input", unsafe_allow_html=True)
