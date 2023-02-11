import pytest
from src.theory.chords import Chord
from src.theory.note_sequence import NotesFactory

from src.theory.scales import *
from src.theory import *

NOTES = NotesFactory.get_generic_notes()


@pytest.mark.parametrize(
    "root,expected",
    [
        (NOTES["C"][0], "C, E, G"),
        (NOTES["D"][0], f"D, F{SHARP}, A"),
        (NOTES["B"][0], f"B, D{SHARP}, F{SHARP}"),
    ],
)
def test_major_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MAJOR,
    }
    chord = Chord(**args)
    assert str(chord) == expected


@pytest.mark.parametrize(
    "root,expected",
    [
        (NOTES["C"][0], f"C, D{SHARP}, G"),
        (NOTES["D"][0], f"D, F, A"),
        (NOTES["B"][0], f"B, D, F{SHARP}"),
    ],
)
def test_minor_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.MINOR,
    }
    chord = Chord(**args)
    assert str(chord) == expected


@pytest.mark.parametrize(
    "root,expected",
    [
        (NOTES["B"][0], f"B, D, F"),
        (NOTES["C"][0], f"C, D{SHARP}, F{SHARP}"),
    ],
)
def test_diminished_triad(root, expected):
    args = {
        "root": root,
        "type": ChordType.DIMINISHED,
    }
    chord = Chord(**args)
    assert str(chord) == expected


@pytest.mark.parametrize(
    "root,extensions,expected",
    [
        (NOTES["C"][0], [], f"C, E, G"),
        (NOTES["D"][0], None, f"D, F{SHARP}, A"),
        (NOTES["C"][0], [9], f"C, E, G, D"),
        (NOTES["C"][0], [6], f"C, E, G, A"),
        (
            NOTES["C"][0],
            [9, 11, 13],
            f"C, E, G, D, F, A",
        ),
    ],
)
def test_major_chord_extensions(root, extensions, expected):
    args = {"root": root, "type": ChordType.MAJOR, "extensions": extensions}
    chord = Chord(**args)
    assert str(chord) == expected


@pytest.mark.parametrize(
    "root,extensions,expected",
    [
        (NOTES["C"][0], [], f"C, D{SHARP}, G"),
        (
            NOTES["C"][0],
            [7],
            f"C, D{SHARP}, G, A{SHARP}",
        ),
        (NOTES["C"][0], [9], f"C, D{SHARP}, G, D"),
        (
            NOTES["C"][0],
            [13],
            f"C, D{SHARP}, G, G{SHARP}",
        ),
        (
            NOTES["C"][0],
            [9, 13],
            f"C, D{SHARP}, G, D, G{SHARP}",
        ),
    ],
)
def test_minor_chord_extensions(root, extensions, expected):
    args = {"root": root, "type": ChordType.MINOR, "extensions": extensions}
    chord = Chord(**args)
    assert str(chord) == expected


@pytest.mark.parametrize(
    "chord,scale,expected",
    [
        (
            Chord(root=NOTES["C"][0], type=ChordType.MAJOR),
            IonianScaleFact.generate_scale(NOTES["C"][0]),
            True,
        ),
        (
            Chord(root=NOTES["D"][0], type=ChordType.MAJOR),
            IonianScaleFact.generate_scale(NOTES["C"][0]),
            False,
        ),
        (
            Chord(root=NOTES["G"][0], type=ChordType.SEVENTH),
            IonianScaleFact.generate_scale(NOTES["C"][0]),
            True,
        ),
        (
            Chord(root=NOTES["A"][0], type=ChordType.SEVENTH),
            MixolydianFlat6Fact.generate_scale(NOTES["A" + SHARP][0]),
            False,
        ),
        (
            Chord(root=NOTES["A"][0], type=ChordType.MAJOR_SEVENTH),
            MixolydianFlat6Fact.generate_scale(NOTES["A" + SHARP][0]),
            False,
        ),
    ],
)
def test_is_diatonic(chord, scale, expected):
    assert chord.is_diatonic(scale) == expected
