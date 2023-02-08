from abc import ABC, abstractmethod
from src.theory import *
from midiutil import MidiFile


class NoteSequence(ABC):
    """General class for sequences of notes (scales, chords, melodies...)"""

    def __init__(
        self, root: Note, formula: StepSequence, name: str, octave: int = 4
    ) -> None:
        self.root = root
        self.formula = formula
        self.octave = octave
        self.name = name
        self.notes = []

        self._set_notes()

    @abstractmethod
    def _set_notes(self) -> None:
        """Specific to subclasses, scales and chords will be different implemenations"""
        ...

    def get_notes(self) -> List[Note]:
        return self.notes

    def get_name(self) -> str:
        return self.name.title()

    def get_midi_value(self, velocity: Any, bpm: int, note_lengths: Any) -> MidiFile:
        """Convert notes to midi values"""

        calc_midi = lambda nv: midi_start_val * self.octave + nv
        midi_notes = [calc_midi(note.value) for note in self.notes]
        midi_notes_filtered = list(
            filter(lambda n: midi_end_val > n > midi_start_val, midi_notes)
        )

        return midi_notes_filtered
