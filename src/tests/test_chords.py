import pytest
from src.theory.chords import Chord
from src.theory.scales import *
from src.theory import *


@pytest.mark.parametrize(
    "root,expected",
    [
        (Note.C, [Note.C, Note.E, Note.G]),
        (Note.D, [Note.D, Note.Fsharp, Note.A]),
        (Note.B, [Note.B, Note.Dsharp, Note.Fsharp]),
    ],
)
def test_major_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MAJOR,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected


@pytest.mark.parametrize(
    "root,expected",
    [
        (Note.C, [Note.C, Note.Dsharp, Note.G]),
        (Note.D, [Note.D, Note.F, Note.A]),
        (Note.B, [Note.B, Note.D, Note.Fsharp]),
    ],
)
def test_minor_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MINOR,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected


@pytest.mark.parametrize(
    "root,expected",
    [
        (Note.B, [Note.B, Note.D, Note.F]),
        (Note.C, [Note.C, Note.Dsharp, Note.Fsharp]),
    ],
)
def test_diminished_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.DIMINISHED,
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected


@pytest.mark.parametrize(
    "root,extensions,expected",
    [
        (Note.C, [], [Note.C, Note.E, Note.G]),
        (Note.D, None, [Note.D, Note.Fsharp, Note.A]),
        (Note.C, [9], [Note.C, Note.E, Note.G, Note.D]),
        (Note.C, [6], [Note.C, Note.    E, Note.G, Note.A]),
        (Note.C, [9, 11, 13], [Note.C, Note.E, Note.G, Note.D, Note.F, Note.A]),
    ],
)
def test_major_chord_extensions(root, extensions, expected):
    args = {
        "root": root,
        "type": ChordType.MAJOR,
        "extensions": extensions
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected
@pytest.mark.parametrize(
    "root,extensions,expected",
    [
        (Note.C, [], [Note.C, Note.Dsharp, Note.G]),
        (Note.C, [7], [Note.C, Note.Dsharp, Note.G, Note.Asharp]),
        (Note.C, [9], [Note.C, Note.Dsharp, Note.G, Note.D]),
        (Note.C, [13], [Note.C, Note.Dsharp, Note.G, Note.Gsharp]),
        (Note.C, [9, 13], [Note.C, Note.Dsharp, Note.G,Note.D, Note.Gsharp]),
    ],
)
def test_minor_chord_extensions(root, extensions, expected):
    args = {
        "root": root,
        "type": ChordType.MINOR,
        "extensions": extensions
    }
    chord = Chord(**args)
    assert chord.get_notes() == expected

@pytest.mark.parametrize(
    "chord,scale,expected", [
        (Chord(root=Note.C, type=ChordType.MAJOR), IonianScaleFact.generate_scale(Note.C), True),
        (Chord(root=Note.D, type=ChordType.MAJOR), IonianScaleFact.generate_scale(Note.C), False),
        (Chord(root=Note.G, type=ChordType.SEVENTH), IonianScaleFact.generate_scale(Note.C), True),
        (Chord(root=Note.A, type=ChordType.SEVENTH), MixolydianFlat6Fact.generate_scale(Note.Asharp), False),
        (Chord(root=Note.A, type=ChordType.MAJOR_SEVENTH), MixolydianFlat6Fact.generate_scale(Note.Asharp), False)
    ]
)
def test_is_diatonic(chord, scale, expected):
    assert chord.is_diatonic(scale) == expected