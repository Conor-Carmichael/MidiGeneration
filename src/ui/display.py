from src.theory import *
from src.settings import dev_mode
from src.ui.state_mgmt import *

import streamlit as st
from copy import deepcopy


# =========================================== #
#           Display drivers
# =========================================== #

notes_list = NotesFactory.get_generic_notes()


def set_sidebar(homepage: bool = True):
    st.sidebar.button("Load State", on_click=load_state, disabled=True, key=f"load_state_{homepage}")
    st.sidebar.button("Save State", on_click=save_state, disabled=True, key=f"save_state_{homepage}")

    if homepage:
        st.sidebar.header("Configure App Usage")
        st.session_state.input_method = st.sidebar.radio(
            "Input method", options=input_methods, help=input_help_str, disabled=True
        )
    else:
        st.sidebar.header("Configure MIDI File")
        st.session_state.dest = os.path.join(
            st.sidebar.text_input(
                "Destination", value=os.path.join(os.getcwd(), "midi_files")
            ),
            st.sidebar.text_input("Midi File Name", value="midi_notes") + ".mid",
        )
        st.session_state.create_bass_track = st.sidebar.checkbox("Create separate bass note track", value=False, key="bass_note_track")
        st.sidebar.button(
            ".  . ...---== Create Midi File ==---... .  .", on_click=generate_midi_files
        )


def fmt_name(name_enum: object) -> str:
    return " ".join(name_enum.name.split("_")).title()


def fmt_note_alter(note_alter: dict) -> str:
    return f"{note_alter['fn'][:-2].title()} {note_alter['degree']}"


def diatonic_input_form(container: st.container) -> None:
    """Input for only diatonic chords

    Args:
        container (st.container): Housing for form
    """
    ...


def generic_input_form(container: st.container) -> None:
    """Generic input, create chords by scale degrees

    Args:
        container (st.container): Housing for form
    """
    ...


def chord_input_form(container: st.container) -> None:
    """Input form for specific chords

    Args:
        container (st.container): Housing for form
    """
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
            "Slash Value",
            options=[None] + [n for n in notes_list.get_notes()],
            format_func=lambda n: n.name if not n is None else "None",
        )
        inversion_value = cols[4].number_input(
            "Inversion",
            min(inversion_values),
            max(inversion_values),
            value=0,
            disabled=slash_value != None,
        )
        extensions = cols[5].multiselect("Extensions", options=extension_values)
        altered_notes = cols[6].multiselect(
            "Altered Notes",
            options=note_alterations,
            format_func=fmt_note_alter,
            disabled=True,
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
    # TODO Shouldnt be messing with state variable here. move to other file.
    root = NoteGeneric(name=root)
    chord = Chord(root, ct, slash, inv, ext, alters)
    add_chord_to_prog(chord)

    return chord


def display_song(container: st.container, song: Song, curr_prog: ChordProgression):
    # Show the current song
    if not song.is_empty():
        with container:
            for sect_idx, section in enumerate(song):
                st.markdown(f"<h5>{str(section)}</h5>", unsafe_allow_html=True)

    else:
        st.markdown("No progressions", unsafe_allow_html=True)

    # Now show the current
    if not curr_prog.is_empty():
        with container:
            st.markdown(f"<h5>{str(curr_prog)}</h5>", unsafe_allow_html=True)

    else:
        st.markdown("No current progression", unsafe_allow_html=True)


def set_time_signature(container: st.container):
    with container:
        if st.session_state.input_method == "Generic":
            cols = st.columns(4)
            root_note_key = cols[0].select_slider(
                "Select Root", options=notes_list, format_func=lambda note: note.name
            )
            scale_type = cols[0].select_slider(
                "Select Root", options=notes_list, format_func=lambda note: note.name
            )
        else:
            cols = st.columns(3)

        bpm = cols[0].slider("BPM", bpm_range[0], bpm_range[1], value=120)
        beats_per_measure = cols[1].number_input(
            "Beats per measure (time sig numerator)",
            *beats_per_measure_range,
            value=4,
            disabled=True,
        )
        note_duration_per_beat = cols[2].number_input(
            "Note duration per beat (time sig denominator)",
            *note_duration_per_beat_range,
            value=4,
            disabled=True,
        )

    return bpm, beats_per_measure, note_duration_per_beat


def chord_midi_form(chord: Chord, chord_idx: int, prog_idx: int):
    key = f"{str(chord)}.{chord_idx}.{prog_idx}"
    cols = st.columns(4)
    cols[0].markdown(f"<h4>Chord<br>{str(chord)}</h4>", unsafe_allow_html=True)

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
        "Note Length (in beats)",
        note_lengths,
        value=note_lengths[2],
        key="note_duration." + key,
    )

    return {
        "arpeggiated": arp,
        "random_velocity": rand_vel,
        "velocity": velocity,
        "octave": octave,
        "note_duration": note_duration,
    }
