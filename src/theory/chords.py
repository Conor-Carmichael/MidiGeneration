from src.theory import *
from src.theory.note_sequence import NoteSequence
from src.theory.notes import Note
from src.theory.constants import ChordFormulas, ChordSymbols, ChordType
from src.theory.scales import Scale, ScaleFactory, find_scale_factory_for_mode
from src.utils.utils import cycle_n_times


class Chord(NoteSequence):
    """
    Class for chord objects, built from a root note, and
    a scale to pull intervals from. Allows for inversions and
    chord extensions to be utilized
    """

    def __init__(
        self,
        type: ChordType,
        slash_value: Note = None,
        inversion: int = 0,
        extensions: List[str] = None,
        *args,
        **kwargs
    ) -> None:
        self.type = type
        self.inversion = inversion
        self.slash_value = slash_value
        self.extensions = extensions

        formula = ChordFormulas.get(self.type, None)
        super(Chord, self).__init__(
            formula=formula, name=self.type.name, *args, **kwargs
        )

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
        if self.inversion:
            notes = cycle_n_times(self.inversion)

        # Check for altered root
        if self.slash_value:
            notes = [self.slash_value] + notes

        self.notes = notes

    def is_diatonic(self, scale: Scale) -> bool:
        """Checks if this chord is diatonic in the given scale"""
        return all([note in scale.get_notes() for note in self.notes])
