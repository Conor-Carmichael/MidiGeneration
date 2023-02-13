from src.theory import *
from src.ui.Progressions import display_current_chords
from src.ui.state_mgmt import *
from src.ui.display import *
import streamlit as st
from random import randint


set_chords_cont = st.container()
time_sig_cont = st.container()

check_and_init_state()

add_curr_to_total()


# Start display code

set_sidebar()
st.session_state.time_settings = project_settings_form(time_sig_cont)

st.session_state.midi_instr = []
loops = st.number_input("Repeat All", min_value=1, value=1)
for prog_idx, chord_prog in enumerate(st.session_state.all_progressions):
    prog_container = st.expander(f"Progression {prog_idx+1}", expanded=True)
    midi_ready_prog = []
    with prog_container:

        repeat_prog_n = st.number_input(f"Progression {prog_idx+1} repeats", min_value=1, value=1, key=f"progression_{prog_idx}")

        for chord_idx, chord in enumerate(chord_prog):
            chord_midi_settings = chord_midi_form(chord, chord_idx, prog_idx)
            
            chord_midi_settings["start_time"] = "00:00:00.00"
            chord.add_midi_info(chord_midi_settings)

        
            midi_ready_prog.append({"chord": chord, "midi": chord_midi_settings})

    st.session_state.midi_instr.append(midi_ready_prog*repeat_prog_n)
st.session_state.midi_instr = st.session_state.midi_instr * loops