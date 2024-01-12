from src.theory import *
from src.settings import dev_mode
from src.ui.state_mgmt import *

import streamlit as st
from copy import deepcopy


# =========================================== #
#           Display drivers: input forms,
#               and data dipslays
# =========================================== #

notes_list = NotesFactory.get_generic_notes()

# **************************************** #
# General display functions                #
# **************************************** #


def passthrough(input):
    """ 'Dummy' fn to help with a process :) """
    return input


def set_fmt_fn(possible_fmt_fn):
    """Allows me to pass None to format function for input form generators easier"""
    if possible_fmt_fn is None:
        return passthrough

    else:
        return possible_fmt_fn


def set_sidebar(homepage: bool = True):
    """Sets the sidebar for the given page.

    Args:
        homepage (bool, optional): If we are setting the sidebar for the homepage. Defaults to True.
    """
    st.sidebar.button(
        "Load State", on_click=load_state, disabled=True, key=f"load_state_{homepage}"
    )
    st.sidebar.button(
        "Save State", on_click=save_state, disabled=True, key=f"save_state_{homepage}"
    )

    if homepage:
        st.sidebar.header("Configure App Usage")
        selected = st.sidebar.radio(
            "Input method", options=input_methods
        )
        both_empty = get_state_val("song").is_empty() and get_state_val("current_progression").is_empty()

        if selected != get_state_val("input_method") and not both_empty:
            st.warning("Clearing progressions due to input method change.", )
            clear_all_progressions()

        set_state_val("input_method", selected)


def display_song(song: Song, curr_prog: ChordProgression):
    """Show the current song: Iteratively display chord progs"""
    both_empty = song.is_empty() and curr_prog.is_empty()

    if both_empty:
        st.markdown("No chords...", unsafe_allow_html=True)

    else:
        viz = Visualizer(settings={})
        # Show all the song
        if not song.is_empty():
            st.markdown(f"<h4>Song in {song.home_key.__str__()}</h4>", unsafe_allow_html=True)
            song_graph = viz._build_from_song(song=song)
            st.graphviz_chart(song_graph)
            # for sect_idx, section in enumerate(song):
            #     st.markdown(f"<h5>{str(section)}</h5>", unsafe_allow_html=True)
        # Now show the current
        st.markdown("<h4>Progression in progress...</h4>", unsafe_allow_html=True)
        if not curr_prog.is_empty():
            curr_prog_graph = viz._build_from_seq(name="Current Progression", sequence=curr_prog)
            st.graphviz_chart(curr_prog_graph)
        else:
            st.markdown("Add in some chords")




def show_progression_controls():
    # Display buttons
    cols = st.columns(4)
    # if not get_state_val("adding_chord"):
    #     temp = cols[0].button(":heavy_plus_sign: Add Chord")
    #     set_state_val("adding_chord", temp if temp else get_state_val("adding_chord"))

    progression_designation = cols[0].selectbox("Progression designation", index=0, options=["Verse", "Pre-chorus", "Chorus", "Bridge", "Outro"] )
    # these are to force alignment with the button, annoying ik
    cols[1].markdown("")
    cols[1].markdown("")
    cols[1].button("Start Next Progression", on_click=start_next_progression, args=({"progression_designation":progression_designation}), use_container_width=True)

    cols[2].markdown("")
    cols[2].markdown("")
    cols[2].button("Clear All Progressions", on_click=clear_all_progressions, use_container_width=True)
    cols[3].markdown("")
    cols[3].markdown("")
    cols[3].button(
        "Clear Current Progression", on_click=clear_progression, use_container_width=True
    )


def display_list(data: List[str]) -> None:
    """Display a list of strings as a html list

    Args:
        data (List[str]): _description_

    Returns:
        _type_: _description_
    """
    display_str = "<ul>"
    for ele in data:
        display_str += f"<li>{ele}</li>"
    display_str += "</ul>"
    st.markdown(display_str, unsafe_allow_html=True)
    return display_str


