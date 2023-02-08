from abc import ABC
from src.theory import *
from src.theory.note_sequence import NoteSequence
from src.utils.utils import cycle_n_times


class Scale(NoteSequence):
    """
    Class to calculate the notes in a scale, and get the chords
    """

    def __init__(self, chord_mapping: List[ChordType], *args, **kwargs) -> None:
        super(Scale, self).__init__(*args, **kwargs)
        self.chord_mapping = chord_mapping
        self._set_notes()

    def _set_notes(self) -> List[Note]:
        self.notes = [self.root]
        last_note_idx = Notes.index(self.root.name)
        for step in self.formula:
            next_note_idx = (last_note_idx + step) % len(Notes)
            next_note = Note[Notes[next_note_idx]]
            self.notes.append(next_note)
            last_note_idx = next_note_idx

    def get_interval(self, interval:int) -> Note:
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

    def generate_scale(self, root_note: Note, octave: int = 4) -> Scale:
        return Scale(
            self.chord_mappings,
            root=root_note,
            formula=self.steps,
            name=self.name,
            octave=octave,
        )


IonianScaleFact = ScaleFactory(
    IonianModes.IONIAN,
    IonianFormula,
    IonianChordFormulas,
    modes=[i for i in IonianModes],
)

PentatonicScaleFact = ScaleFactory(PentatonicModes.MAJOR, PentatonicFormula)

WholeToneScaleFact = ScaleFactory("Whole Tone", WholeToneFomula)

MixolydianFlat6Fact = ScaleFactory("Mixolydian Flat 6", MixolydianFlat6Formula)

AllScaleFactories = [
    IonianScaleFact,
    PentatonicScaleFact,
    WholeToneScaleFact,
    MixolydianFlat6Fact,
]


def find_scale_factory_for_mode(mode_name: Union[str, Enum]) -> ScaleFactory:
    for sf in AllScaleFactories:
        if sf.has_mode(mode_name):
            return sf.get_mode_definition(mode_name)
    raise ValueError(f"Mode {mode_name} was not found in any scale")
