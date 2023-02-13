"""
File to structure use for notes.
Author: Conor Carmichael

"""
from src.utils.utils import get_pitch_from_midi_value
from typing import *
from src.theory.constants import SHARP, FLAT, midi_start_val, midi_end_val
import numpy as np


class NoteGeneric:

    """Note class with no pitch or midi information. Basically just the name."""

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
        """
        Does not change base note name if not requested, just adds sharp.
        Sometimes it is more proper to have a Bbb rather than A. 
        """
        if keep_base_note_name:
            self.name += SHARP
            self.alter += SHARP
        else:
            self.name = self.next_note.name
            self.base_note_name = self.name[0]
            self.alter = self.name[1:] if len(self.name) > 1 else ""

    def flatten(self, keep_base_note_name: bool):
        """
        Does not change base note name if not requested, just adds flat.
        Sometimes it is more proper to have a Bbb rather than A. 
        """
        if keep_base_note_name:
            self.alter += FLAT
            self.name += FLAT
        else:
            self.name = self.prev_note.name
            self.base_note_name = self.name[0]
            self.alter = self.name[1:] if len(self.name) > 1 else ""

    def __repr__(self) -> str:
        return f"{self.name}"

class Note(NoteGeneric):

    """
    To allow for more significant use, the Note class.
    Holds pitch, velocity, duration, start time, midi value for the note.
    """

    def __init__(self, midi_value: int, duration:int, velocity:int, start_time:any, *args, **kwargs) -> None:
        super(Note, self).__init__(*args, **kwargs)
        self.midi_value = midi_value
        self.duration = duration
        self.velocity = velocity
        self.start_time = start_time
        assert midi_start_val < self.midi_value < midi_end_val , f"MIDI value is out of range for {self.name} with value of {self.midi_value}"
        self.pitch = get_pitch_from_midi_value(self.midi_value)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, NoteGeneric) and self.midi_value == __o.midi_value:
            return True
        else:
            return False

    def change_name_notation(self, new_base_note: str, new_alter: str) -> None:
        """
        Sometimes it is more proper to have a Bbb rather than A. 
        If the name needs to be changed to A though this fn does so        
        """
        self.base_note_name = new_base_note
        self.alter = new_alter
        self.name = self.base_note_name + self.alter

    def sharpen(self, keep_base_note_name: bool = True):
        """Does not change base note name if not requested, just adds sharp to the str"""
        super().sharpen(keep_base_note_name)
        self.pitch = self.pitch * np.power(2, 1 / 12)

    def flatten(self, keep_base_note_name: bool = False):
        """Does not change base note name if not requested, just adds flat to the str"""
        super().flatten(keep_base_note_name)
        self.pitch = self.pitch * np.power(2, -1 * (1 / 12))


    def __repr__(self) -> str:
        return f"{self.name}={self.midi_value} (Vel:{self.velocity}, Dur:{self.duration}, T:{self.start_time})"