def scale_selection(container:st.container=None) -> Tuple[ScaleFactory, Note, str]:
    """Function to generate an input form for scale selection.

    Returns:
        Tuple[ScaleFactory, Note, str]: _description_
    """
    with container:
        cols = st.columns([1, 2, 2])

        root_note_str = cols[0].selectbox(
            "Root Note",
            options=notes_list.get_notes(),
            format_func=lambda note: note.name,
        )

        scale_fact = cols[1].selectbox(
            "Scale Type",
            options=AllScaleFactories,
            format_func=lambda sf: sf.name.name.title()
            if isinstance(sf.name, Enum)
            else sf.name,
        )


        if scale_fact.has_modes():
            mode = cols[2].selectbox(
                scale_fact.name + " Mode",
                scale_fact.modes,
                format_func=lambda mode: mode.name.title()
                if isinstance(mode, Enum)
                else mode,
            )
        else:
            mode = None

    return scale_fact, root_note_str, mode




# ****************************************************** #
# Chord Progresssion selection display functions         #
# ****************************************************** #

def diatonic_chord_input_form(
    diatonic_opts:dict,
    root_fmt_fn: Callable,
    chord_type_fmt_fn: Callable,
    inversion_range: tuple
) -> Chord:
    st.markdown(f"<h3>Input via options</h3>", unsafe_allow_html=True)
    root_options = list(diatonic_opts.keys())
    cols = st.columns([1, 1, 1, 1])

    root_selected = cols[0].radio(
        "Root Note", options=root_options
        #, format_func=set_fmt_fn(root_fmt_fn) # The keys are just the string, name
    )

    chord_type = cols[1].radio(
        "Chord Type",
        options=diatonic_opts[root_selected],
        format_func=set_fmt_fn(chord_type_fmt_fn),
        disabled=root_selected is None
    )  


    slash_value = cols[2].selectbox(
        "Slash Value",
        options=[None] + root_options,
        # format_func=set_fmt_fn(root_fmt_fn),
    )

    inversion_value = cols[2].number_input(
        "Inversion",
        min(inversion_range),
        max(inversion_range),
        value=min(inversion_range),
        disabled=slash_value != None,
    )

    extensions = cols[3].multiselect(
        "Upper Chord Extensions", options=extension_values
    )
    altered_notes = cols[3].multiselect(
        "Altered Notes",
        options=note_alterations,
        # format_func=,
        disabled=True,
        help="Coming soon: Choose chord interval and flatten/sharpen",
    )
    logger.debug(root_selected)
    logger.debug(NoteGeneric(name=root_selected, ))


    # if st.button("Random chord"):
    #     ran


    chord = Chord(
        NoteGeneric(name=root_selected), chord_type, NoteGeneric(slash_value) if slash_value else None, inversion_value, extensions, altered_notes
    )

    return chord


def chord_input_form(
    root_options: List,
    root_fmt_fn: Callable,
    chord_type_options: List,
    chord_type_fmt_fn: Callable,
    inversion_range: tuple,
) -> Chord:

    st.markdown(f"<h3>Input via options</h3>", unsafe_allow_html=True)

    cols = st.columns([1, 1, 3])
    print(root_options)
    st.selectbox("Root Note", options=root_options[:3],     format_func=set_fmt_fn(root_fmt_fn))
    root_selected = cols[0].radio(
        "Root Note", options=["A","V"]#, format_func=set_fmt_fn(root_fmt_fn)
    )
    # chord_type = cols[1].radio(
    #     "Chord Type",
    #     options=chord_type_options,
    #     format_func=set_fmt_fn(chord_type_fmt_fn),
    # )       

    # slash_value = cols[2].selectbox(
    #     "Slash Value",
    #     options=[None] + root_options,
    #     format_func=set_fmt_fn(root_fmt_fn),
    # )

    # inversion_value = cols[2].number_input(
    #     "Inversion",
    #     min(inversion_range),
    #     max(inversion_range),
    #     value=min(inversion_range),
    #     disabled=slash_value != None,
    # )

    # extensions = cols[2].multiselect(
    #     "Upper Chord Extensions", options=extension_values
    # )
    # altered_notes = cols[2].multiselect(
    #     "Altered Notes",
    #     options=note_alterations,
    #     # format_func=,
    #     disabled=True,
    #     help="Coming soon: Choose chord interval and flatten/sharpen",
    # )
    # chord = Chord(
    #     root_selected, chord_type, slash_value, inversion_value, extensions, altered_notes
    # )

    # return chord


