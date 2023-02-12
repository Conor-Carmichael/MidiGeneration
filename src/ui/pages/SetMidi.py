from src.theory import *
from src.ui.Progressions import display_current_chords
from src.ui.state_mgmt import *
from src.ui.display import *
import streamlit as st


set_chords_cont = st.container()
time_sig_cont = st.container()

check_and_init_state()

add_curr_to_total()


# Start display code

set_sidebar()
st.session_state.time_settings = project_settings_form(time_sig_cont)

st.session_state.midi_instr = []
for prog_idx, chord_prog in enumerate(st.session_state.all_progressions):
    prog_container = st.container()
    midi_ready_prog = []
    with prog_container:
        st.header(f"Progression {prog_idx+1}")

        for chord_idx, chord in enumerate(chord_prog):
            chord_midi_settings = chord_midi_form(chord, chord_idx, prog_idx)
            del chord_midi_settings['random_velocity']
            del chord_midi_settings['arpeggiated']
            chord_midi_settings["start_time"] = "00:00:00.00"
            # midi_chord = MidiChord.get_from_chord(**chord_midi_settings, chord=chord)
            midi_ready_prog.append({"chord": chord, "midi": chord_midi_settings})

    st.session_state.midi_instr.append(midi_ready_prog)