import pytest
from src.theory.constants import SHARP, FLAT
from src.theory.notes import Note, NoteGeneric


# def test_get_notes():
#     midi_notes = Notes.get_notes(midi=True)
#     assert midi_notes.notes[0].name == "C"
#     assert midi_notes.notes[21].name == "A"
#     assert midi_notes.notes[60].name == "C"
#     assert midi_notes.notes[59].name == "B"
#     assert len(midi_notes) == 128

#     notes = Notes.get_notes(midi=False)
#     assert len(notes) == 12


# @pytest.mark.parametrize(
#     "start,expected",
#     [
#         ("C", "C" + SHARP),
#         ("E", "F"),
#     ],
# )
# def test_next_notes(start, expected):
#     notes = Notes.get_notes()

#     assert notes[start][0].next_note.name == expected


# @pytest.mark.parametrize(
#     "start,expected",
#     [
#         ("C", "B"),
#         ("F", "E"),
#     ],
# )
# def test_prev_notes(start, expected):
#     notes = Notes.get_notes(midi=False)

#     assert notes[start][0].prev_note.name == expected


# def test_flatten():
#     a = NoteGeneric("A", None, None)
#     a.flatten(keep_base_note_name=True)
#     assert a.name == "A" + FLAT

#     a = NoteGeneric("C", None, NoteGeneric("B"))
#     a.flatten(keep_base_note_name=False)
#     assert a.name == "B"