# Moving chords from input form to the progression
def submit_chord_to_prog(
    chord:Chord
) -> None:
    """Takes the chord args and builds a chord, adds it to the song.

    Args:
        root_note (_type_): _description_
        chord_type (_type_): _description_
        slash_value (_type_): _description_
        inversion_value (_type_): _description_
        extensions (_type_): _description_
        altered_notes (_type_): _description_
    """
    # TODO Shouldnt be messing with state variable in display code
    # but wasnt working on first attempt to change
    # root = NoteGeneric(name=root_note)

    add_chord_to_prog(chord)
    set_state_val("adding_chord", False)



def submit_generic_chord_to_prog(
    root_degree, chord_type, slash_value, inversion_value, extensions, altered_notes
) -> None:
    """Creates a generic chord (uses scale degrees for the name, no notes.), adds to progression.

    Args:
        root_degree (_type_): _description_
        chord_type (_type_): _description_
        slash_value (_type_): _description_
        inversion_value (_type_): _description_
        extensions (_type_): _description_
        altered_notes (_type_): _description_
    """
    chord = ChordGeneric(
        degree=root_degree,
        type=chord_type,
        slash_value=slash_value,
        inversion=inversion_value,
        extensions=extensions,
        altered_notes=altered_notes,
    )

    add_chord_to_prog(chord)
    set_state_val("adding_chord", False)

# ******************************** #
# Set Midi Page display Fns
# ******************************** #


def set_time_signature():
    """Collect time signature args, sets state"""
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
    set_state_val("time_settings", (bpm, beats_per_measure, note_duration_per_beat))


def chord_midi_form(chord: Chord, chord_idx: int, prog_idx: int):
    key = f"{str(chord)}.{chord_idx}.{prog_idx}"
    cols = st.columns(5)
    cols[0].markdown(f"<h4>Chord<br>{str(chord)}</h4>", unsafe_allow_html=True)

    # arp = cols[1].checkbox("Arpeggiate", value=False, key="arp." + key, disabled=True)
    rand_vel = cols[1].checkbox("Random Velocity", value=False, key="rand_vel." + key)
    velocity = cols[2].slider(
        "Velocity",
        min_value=midi_vel_low,
        max_value=midi_vel_high,
        disabled=rand_vel,
        value=100,
        key="velocity." + key,
    )
    octave = cols[3].number_input(
        "Octave",  min_value=2, max_value=6, value=4, key="octave." + key
    )
    note_duration = cols[4].select_slider(
        "Note Length (in beats)",
        note_lengths,
        value=note_lengths[4],
        key="note_duration." + key,
        help="1 means play for one beat, so a quarter note. 0.25 -> sixteenth note. 4 -> whole note."
    )
    # playbacks = cols[3].number_input(
    #     "Play _ times",
    #     min_value=1,
    #     max_value=16,
    #     value=1
    # )

    return {
        "arpeggiated": False,
        # "playbacks":playbacks,
        "random_velocity": rand_vel,
        "velocity": velocity,
        "octave": octave,
        "note_duration": note_duration,
    }


def generate_track_form(container: st.container) -> None:
    with container:
        set_state_val(
            "file_name", st.text_input("Midi File Name", value="midi_notes") + ".mid"
        )

        set_state_val(
            "create_bass_track",
            st.checkbox(
                "Create separate bass note track",
                value=False,
                help="Take the bass note of each chord, and add it to a separate track.",
            ),
        )

        cols = st.columns(2)
        result = cols[0].button("Generate MIDI File", on_click=generate_midi_files)
        download_button_empty = cols[1].empty()

        if result:
            st.success("MIDI created successfully")
            with open(get_state_val("file_name"), "rb") as f:
                download_button_empty.download_button(
                    "Download File", f, file_name=get_state_val("file_name")
                )

