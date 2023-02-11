from src.theory import *
from src.ui.Progressions import display_current_chords

import streamlit as st

if not st.session_state.midi_instr:
    st.session_state.midi_instr = []

set_chords_cont = st.container()
time_sig_cont = st.container()

def project_settings_form(container:st.container):
    cols = st.columns(3)
    bpm = cols[0].slider("BPM", bpm_range[0], bpm_range[1])
    beats_per_measure = cols[1].number_input("Beats per measure (time sig numerator)", *beats_per_measure_range, value=4)
    note_duration_per_beat = cols[2].number_input("Note duration per beat (time sig denominator)", *note_duration_per_beat_range, value=4)

    return bpm, beats_per_measure, note_duration_per_beat


def set_chord_info(chords:List):
    for chord_prog in st.session_state.all_progressions:
        for chord in chord_prog:
            # Get start / dur / vel / arpeg
            ...

# Start display code



display_current_chords(set_chords_cont, st.session_state.all_progressions)

bpm, num, denom = project_settings_form(time_sig_cont)