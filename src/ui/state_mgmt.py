# =========================================== #
#           State management
# =========================================== #

import os
import streamlit as st
from pickle import load, dump
from src.theory import *
from loguru import logger

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
    "file_name": [str],
    "input_method": [str],
    "create_bass_track": [bool],
    "scale_factory": [ScaleFactory],
    "scale_mode": [str],
    "scale_root": [NoteGeneric, Note],
    "scale": [Scale]
}

state_value_defaults = {
    "current_progression": ChordProgression.empty(),
    "song": Song.empty(),
    "adding_chord": False,
    "time_settings": (120, 4, 4),
    "file_name": "",
    "input_method": input_methods[0],
    "create_bass_track": False,
    "scale_factory": ScaleFactory.empty(),
    "scale_mode": "",
    "scale_root": NoteGeneric.empty(),
    "scale": Scale.empty()
}


def check_and_init_state():
    for key, default in state_value_defaults.items():
        if not key in st.session_state:
            set_state_val(key, default)


# Also i dont like writing st.session_state.---- = ----
def set_state_val(k, v):
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
        return getattr(st.session_state, k)
    else:
        print(f"Key provided {k} is not an expected value for the state.")
        raise ValueError(f"Key provided {k} is not an expected value for the state.")


def display_state():
    logger.info("Current state of application.")

    for k, v in st.session_state.items():
        # print(f"{k} .. {str(v)}")
        logger.info(f"{k} : {str(v)}")


def remove_empty():
    get_state_val("song").remv_empty()


def clear_progression():
    get_state_val("current_progression").clear()


def clear_all_progressions():
    set_state_val("current_progression", ChordProgression.empty())
    set_state_val("song", Song.empty())


def add_chord_to_prog(chord: Chord):
    """Adds chord to sessions current_progression"""
    logger.debug(f"Adding {chord.__str__()} to current progression")
    get_state_val("current_progression").add_chord(chord)
    set_state_val("adding_chord", False)


def start_next_progression():
    get_state_val("song").add_section(get_state_val("current_progression"))
    set_state_val("current_progression", ChordProgression.empty())


def add_curr_to_total():
    get_state_val("song").add_section(get_state_val("current_progression"))
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
    # try:
    if os.path.exists(get_state_val("file_name")):
        os.remove(get_state_val("file_name"))

    get_state_val("song").write_song_to_midi(
        get_state_val("file_name"),
        get_state_val("create_bass_track"),
        is_generic=get_state_val("input_method").upper()=="GENERIC",
        # scale=get_state_val("scale_factory")
    )
    # success = True
    # except Exception as E:
    #     success = False
    # finally:
    return success
