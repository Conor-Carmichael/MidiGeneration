from abc import ABC
from src.theory import *
from src.theory.note_sequence import NoteSequence, NotesFactory
from src.theory.notes import Note, NoteGeneric
from src.utils.utils import cycle_n_times


class Scale(NoteSequence):
    """
    Class to calculate the notes in a scale, and get the chords.
    """

    def __init__(
        self,
        root: Union[NoteGeneric, Note],
        formula: StepSequence,
        chord_mapping: List[ChordType] = None,
        altered_notes: List = None,
        *args,
        **kwargs,
    ) -> None:
        """Initializer a Scale object

        Args:
            root (Union[NoteGeneric, Note]): Note obj for root of scale
            formula (StepSequence): How to derive the scale
            chord_mapping (List[List[ChordType]], optional): Map a scale degree to a chord type. Defaults to None.
            altered_notes (List, optional): In format [{"degree": int, "fn": flatten/sharpen}, ...]. Defaults to None.
        """
        self.root = root
        self.formula = formula
        self.chord_mapping = chord_mapping
        self.altered_notes = altered_notes
        notes = self._set_notes()

        super(Scale, self).__init__(notes=notes, *args, **kwargs)

        if self.altered_notes:
            self.set_altered_notes(notes)


    def _set_notes(self) -> List[Note]:
        """Used to set the notes of the scale based on the root and formula.

        Returns:
            List[Note]: Returns value for clarity, and set it in __init__
        """
        notes_set = NotesFactory.get_generic_notes()
        notes = [self.root]
        prev_note = self.root
        last_note_idx = notes_set.get_idxs(self.root.name)[0]

        for step in self.formula:
            note_idx = (last_note_idx + step) % len(notes_set)
            note_name = notes_set.get_note_by_idx(note_idx).name

            note = NoteGeneric(name=note_name, next_note=None, prev_note=prev_note)
            notes.append(note)

            last_note_idx = note_idx
            prev_note = note

        prev_note.next_note = note
        notes[0].prev_note = note  # make circular

        return notes

    def _adjust_notation(self) -> None:
        """
        Check scale notation for repeated notes, change sharp flat accordingly
        Root note is stuck.
        """

        unique_notes = 0

    def get_interval(self, interval: int) -> Note:
        """Get the scale degree for the given interval

        Args:
            interval (int): What to get.

        Returns:
            Note: Returns the note requested.
        """
        # TODO clean this up, kinda confusing.
        # If I mod it, I mod it by a lower length.
        # If not, the 'second' is actually the index pos 1
        # But the ninth is 9 mod 7  ....
        # It currently works.
        mod_len = len(self.notes[:-1])
        return self.notes[:-1][
            (interval % mod_len) - 1 if interval > mod_len else interval - 1
        ]

    def get_available_chords(self) -> List[NoteSequence]:
        chords = []
        return chords


# Define scale information
class ScaleFactory:
    """
    A class to standardize the instructions to create scales, define modes, and generate scales.
    and order the modes of a scale.
    Generates Scale objects.
    """

    def __init__(
        self,
        name: Union[str, Enum],
        steps: StepSequence,
        chord_mappings: List[ChordType] = None,
        modes: List[str] = None,
    ) -> None:
        self.name = name  # Can be enum or string
        self.steps = steps
        self.chord_mappings = chord_mappings
        self.modes = modes

    def has_modes(self) -> bool:
        """Returns true if this scale has a list of modes"""
        return not self.modes is None

    def has_mode(self, mode_name: Enum) -> bool:
        """Returns true if supplied mode is in list of modes"""
        return mode_name in self.modes

    def has_chord_mappings(self) -> bool:
        return not self.chord_mappings is None

    def get_mode_definition(self, mode_name: Enum) -> Any:
        """
        For the supplied mode,
            * rotate the step sequence to reflect the new mode
            * rotate the chord mapping to reflect the new mode
        The new mode cannot have modes, to avoid confusion.

        If the supplied mode is not available, None is returned.
        If the instance does not have modes, None is returned.
        """
        if self.has_modes() and self.has_mode(mode_name):
            rotations = (
                mode_name.value - 1
            )  # Minus 1 because the first mode in enum has val 1
            new_step_seq = cycle_n_times(self.steps, n=rotations)
            rotated_chord_mappings = cycle_n_times(self.chord_mappings, n=rotations)

            # Leave modes as none, no need for modes stored on a modulated scale
            return ScaleFactory(
                mode_name,
                new_step_seq,
                rotated_chord_mappings,
            )

        else:
            return None

    def generate_scale(self, root_note: Note, altered_notes: dict = None) -> Scale:
        return Scale(
            root=root_note,
            formula=self.steps,
            chord_mapping=self.chord_mappings,
            name=self.name,
            altered_notes=altered_notes,
        )


IonianScaleFact = ScaleFactory(
    "Major Scale",
    IonianFormula,
    IonianChordFormulas,
    modes=[i for i in MajorModes],
)
PentatonicScaleFact = ScaleFactory("Major Pentatonic", PentatonicFormula)
WholeToneScaleFact = ScaleFactory("Whole Tone", WholeToneFomula)
HarmonicMinScaleFact = ScaleFactory("Harmonic Minor", HarmonicMinorFormula)
MelodicMinScaleFact = ScaleFactory("Meolodic Minor", MelodicMinorFormula)
BluesScaleFact = ScaleFactory("Blues", BluesFormula)
MixolydianFlat6Fact = ScaleFactory("Mixolydian Flat 6", MixolydianFlat6Formula)

AllScaleFactories = [
    IonianScaleFact,
    PentatonicScaleFact,
    MixolydianFlat6Fact,
    BluesScaleFact,
    MelodicMinScaleFact,
    HarmonicMinScaleFact,
    WholeToneScaleFact,
]


def find_scale_factory_for_mode(mode_name: Union[str, Enum]) -> ScaleFactory:
    for sf in AllScaleFactories:
        if sf.has_mode(mode_name):
            return sf.get_mode_definition(mode_name)
    raise ValueError(f"Mode {mode_name} was not found in any scale")
