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

    def __init__(self, notes: List[Union[NoteGeneric, Note]], name: str = None) -> None:
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

    def set_altered_notes(self, notes) -> None:
        """
        For each note alteration instrcution, find the degree in
        the set of notes and adjust it
        """
        assert len(self.altered_notes) < 7, "Cannot alter seven notes"
        for alt in self.altered_notes:
            deg_idx = alt["degree"] - 1
            assert 8 > deg_idx > 1, "Degree index must be between 1, 8 uninclusive."
            fn = getattr(notes[deg_idx], alt["fn"])
            # operates in place..
            fn(keep_base_note_name=True)
            # self.notes[deg] = new_note

    def get_idxs(self, note_name: str) -> List[int]:
        """Get the index of where the note appears in sequence"""
        locs = []
        for idx, elem in enumerate(self.notes):
            locs += [idx] if elem.name == note_name else []
        return locs

    def get_note_by_idx(self, req: int) -> Note:
        """Index into the sequence of notes"""
        return self.notes[req]

    def get_note_by_midi(self, req: int) -> Note:
        """
        Return the note with the matching midi value
        Raises Attr Error if midi values are not set
        """
        try:
            return list(filter(lambda note: note.midi_value == req, self.notes))[0]

        except AttributeError as ae:
            raise AttributeError("Midi values are not set on this NoteSequence")

    def get_note_by_pitch(self, req: float) -> Note:
        """
        Return the note with the matching pitch value
        Raises Attr Error if pitch values are not set
        """
        try:
            return list(filter(lambda note: note.pitch == req, self.notes))[0]

        except AttributeError as ae:
            raise AttributeError("Pitch values are not set on this NoteSequence")

    def get_name(self) -> str:
        """Returns the name of the note sequence"""
        return self.name.title()

    def get_midi_value(self) -> List[int]:
        """
        Return each notes midi values in list
        Raises Attr Error if midi values are not set
        """
        try:
            return [note.midi_value for note in self.notes]
        except AttributeError as ae:
            raise AttributeError("Midi values are not set on this NoteSequence")

    def get_notes(self) -> List[Note]:
        """Return the notes of this sequence"""
        return self.notes

    def conv_generic_notes_to_midi_notes(
        self, start_time: int, note_duration: int, velocity: int, octave: int
    ) -> None:
        """Converts the Notes in this sequence (which may be NoteGeneric) to Note, containing
        the relevant midi information.

        Args:
            start_time (int): Not Implemented Yet! But will be the start time for the note to sound
                * Note start time is currently dynamically calculated. So it is set to whatever the
                next beat to play on is, based on all the prior chords in progression.
            note_duration (int): Length (in beats) to play the note.
            velocity (int): Loudness of note, per midi format
            octave (int): Which octave to sound the note in.
        """

        # Holds the new note objects to set all at end
        new_notes = []

        for note in self.notes:
            # For each note, calc the midi value for it
            midi_value = (octave * len(self._note_strings)) + self._note_strings.index(
                note.name
            )

            new_notes.append(
                Note(
                    midi_value=midi_value,
                    duration=note_duration,
                    velocity=velocity,
                    start_time=start_time,
                    name=note.name,
                    next_note=note.next_note,
                    prev_note=note.prev_note,
                )
            )
        # Set the cls variable to overwrite the old (potentially) NoteGeneric
        self.notes = new_notes


class NotesFactory:
    """Class to generate a set of Note objects.
    Either midi info containing notes, or generic notesss
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def get_midi_notes(cls) -> NoteSequence:
        """Returns NoteSequence with notes list set, all midi notes"""
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

        prev_note.next_note = notes[0]
        notes[0].prev_note = note  # make circular

        return NoteSequence(notes=notes, name="Generic Notes")
