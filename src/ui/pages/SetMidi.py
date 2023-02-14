from src.theory import *
from src.ui.Progressions import display_song
from src.ui.state_mgmt import *
from src.ui.display import *
import streamlit as st
from random import randint

check_and_init_state() # Checks for missing state variables and initializes

st.title("Configure MIDI Instrucions")

# If there is a current progresssion not yet added to the song
if not st.session_state.current_progression.is_empty():
    start_next_progression()


# Start display code
set_sidebar(homepage=False)

time_sig_cont = st.container()
st.session_state.time_settings = set_time_signature(time_sig_cont)

if not st.session_state.song.is_empty():
    st.session_state.song.full_loops = st.number_input("Repeat All", min_value=1, value=1)

    for prog_idx, section in enumerate(st.session_state.song):
        prog_container = st.expander(f"Progression {prog_idx+1}", expanded=True)
        midi_ready_prog = []

        with prog_container:
            section.repeats = st.number_input(
                f"Progression {prog_idx+1} repeats",
                min_value=1,
                value=1,
                key=f"progression_{prog_idx}",
            )

            for chord_idx, chord in enumerate(section):
                chord_midi_settings = chord_midi_form(chord, chord_idx, prog_idx)

                chord_midi_settings["start_time"] = "00:00:00.00"
                chord.add_midi_info(chord_midi_settings)

else:
    st.header("Nothing yet..")

generate_track_form(st.container())
