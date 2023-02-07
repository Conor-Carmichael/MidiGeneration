from abc import ABC
from src.theory.note_sequence import NoteSequence
from theory import *


class Scale(NoteSequence):
    def __init__(
        self, 
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._set_notes()

    def _set_notes(self) -> List[Note]:
        self.notes = [self.root]
        last_note_idx = Notes.index(self.root.name)
        for step in self.formula:
            next_note_idx = (last_note_idx + step) % len(Notes)
            next_note = Note[Notes[next_note_idx]]
            self.notes.append(next_note)
            last_note_idx = next_note_idx
