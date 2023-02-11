"""
Main UI driver for project

Author: Conor Carmichael
"""

from src.theory import *

# from time import time
import streamlit as st
from copy import deepcopy


st.set_page_config(layout="wide")

page_title = "Chord Progression Generator"
notes_list = NotesFactory.get_generic_notes()

if not "current_progression" in st.session_state:
    st.session_state.current_progression = [] 
if not "all_progressions" in st.session_state:
    st.session_state.all_progressions = [] 
if not "adding_chord" in st.session_state:
    st.session_state.adding_chord = False


print("\n\n\n", "*"*15, " Reload ", "*"*15, "\n\n")

st.title(page_title)
project_settings_container = st.container()
chord_disp_container = st.container()


def disp_state():
    print(f"State Vars")
    for key in ["current_progression", "all_progressions"]:
        print(f"{key} : {st.session_state.get(key)}")

def clear_progression():
    st.session_state.current_progression = []

def clear_all_progressions():
    st.session_state.all_progressions = []

def next_chord_progression():
    st.session_state.all_progressions.append(st.session_state.current_progression)
    st.session_state.current_progression = []

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
    with container:
        st.markdown("<h3>Define a Chord</h3>", unsafe_allow_html=True)
        cols = st.columns(7)
        root_note_str = cols[0].selectbox(
            "Root Note", options=[n.name for n in notes_list.get_notes()]
        )
        chord_type = cols[1].selectbox(
            "Chord Type", options=[ct for ct in ChordType], format_func=fmt_name
        )
        slash_value = cols[2].selectbox(
            "Slash Value", options=[None] + [n.name for n in notes_list.get_notes()]
        )
        inversion_value = cols[3].number_input(
            "Inversion", min(inversion_values), max(inversion_values), value=0
        )
        extensions = cols[4].multiselect("Extensions", options=extension_values)
        altered_notes = cols[5].multiselect(
            "Altered Notes", options=note_alterations, format_func=fmt_note_alter
        )

        cols[6].button("Add", on_click=set_chord_from_args, args=(
                root_note_str,
                chord_type,
                slash_value,
                inversion_value,
                extensions,
                altered_notes,
            ))

def set_chord_from_args(root, ct, slash, inv, ext, alters):
    root = NoteGeneric(name=root)
    chord = Chord(root, ct, slash, inv, ext, alters)
    st.session_state.current_progression.append(chord)
    st.session_state.adding_chord = False

def display_chord(chord: Chord, container: st.container):
    with container:
        st.markdown(f"<h4>{str(chord)}</h4>", unsafe_allow_html=True)

def display_current_chords(container: st.container, chords:list):
    # All progressions is list of progression lists
    all_progressions_disp = deepcopy(st.session_state.all_progressions)
    if st.session_state.current_progression != []:
        all_progressions_disp.append(st.session_state.current_progression)
    with container:
        if all_progressions_disp == []:
                st.markdown("<h4><i>You haven't set any chords yet.</i></h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h3>Chord Progressions</h3>", unsafe_allow_html=True)
            for chord_prog in all_progressions_disp:    
                cols = st.columns(len(chord_prog))
                for i, chord in enumerate(chord_prog):
                    display_chord(chord, cols[i])

# ****************************************** #
#                 Display
# ****************************************** #
disp_state()
bpm, numerator, denominator = project_settings_form(project_settings_container)

display_current_chords(chord_disp_container, st.session_state.all_progressions)

st.button("Start Next Progression", on_click=next_chord_progression)

# Allows it to be set false elsewhere in code
temp = st.button("Add a chord")
st.session_state.adding_chord = temp if temp else st.session_state.adding_chord

if st.session_state.adding_chord:
    chord_args = add_chord()
    if chord_args:
        set_chord_from_args(*chord_args)

