from abc import ABC, abstractmethod
from src.theory.datatypes import StepSequence
from src.theory.constants import SHARP, FLAT, midi_end_val, midi_start_val
from src.theory.notes import Note, NoteGeneric
from typing import *
from midiutil import MidiFile


class NoteSequence:
    """General class for sequences of notes (scales, chords, melodies...)"""

    _note_strings = [
        "C",
        "C" + SHARP,
        "D",
        "D" + SHARP,
        "E",
        "F",
        "F" + SHARP,
        "G",
        "G" + SHARP,
        "A",
        "A" + SHARP,
        "B",
    ]

    def __init__(
        self, notes:List[Union[NoteGeneric, Note]], name: str=None
    ) -> None:
        self.notes = notes
        self.name = name

    def __contains__(self, ele) -> bool:
        return ele.name in [n.name for n in self.notes]

    def __len__(self) -> int:
        return len(self.notes)

    def __str__(self) -> str:
        return ", ".join([n.name for n in self.notes])

    def __getitem__(self, req: str) -> List:
        return list(filter(lambda note: note.name == req, self.notes))

    def get_idxs(self, note_name: str) -> List[int]:
        """Get the index of where the note appears in list"""
        locs = []
        for idx, elem in enumerate(self.notes):
            locs += [idx] if elem.name == note_name else []
        return locs

    def get_note_by_idx(self, req: int) -> Note:
        return self.notes[req]

    def get_note_by_midi(self, req: int) -> Note:
        try:
            return list(filter(lambda note: note.midi_value == req, self.notes))[0]

        except AttributeError as ae:
            print("'midi_value' only available on Note, not NoteGeneric")
            return []

    def get_note_by_pitch(self, req: float) -> Note:
        try:
            return list(filter(lambda note: note.pitch == req, self.notes))[0]

        except AttributeError as ae:
            print("'pitch' only available on Note, not NoteGeneric")
            return []

    def get_name(self) -> str:
        return self.name.title()

    def get_midi_value(self) -> List[int]:
        """Convert notes to midi values"""
        try:
            return [note.midi_value for note in self.notes]
        except AttributeError as ae:
            print("'midi_value' only available on Note, not NoteGeneric")
            return []

    def get_notes(self) -> List[Note]:
        return self.notes

class NotesFactory:

    def __init__(self) -> None:
        pass

    @classmethod
    def get_midi_notes(cls) -> NoteSequence:
        """Returns NoteSequence with notes list set, as either all midi notes, or basic notes [C,C)]"""
        notes = []
        prev_note = None

        for idx in range(midi_start_val, midi_end_val + 1):
            # Get name for the note
            note_name = cls._note_strings[idx % len(cls._note_strings)]

            # Create Note object
            note = Note(
                name=note_name,
                midi_value=idx,
                prev_note=prev_note,
                next_note=None,
            )
            # Add to list for cls
            notes.append(note)

            if prev_note:
                prev_note.next_note = note

            prev_note = note

        prev_note.next_note = note

        return NoteSequence(notes=notes, name="Midi Notes")

    @classmethod
    def get_generic_notes(cls) -> NoteSequence:
        """Returns NoteSequence with notes list set, as either all midi notes, or basic notes [C,C)]"""
        notes = []
        prev_note = None

        for note_name in NoteSequence._note_strings:
            # Get name for the note
            # Create Note object
            note = NoteGeneric(
                name=note_name,
                prev_note=prev_note,
                next_note=None,
            )
            # Add to list for cls
            notes.append(note)

            if prev_note:
                prev_note.next_note = note

            prev_note = note

        prev_note.next_note = note
        notes[0].prev_note = note # make circular

        return NoteSequence(notes=notes, name="Generic Notes")