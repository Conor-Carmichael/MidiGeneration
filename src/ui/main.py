"""
Main UI driver for project

Author: Conor Carmichael
"""

from src.theory import *

# from time import time
import streamlit as st
print("="*10, "  Reload  ", "="*10)
st.set_page_config(layout="wide")
page_title = "Chord Progression Generator"
notes_list = NotesFactory.get_generic_notes()
if not "current_progression" in st.session_state:
    st.session_state.current_progression = [] 

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()


def fmt_name(name_enum: object) -> str:
    return " ".join(name_enum.name.split("_")).title()


def fmt_note_alter(note_alter: dict) -> str:
    return f"{note_alter['fn'][:-2].title()} {note_alter['degree']}"


def project_settings_form(container:st.container):
    cols = st.columns(3)
    bpm = cols[0].slider("BPM", bpm_range[0], bpm_range[1])
    beats_per_measure = cols[1].number_input("Beats per measure (time sig numerator)", *beats_per_measure_range, value=4)
    note_duration_per_beat = cols[2].number_input("Note duration per beat (time sig denominator)", *note_duration_per_beat_range, value=4)

    return bpm, beats_per_measure, note_duration_per_beat

def add_chord():
    container_for_options = st.container()
    chord_form = st.form(key=f"chord_input_{len(st.session_state.current_progression)}",clear_on_submit=True)
    chord_input_form(container=container_for_options, form=chord_form)


def chord_input_form(container: st.container, form: st.form):
    # with container:
    st.markdown("<h3>Define a Chord</h3>", unsafe_allow_html=True)
    with st.form(key="KEY", clear_on_submit=True):
        root_note_str = st.selectbox(
            "Root Note", options=[n.name for n in notes_list.get_notes()]
        )
        chord_type = st.selectbox(
            "Chord Type", options=[ct for ct in ChordType], format_func=fmt_name
        )
        slash_value = st.selectbox(
            "Slash Value", options=[None] + [n.name for n in notes_list.get_notes()]
        )
        inversion_value = st.number_input(
            "Inversion", min(inversion_values), max(inversion_values), value=0
        )
        extensions = st.multiselect("Extensions", options=[6, 9, 11, 13])
        altered_notes = st.multiselect(
            "Altered Notes", options=note_alterations, format_func=fmt_note_alter
        )

        submitted = st.form_submit_button("Add", on_click=set_chord_from_args, args=(
                root_note_str,
                chord_type,
                slash_value,
                inversion_value,
                extensions,
                altered_notes,
            ))

def set_chord_from_args(root, ct, slash, inv, ext, alters):
    print(root, ct, slash, inv, ext, alters)
    root = NoteGeneric(name=root)
    chord = Chord(root, ct, slash, inv, ext, alters)

    st.session_state.current_progression.append(chord)

def display_chord(chord: Chord, container: st.container):
    with container:
        st.markdown(f"<h4>{str(chord)}</h4>", unsafe_allow_html=True)

def display_current_chords(container: st.container):
    with container:
        st.markdown("<h3>Chord Progression:</h3>", unsafe_allow_html=True)
        if st.session_state.current_progression == []:
                st.markdown("<h4><i>You haven't set any chords yet.</i></h4>", unsafe_allow_html=True)
        else:
            cols = st.columns(len(st.session_state.current_progression))
            for i, chord in enumerate(st.session_state.current_progression):
                display_chord(chord, cols[i])




# Display


bpm, numerator, denominator = project_settings_form(project_settings_container)

display_current_chords(chord_disp_container)
print([str(c) for c in st.session_state.current_progression])
if st.button("Add a chord"):
    chord_args = add_chord()
    if chord_args:
        set_chord_from_args(*chord_args)
