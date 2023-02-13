# =========================================== #
#           State management
# =========================================== #

import os
import streamlit as st
from pickle import load, dump
from src.theory import *

# Input styles:
# * Free: Select from any chords
# * Generic: by numeral
# * Diatonic: only show diatonic chords
input_help_str = "Choose how to enter chords. Freely select any chords, choose by numerals, or choose from diatonic chords."
input_methods = ["Free", "Generic", "Diatonic"]
save_dir = os.path.join(os.getcwd(), "midi_values")


def check_and_init_state():

    if not "current_progression" in st.session_state:
        st.session_state.current_progression = []
    if not "all_progressions" in st.session_state:
        st.session_state.all_progressions = []
    if not "adding_chord" in st.session_state:
        st.session_state.adding_chord = False
    if not "setting_chord_midi" in st.session_state:
        st.session_state.setting_chord_midi = False
    if not "time_settings" in st.session_state:
        st.session_state.time_settings = (60, 4, 4)
    if not "midi_instr" in st.session_state:
        st.session_state.midi_instr = []
    if not "dest" in st.session_state:
        st.session_state.dest = ""

state_file = os.path.join(".", "src", "ui", "store", "state.pkl")


def dev_set_state(state: dict):
    ...


def disp_state():
    print("\n\n\n", "*" * 15, " Reload ", "*" * 15, "\n\n")
    print(f"State Vars")
    for k, v in st.session_state.items():
        print(f"{k} : {v}")


def remove_empty():
    st.session_state.all_progressions = list(
        filter(lambda prog: prog != [], st.session_state.all_progressions)
    )


def clear_progression():
    st.session_state.current_progression = []


def clear_all_progressions():
    clear_progression()
    st.session_state.all_progressions = []


def next_chord_progression():
    if st.session_state.current_progression == []:
        return
    add_curr_to_total()


def add_curr_to_total():
    st.session_state.all_progressions.append(st.session_state.current_progression)
    clear_progression()
    remove_empty()


def save_state():
    try:
        with open(state_file, 'wb') as f:
            ss = dict(st.session_state)
            print(ss)
            dump(ss, f)
        st.success("State saved.")

    except Exception as e:
        st.warning("Failed to save state...")
        print(e)


def load_state():
    try:
        with open(state_file, 'rb') as f:
            data = load(f)
            print("Data: ", data)
            for k, v in data.items():
                print(k, v)
                setattr(st.session_state, k, v)

        st.success("State loaded.")

    except Exception as e:
        print("Exception: ", e)
        st.warning("Failed to load state...")


def generate_midi_files():

    midi_obj = get_midi_object_from_progression(
        bpm=st.session_state.time_settings[0],
        track=0,
        chord_progressions=st.session_state.midi_instr
    )

    if os.path.exists(st.session_state.dest):
        os.remove(st.session_state.dest)

    try:
        with open(st.session_state.dest, "wb") as f:
            midi_obj.writeFile(f)

        st.success(f"{st.session_state.dest} Created")
    
    except Exception as e:
        st.error("Error creating the midi file.")