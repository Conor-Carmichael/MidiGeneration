from theory import *


class Scale:
    def __init__(self, root: Note, formula: List[StepType], name: AnyStr) -> None:
        self.root = root
        self.formula = formula
        self.name = name
        self.scale_notes = []
        self._set_notes()

    def _set_notes(self) -> List[Note]:
        self.notes = [self.root]
        last_note_idx = Notes.index(self.root.name)
        for step in self.formula:
            next_note_idx = (last_note_idx + step) % len(Notes)
            next_note = Note[Notes[next_note_idx]]
            self.notes.append(next_note)
            last_note_idx = next_note_idx

    def get_midi(self) -> List[midi.MIDIFile]:
        pass
