"""
UI for choosing the songs midi configuration

Author: Conor Carmichael
"""
import sys, os

sys.path.append(os.getcwd())


from src.theory import *
from src.ui.Progressions import display_song
from src.ui.state_mgmt import *
from src.ui.display import *
import streamlit as st
from random import randint

check_and_init_state()  # Checks for missing state variables and initializes

# If there is a current progresssion not yet added to the song
if not get_state_val("current_progression").is_empty():
    start_next_progression()

# TODO: If input is generic, text: need to calculate the degree chords
if get_state_val("input_method").upper() == "GENERIC":

    # This is wasteful, need to find way to skip this process after its been run once.
    new_song = Song.empty()
    for section in get_state_val("song"):
        new_section = ChordProgression.empty()

        for chord in section:
            # Convert the generic chord to a full chord:
            new_chord = chord.define_chord(get_state_val("scale")) if isinstance(chord, ChordGeneric) else chord
            new_section.add_chord(new_chord)
        
        new_song.add_section(new_section)

    set_state_val("song", new_song)

    

st.title(" Configure MIDI Instrucions")


# Start display code
set_sidebar(homepage=False)

st.header(":notes: Your Chords")
display_song(
    get_state_val("song"), get_state_val("current_progression")
)

st.header(":musical_score: Set the Time Signature")
set_time_signature()


st.header(":control_knobs: Configure Playback by Chord")
if not get_state_val("song").is_empty():
    get_state_val("song").full_loops = st.number_input(
        "Repeat All", min_value=1, value=1
    )

    for prog_idx, section in enumerate(get_state_val("song")):
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
                if type(chord) == ChordGeneric:
                    chord = chord.define_chord(get_state_val("scale"))
                chord.add_midi_info(chord_midi_settings)
    
    st.header(":file_folder: Download Your MIDI File")
    generate_track_form(st.container())

else:
    st.markdown("<p>Nothing yet...</p>", unsafe_allow_html=True)



