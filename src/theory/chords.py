from src.theory import *
from src.theory.note_sequence import NoteSequence
from src.theory.notes import Note, NoteGeneric
from src.theory.constants import ChordFormulas, ChordSymbols, ChordType
from src.theory.scales import Scale, ScaleFactory, find_scale_factory_for_mode
from src.utils.utils import cycle_n_times
from random import randint

from numpy import log2


class ChordGeneric(NoteSequence):

    """Holds information to form a chord later when scale root is determined."""

    def __init__(
        self,
        degree: int,
        type: ChordType,
    ) -> None:
        ...


class Chord(NoteSequence):
    """
    Class for chord objects, built from a root note, and
    a scale to pull intervals from. Allows for inversions and
    chord extensions to be utilized
    """

    def __init__(
        self,
        root: Union[NoteGeneric, Note],
        type: ChordType,
        slash_value: Note = None,
        inversion: int = 0,
        extensions: List[int] = [],
        altered_notes: List[dict] = None,
        *args,
        **kwargs,
    ) -> None:
        """Initialize a Chord.

        Args:
            root (Union[NoteGeneric, Note]): Note for root of chord.
            type (ChordType): Enum of ChordType
            slash_value (Note, optional): Altered root note for the chord. Defaults to None.
            inversion (int, optional): Inversion value for chord. Defaults to 0.
            extensions (List[str], optional): Chord extensions, built off chord_type scale. Defaults to None.
            altered_notes (List[dict], optional): In format [{"degree": int, "fn": flatten/sharpen}, ...]. Defaults to None.

        Raises:
            NotImplementedError: Altered notes needs to be implemented for chords
        """

        self.root = root
        self.type = type
        self.inversion = (
            inversion
            if inversion in inversion_values
            else ValueError("Inversion value invalid")
        )
        self.slash_value = slash_value
        self.extensions = sorted(extensions)
        self.has_extensions = len(self.extensions) > 0 and max(self.extensions) > 8
        self.altered_notes = altered_notes

        if not self.slash_value is None and self.inversion > 0:
            raise ValueError("Cannot invert a slash chord.")

        self.formula = ChordFormulas.get(self.type, None)
        if kwargs.get("notes", None) is None:
            notes = self._set_notes()
        else:
            notes = kwargs["notes"]
            del kwargs["notes"]

        super(Chord, self).__init__(name=self.type.name, notes=notes, *args, **kwargs)

        if self.altered_notes:
            raise NotImplementedError("altered_notes for chord")
            self.set_altered_notes(notes)

    def __repr__(self) -> str:
        # TODO Set up to be ready for writeline to midi file
        s = f"Chord Name: {self.__str__()}\n"
        for n in self.notes:
            s += "\t" + repr(n) + "\n"

        return s

    def __str__(self) -> str:
        symb = (
            ChordSymbols[self.type][1]
            if self.has_extensions
            else ChordSymbols[self.type][0]
        )
        s = f"{self.root} {symb}"
        if self.has_extensions:
            # To calculate if C add 11 or just C 11.
            # Must include all sub extensions, so if index of the ext in the possible extensions,
            # Plus 1 is the same as the length of the current extensions, then all relevant ext
            # are included. IF extensions = [9, 11], max ext is 11, the index of 11 is 1, must be 2 extensions (9 and 11)
            # to be a C11 chord, else if only 11 is present its an Add 11 chord
            max_ext = max(self.extensions)
            max_ext_idx = extension_values.index(max_ext)

            if max_ext != 0 and max_ext_idx + 1 == len(self.extensions):
                ext_str = str(max_ext)
            else:
                ext_str = "add " + ", ".join([str(e) for e in self.extensions])

            s += " " + ext_str

        if self.slash_value:
            s += " / " + self.slash_value.name
        elif self.inversion > 0:
            s += f" / {self.notes[0]}"
        # if self.extensions:
        #     s
        return s

    def _set_notes(self) -> None:
        notes = []

        # Get relative scale
        base_scale_type = self.formula["scale"]
        sf = find_scale_factory_for_mode(base_scale_type)
        scale = sf.generate_scale(self.root)

        # Select appropriate notes, considering extensions
        notes = [scale.get_notes()[idx - 1] for idx in self.formula["intervals"]]
        if self.extensions:
            # TODO: Add in option for flat and sharp extensions

            # Add in the notes by mod the length of the scale // 9 is the 2, 11 is the 4..

            # NOTE: The octave is IN the scale. So add 9, the 8th index (9-1) is root note again
            # this messes with using mod to circulate through it
            # Dealt with in scale.get_interval

            notes.extend([scale.get_interval(val) for val in self.extensions])

        # Check for inversion
        if self.inversion > 0:
            notes = cycle_n_times(notes, self.inversion)

        # Check for altered root
        if self.slash_value:
            notes = [self.slash_value] + notes

        return notes

    def conv_notes_to_midi(self, octave: int) -> None:
        self.notes = [
            Note.get_from_generic(octave=octave, note=note) for note in self.notes
        ]

    def is_diatonic(self, scale: Scale) -> bool:
        """Checks if this chord is diatonic in the given scale"""
        return all([note in scale for note in self.notes])

    def add_midi_info(self, midi_instructions: dict) -> None:
        assert all(
            [
                midi_instructions.get(k, False)
                for k in ["start_time", "note_duration", "velocity", "octave"]
            ]
        ), "Cannot set midi info without prerequisite info."

        # If velocity is checked off to be random, calculate it, then delete from dict
        # so it can be dumped in as args
        if midi_instructions["random_velocity"]:
            midi_instructions["velocity"] = randint(midi_vel_low, midi_vel_high)
        del midi_instructions["random_velocity"]

        # TODO work in arpeggiation. For now just delete before passing as args
        del midi_instructions["arpeggiated"]

        # Use super class function to, for each note in chord, calculate the midi
        # value of the note, and collecte the midi information and tie it to each note.
        # Converts notes from 'NoteGeneric' to 'Note' (if they are not already)
        self.conv_generic_notes_to_midi_notes(**midi_instructions)
