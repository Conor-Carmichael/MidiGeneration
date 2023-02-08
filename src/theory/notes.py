"""
File to structure use for notes.
Author: Conor Carmichael

"""

from src.utils.utils import (
    get_pitch_from_midi_value, 
    get_note_from_midi
)
from typing import *
from src.theory.constants import SHARP, FLAT
import numpy as np


class NoteGeneric:

    """Note class with no pitch or midi information"""

    def __init__(self, name:str, next_note, prev_note) -> None:
        self.name = name
        self.base_note_name = self.name[0]
        self.alter = self.name[1:] if len(self.name) > 1 else ""

        self.next_note = next_note
        self.prev_note = prev_note

    def __str__(self) -> str:
        return f"{self.base_note_name}{self.alter}"

    def __iter__(self):
        return self.next_note

    def sharpen(self, keep_base_note_name:bool):
        """Does not change base note name if not requested, just adds sharp"""
        if keep_base_note_name:
            self.alter += SHARP
        else:
            self.base_note_name = self.next_note.base_note_name

    def flatten(self, keep_base_note_name:bool):
        if keep_base_note_name:
            self.alter += FLAT
        else:
            self.base_note_name = self.prev_note.base_note_name


class Note(NoteGeneric):

    """
    To allow for more significant alterations, the Note class.
    """

    def __init__(self, midi_value: int, *args, **kwargs) -> None:
        super(Note, self).__init__(*args, **kwargs)
        self.midi_value = midi_value
        self.pitch = get_pitch_from_midi_value(self.midi_value)


    def change_name_notation(self, new_base_note: str, new_alter: str) -> None:
        self.base_note_name = new_base_note
        self.alter = new_alter
        self.name = self.base_note_name + self.alter

    def sharpen(self, keep_base_note_name: bool = True):
        """Does not change base note name if not requested, just adds sharp"""
        super().sharpen(keep_base_note_name)
        self.pitch = self.pitch * np.power(2, 1 / 12)

    def flatten(self, keep_base_note_name: bool = False):
        """Does not change base note name if not requested, just adds flat"""
        super().flatten(keep_base_note_name)

        self.pitch = self.pitch * np.power(2, -1 * (1 / 12))



class Notes:
    """LinkedList Structure to encode distance between notes"""

    def __init__(self, notes: List[Note]) -> None:
        self.notes = notes

    def __len__(self) -> int:
        return len(self.notes)

    @classmethod
    def get_notes(cls):
        prev_note = None
        notes = []
        for midi_value in range(0, 128):
            note_name = get_note_from_midi(midi_value)
            note = Note(
                name=note_name,
                midi_value=midi_value,
                prev_note=prev_note,
                next_note=None,
            )
            notes.append(note)
            if prev_note:
                prev_note.next_note = note

            prev_note = note

        return Notes(notes)

    def __getitem__(self, req: str):
        return list(filter(lambda note: note.name == req, self.notes))

    def get_note_by_midi(self, req: int):
        return list(filter(lambda note: note.midi_value == req, self.notes))

    def get_note_by_pitch(self, req: float):
        return list(filter(lambda note: note.pitch == req, self.notes))


AllNotes = Notes.get_notes()