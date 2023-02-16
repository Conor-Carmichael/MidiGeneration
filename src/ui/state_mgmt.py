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



# Used to type check state values as they are set
# NOTE: While this requires some manual intervention, it should ensure
# that values are just _formatted_ for display, and then the internal
# value is the value it should be. Check that the type of the value is
# in this dict mapping.
type_check_state = {
    "current_progression": [ChordProgression],
    "song": [Song],
    "adding_chord": [bool],
    "time_settings": [tuple],
    "dest": [str],
    "input_method": [str],
    "create_bass_track": [bool],
    "scale_type": [ScaleFactory],
    "scale_mode": [str],
    "scale_root": [NoteGeneric, Note],
}

state_value_defaults = {
    "current_progression": ChordProgression.empty(),
    "song": Song.empty(),
    "adding_chord": False,
    "time_settings": (120, 4, 4),
    "dest": "",
    "input_method": input_methods[0],
    "create_bass_track": False,
    "scale_type": None,
    "scale_mode": None,
    "scale_root": None,
}


def check_and_init_state():
    for key, default in state_value_defaults.items():
        if not key in st.session_state:
            set_state(key, default)


# Also i dont like writing st.session_state.---- = ----
def set_state(k, v):
    """Only allows state variables in the inialization routine to be set and to the right type"""
    if k in state_value_defaults and k in type_check_state:
        if type(v) in type_check_state.get(k):
            # Cannot set back to None, must set to its initial value?
            setattr(st.session_state, k, v) 
    else:
        raise ValueError(f"Key provided {k} is not an expected value for the state. DEV: Make sure the type check dictionary is updated.")

def get_state_val(k):
    """Only allows state variables in the inialization routine to be got"""
    if k in state_value_defaults:
        getattr(st.session_state, k)
    else:
        raise ValueError(f"Key provided {k} is not an expected value for the state.")


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
            st.session_state.file_name, st.session_state.create_bass_track
        )
        success = True
    except Exception as E:
        success = False
    finally:
        return success
