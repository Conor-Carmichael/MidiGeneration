import abc
from src.theory import *
from src.theory.scales import Scale
from abc import ABC


class Chord(ABC):
    def __init__(
        self,
        root_note: Note,
        type: ChordTypes,
        formula: Dict,
        slash_value: Note,
        symbols: List[str],
        inversion: int = 0,
        # qualities:List[str],
        extensions: List[str] = None,
        octave: int = 4,
    ) -> None:
        self.root_note = root_note
        self.type = type
        self.inversion = inversion
        self.slash_value = slash_value
        self.symbols = symbols
        self.formula = formula
        # self.qualities = qualities
        self.extensions = extensions
        self.octave = octave

        self._set_notes()

    def _interval_rotation(self, notes) -> List[Note]:
        notes = [notes[i + 1] for i in range(len(notes - 1))] + notes[0]
        return notes

    def _set_notes(self) -> None:
        notes = []

        # Get relative scale
        base_scale_type = self.formula.scale
        base_scale_formula = ScaleFormulas.get(base_scale_type)
        scale = Scale(root_note=self.root_note, formula=base_scale_formula)

        # Select appropriate notes, considering extensions
        notes = [scale.notes[idx] for idx in self.formula.intervals]
        if self.extensions:
            notes.extend([scale[val] for val in self.extensions])

        # Check for inversion
        for _ in range(self.inversion):
            notes = self._interval_rotation(notes)

        # Check for altered root
        if self.slash_value:
            notes = [self.slash_value] + notes

        self.chord_notes = notes

    def get_notes(self) -> List[Note]:
        return self.chord_notes

    def get_midi(self, notes_list: List[Note]) -> List[midi.MIDIFile]:
        pass

    def is_diatonic(self, scale: Scale) -> bool:
        pass
