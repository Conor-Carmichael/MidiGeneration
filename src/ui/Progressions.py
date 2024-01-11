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
from src.theory.diatonic import find_diatonic_chords

# from time import time
import streamlit as st
from streamlit_option_menu import option_menu
from copy import deepcopy

check_and_init_state()

st.set_page_config(layout="wide")

page_title = ":musical_score: Create Your Chord Progressions "

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()

hz_line = lambda : st.markdown("***", unsafe_allow_html=True)

# ****************************************** #
#                 Run Display
# ****************************************** #
# set_sidebar()

# Current progression is in editing, and isnt locked in yet.
# Display the song (all previously added progressions), then prog in progress
display_song(
    get_state_val("song"), 
    get_state_val("current_progression")
)
# Start next, clear current, clear all progressions
show_progression_controls()


# ************************ #
#        Scale Inputs      #
# ************************ #

hz_line()
scale_input_box = st.container(border=False)
# Scale Factory: Generates a scale obj/sequence on demand.
# If a mode is selected, can use that to alter the scale factory
scale_input_box.markdown("<h4>Set the home key for the song</h4>", unsafe_allow_html=True)
scale_factory, root_note_str, mode_choice = scale_selection(scale_input_box)
if mode_choice:
    scale_factory = scale_factory.get_mode_definition(mode_name=mode_choice)
scale = scale_factory.generate_scale(root_note=root_note_str)
hz_line()


# ************************ #
#        Chord Inputs      #
# ************************ #

selected = option_menu(
    "Chord Input Style", 
    ["Text Input", "Diatonic Input",  "Free Form Input"], 
    icons=['keyboard', 'music-note-list',  'card-list'], 
    menu_icon="gear", 
    default_index=0, 
    orientation="horizontal",
    key="input-opt-menu"
)

if selected == "Text Input":

    st.markdown(
        "<sub>Use capital letter to denote notes. \n'b' for flat, '#' for sharp, or ascii characters ♯ and ♭.",
        unsafe_allow_html=True
    )

    chord_input_str = st.text_input(
        label="Input chord by text", 
        max_chars=16, 
        placeholder="A#maj7/A", 
    )

    new_chord = Chord.from_str(
        input_str=chord_input_str
    )

elif selected == "Diatonic Input":
    with st.expander(expanded=True, label="Chord Input"):

        diatonic_info = find_diatonic_chords(scale)

        new_chord = diatonic_chord_input_form(
            diatonic_opts=diatonic_info,
            root_fmt_fn=lambda note: note.name if not note is None else note,
            chord_type_fmt_fn=lambda chord_type: " ".join(chord_type.name.split("_")).title(),
            inversion_range=inversion_values,
        )

elif selected == "Free Form Input":
    with st.expander(expanded=True, label="Chord Input"):
        new_chord = chord_input_form(
            root_options=notes_list,
            root_fmt_fn=lambda note: note.name if not note is None else note,
            chord_type_options=[chord for chord in ChordType],
            chord_type_fmt_fn=lambda chord_type: " ".join(chord_type.name.split("_")).title(),
            inversion_range=inversion_values,
        )


if st.button(
    f"Add {new_chord.__str__()}" if new_chord else "Set Next Chord",
    use_container_width=True,
    disabled=(new_chord is None),
):
    
    submit_chord_to_prog(new_chord)




