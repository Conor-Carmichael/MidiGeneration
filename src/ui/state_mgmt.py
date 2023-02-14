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
input_methods = ["Free", "Generic", "Diatonic", "Text"]
save_dir = os.path.join(os.getcwd(), "midi_values")


def check_and_init_state():
    if not "current_progression" in st.session_state:
        st.session_state.current_progression = ChordProgression.empty()
    if not "song" in st.session_state:
        st.session_state.song = Song.empty()
    if not "adding_chord" in st.session_state:
        st.session_state.adding_chord = False
    if not "setting_chord_midi" in st.session_state:
        st.session_state.setting_chord_midi = False
    if not "time_settings" in st.session_state:
        st.session_state.time_settings = (120, 4, 4)
    if not "midi_instr" in st.session_state:
        st.session_state.midi_instr = []
    if not "dest" in st.session_state:
        st.session_state.dest = ""
    if not "input_method" in st.session_state:
        st.session_state.input_method = input_methods[0]
    if not "create_bass_track" in st.session_state:
        st.session_state.create_bass_track = False


state_file = os.path.join(".", "src", "ui", "store", "state.pkl")


def dev_set_state(state: dict):
    ...


def display_state():
    logging.info("Current state of application.")

    for k, v in st.session_state.items():
        # print(f"{k} .. {str(v)}")
        logging.info(f"{k} : {str(v)}")


def remove_empty():
    st.session_state.song.remv_empty()


def clear_progression():
    st.session_state.current_progression.clear()


def clear_all_progressions():
    st.session_state.current_progression = ChordProgression.empty()
    st.session_state.song = Song.empty()


def add_chord_to_prog(chord: Chord):
    """Adds chord to sessions current_progression"""
    st.session_state.current_progression.add_chord(chord)
    st.session_state.adding_chord = False


def start_next_progression():
    st.session_state.song.add_section(st.session_state.current_progression)
    st.session_state.current_progression = ChordProgression.empty()


def add_curr_to_total():
    st.session_state.song.add_section(st.session_state.current_progression)
    clear_progression()
    remove_empty()


def save_state():
    raise NotImplementedError()
    try:
        with open(state_file, "wb") as f:
            ss = dict(st.session_state)
            print(ss)
            dump(ss, f)
        st.success("State saved.")

    except Exception as e:
        st.warning("Failed to save state...")
        print(e)


def load_state():
    raise NotImplementedError()
    try:
        with open(state_file, "rb") as f:
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
    success = False
    try:
        if os.path.exists(st.session_state.dest):
            os.remove(st.session_state.dest)

        st.session_state.song.write_song_to_midi(
            st.session_state.file_name,
            st.session_state.create_bass_track
        )
        success = True
    except Exception as E:
        success = False
    finally:

        return success
