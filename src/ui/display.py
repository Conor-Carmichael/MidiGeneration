
from src.theory import *
from src.settings import dev_mode
from src.ui.state_mgmt import *


# from time import time
import streamlit as st
from copy import deepcopy


# =========================================== #
#           Display drivers
# =========================================== #

notes_list = NotesFactory.get_generic_notes()

def set_sidebar():
    st.session_state.input_method = st.sidebar.radio("Input method", options=input_methods, help=input_help_str, disabled=True)
    st.sidebar.button("Load State", on_click=load_state, disabled=True)
    st.sidebar.button("Save State", on_click=save_state, disabled=True)

    st.session_state.dest = os.path.join(
        st.sidebar.text_input("Destination", value=os.path.join(os.getcwd(), "midi_files")),
        st.sidebar.text_input("Midi File Name", value="midi_notes.mid")
    ) 

    st.sidebar.button(
        ".  . ...---== Create Midi File ==---... .  .", 
        on_click=generate_midi_files
    )


def fmt_name(name_enum: object) -> str:
    return " ".join(name_enum.name.split("_")).title()


def fmt_note_alter(note_alter: dict) -> str:
    return f"{note_alter['fn'][:-2].title()} {note_alter['degree']}"


def add_chord():
    container_for_options = st.container()
    chord_input_form(container=container_for_options)


def chord_input_form(container: st.container):
    # with container:
    with container:
        st.markdown("<h3>Define a Chord</h3>", unsafe_allow_html=True)
        cols = st.columns(7)
        root_note_str = cols[1].selectbox(
            "Root Note", options=[n.name for n in notes_list.get_notes()]
        )
        chord_type = cols[2].selectbox(
            "Chord Type", options=[ct for ct in ChordType], format_func=fmt_name
        )
        slash_value = cols[3].selectbox(
            "Slash Value", options=[None] + [n for n in notes_list.get_notes()], format_func=lambda n: n.name if not n is None else "None"
        )
        inversion_value = cols[4].number_input(
            "Inversion", min(inversion_values), max(inversion_values), value=0, disabled=slash_value!=None
        )
        extensions = cols[5].multiselect("Extensions", options=extension_values)
        altered_notes = cols[6].multiselect(
            "Altered Notes", options=note_alterations, format_func=fmt_note_alter, disabled=True
        )

        cols[0].button(
            "Add",
            on_click=set_chord_from_args,
            args=(
                root_note_str,
                chord_type,
                slash_value,
                inversion_value,
                extensions,
                altered_notes,
            ),
        )


def set_chord_from_args(root, ct, slash, inv, ext, alters):
    root = NoteGeneric(name=root)
    chord = Chord(root, ct, slash, inv, ext, alters)
    st.session_state.current_progression.append(chord)
    st.session_state.adding_chord = False


def display_chord(chord: Chord, container: st.container, is_current:bool=False):
    with container:
        if chord is None:
            st.markdown("<p>Empty</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h5>{str(chord)}</h5>", unsafe_allow_html=True)


def display_current_chords(container: st.container, chords: list):
    # All progressions is list of progression lists
    all_progressions_disp = deepcopy(st.session_state.all_progressions)

    if st.session_state.current_progression != []:
        all_progressions_disp.append(st.session_state.current_progression)

    with container:

        if st.session_state.all_progressions == [] and st.session_state.current_progression == []:
            st.markdown(
                "<h4><i>You haven't set any chords yet.</i></h4>",
                unsafe_allow_html=True,
            )
        else:

            for chord_prog in st.session_state.all_progressions:
                if len(chord_prog) > 0: 
                    cols = st.columns(len(chord_prog))
                    for i, chord in enumerate(chord_prog):
                        display_chord(chord, cols[i])
            
            if len(st.session_state.current_progression) > 0: 
                cols = st.columns(len(st.session_state.current_progression)+1)
                cols[0].markdown("<i>Current Progression</i>", unsafe_allow_html=True)

                for i, chord in enumerate(st.session_state.current_progression):
                    display_chord(st.session_state.current_progression[i], cols[i+1], is_current=True)




def project_settings_form(container: st.container):
    with container:
        cols = st.columns(3)
        bpm = cols[0].slider("BPM", bpm_range[0], bpm_range[1])
        beats_per_measure = cols[1].number_input(
            "Beats per measure (time sig numerator)", *beats_per_measure_range, value=4, disabled=True
        )
        note_duration_per_beat = cols[2].number_input(
            "Note duration per beat (time sig denominator)",
            *note_duration_per_beat_range,
            value=4,
            disabled=True
        )

    return bpm, beats_per_measure, note_duration_per_beat



def chord_midi_form(chord: Chord, chord_idx: int, prog_idx: int):
    key = f"{str(chord)}.{chord_idx}.{prog_idx}"
    cols = st.columns(4)
    cols[0].markdown(f"<h4>Chord: {str(chord)}</h4>", unsafe_allow_html=True)

    arp = cols[1].checkbox("Arpeggiate", value=False, key="arp." + key, disabled=True)
    rand_vel = cols[1].checkbox("Random Velocity", value=False, key="rand_vel." + key)
    velocity = cols[2].slider(
        "Velocity",
        min_value=midi_vel_low,
        max_value=midi_vel_high,
        disabled=rand_vel,
        value=100,
        key="velocity." + key,
    )
    octave = cols[2].slider(
        "Octave", min_value=2, max_value=6, value=4, key="octave." + key
    )
    note_duration = cols[3].select_slider(
        "Note Length (in beats)", note_lengths, value=note_lengths[2], key="note_duration." + key
    )

    return {
        "arpeggiated": arp,
        "random_velocity": rand_vel,
        "velocity": velocity,
        "octave": octave,
        "note_duration": note_duration,
    }

