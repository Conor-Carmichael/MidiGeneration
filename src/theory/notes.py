"""
File to structure use for notes.
Author: Conor Carmichael

"""
from src.utils.utils import get_pitch_from_midi_value
from typing import *
from src.theory.constants import SHARP, FLAT, midi_start_val, midi_end_val
import numpy as np


class NoteGeneric:

    """Note class with no pitch or midi information"""

    def __init__(self, name: str, next_note=None, prev_note=None) -> None:
        self.name = name
        self.base_note_name = self.name[0]
        self.alter = self.name[1:] if len(self.name) > 1 else ""

        self.next_note = next_note
        self.prev_note = prev_note

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, NoteGeneric) and self.name == __o.name:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.base_note_name}{self.alter}"

    def __iter__(self):
        return self.next_note

    def sharpen(self, keep_base_note_name: bool):
        """Does not change base note name if not requested, just adds sharp"""
        if keep_base_note_name:
            self.name += SHARP
            self.alter += SHARP
        else:
            self.name = self.next_note.name
            self.base_note_name = self.name[0]
            self.alter = self.name[1:] if len(self.name) > 1 else ""

    def flatten(self, keep_base_note_name: bool):
        if keep_base_note_name:
            self.alter += FLAT
            self.name += FLAT
        else:
            self.name = self.prev_note.name
            self.base_note_name = self.name[0]
            self.alter = self.name[1:] if len(self.name) > 1 else ""


class Note(NoteGeneric):

    """
    To allow for more significant alterations, the Note class.
    """

    def __init__(self, midi_value: int, *args, **kwargs) -> None:
        super(Note, self).__init__(*args, **kwargs)
        self.midi_value = midi_value
        self.pitch = get_pitch_from_midi_value(self.midi_value)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, NoteGeneric) and self.midi_value == __o.midi_value:
            return True
        else:
            return False

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
