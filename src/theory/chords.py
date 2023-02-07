from src.theory import *
from src.theory.note_sequence import NoteSequence
from src.theory.constants import ChordFormulas, ChordSymbols, ChordType
from src.theory.scales import Scale
from src.utils.utils import cycle_n_times


class Chord(NoteSequence):
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
        super().__init__(formula=formula, name=self.type.name, *args, **kwargs)

    def _set_notes(self) -> None:
        notes = []

        # Get relative scale
        base_scale_type = self.formula["scale"]
        base_scale_formula = ScaleFormulas.get(base_scale_type)
        scale = Scale(root=self.root, formula=base_scale_formula, name='scale')

        # Select appropriate notes, considering extensions
        # TODO why is this minus 1 needed
        notes = [scale.notes[idx-1] for idx in self.formula['intervals']]
        if self.extensions:
            notes.extend([scale[val] for val in self.extensions])

        # Check for inversion
        if self.inversion:
            notes = cycle_n_times(self.inversion)

        # Check for altered root
        if self.slash_value:
            notes = [self.slash_value] + notes

        self.notes = notes

    def is_diatonic(self, scale: Scale) -> bool:
        pass
