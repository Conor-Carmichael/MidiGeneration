import pytest
from src.theory.chords import Chord
from src.theory import *


@pytest.mark.parametrize("root,expected", [
    (Note.C, [Note.C, Note.E, Note.G]),
    (Note.D, [Note.D, Note.Fsharp, Note.A]),
    (Note.B, [Note.B, Note.Dsharp, Note.Fsharp]),
])
def test_major_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MAJOR,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected

@pytest.mark.parametrize("root,expected", [
    (Note.C, [Note.C, Note.Dsharp, Note.G]),
    (Note.D, [Note.D, Note.F, Note.A]),
    (Note.B, [Note.B, Note.D, Note.Fsharp]),
])
def test_minor_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MINOR,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected

@pytest.mark.parametrize("root,expected", [
    (Note.B, [Note.B, Note.D, Note.F]),
    (Note.C, [Note.C, Note.Dsharp, Note.Fsharp]),
])
def test_diminished_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.DIMINISHED,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected