import pytest
from src.theory.chords import Chord
from src.theory.scales import *
from src.theory import *


@pytest.mark.parametrize(
    "root,expected",
    [
        (NOTES["C"], [NOTES["C"], NOTES["E"], NOTES["G"]]),
        (NOTES["D"], [NOTES["D"], NOTES["F" + SHARP], NOTES["A"]]),
        (NOTES["B"], [NOTES["B"], NOTES["D" + SHARP], NOTES["F" + SHARP]]),
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
        (NOTES["C"], [NOTES["C"], NOTES["D" + SHARP], NOTES["G"]]),
        (NOTES["D"], [NOTES["D"], NOTES["F"], NOTES["A"]]),
        (NOTES["B"], [NOTES["B"], NOTES["D"], NOTES["F" + SHARP]]),
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
        (NOTES["B"], [NOTES["B"], NOTES["D"], NOTES["F"]]),
        (NOTES["C"], [NOTES["C"], NOTES["D" + SHARP], NOTES["F" + SHARP]]),
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
        (NOTES["C"], [], [NOTES["C"], NOTES["E"], NOTES["G"]]),
        (NOTES["D"], None, [NOTES["D"], NOTES["F" + SHARP], NOTES["A"]]),
        (NOTES["C"], [9], [NOTES["C"], NOTES["E"], NOTES["G"], NOTES["D"]]),
        (NOTES["C"], [6], [NOTES["C"], NOTES["E"], NOTES["G"], NOTES["A"]]),
        (
            NOTES["C"],
            [9, 11, 13],
            [NOTES["C"], NOTES["E"], NOTES["G"], NOTES["D"], NOTES["F"], NOTES["A"]],
        ),
    ],
)
def test_major_chord_extensions(root, extensions, expected):
    args = {"root": root, "type": ChordType.MAJOR, "extensions": extensions}
    chord = Chord(**args)
    assert chord.get_notes() == expected


@pytest.mark.parametrize(
    "root,extensions,expected",
    [
        (NOTES["C"], [], [NOTES["C"], NOTES["D" + SHARP], NOTES["G"]]),
        (
            NOTES["C"],
            [7],
            [NOTES["C"], NOTES["D" + SHARP], NOTES["G"], NOTES["A" + SHARP]],
        ),
        (NOTES["C"], [9], [NOTES["C"], NOTES["D" + SHARP], NOTES["G"], NOTES["D"]]),
        (
            NOTES["C"],
            [13],
            [NOTES["C"], NOTES["D" + SHARP], NOTES["G"], NOTES["G" + SHARP]],
        ),
        (
            NOTES["C"],
            [9, 13],
            [
                NOTES["C"],
                NOTES["D" + SHARP],
                NOTES["G"],
                NOTES["D"],
                NOTES["G" + SHARP],
            ],
        ),
    ],
)
def test_minor_chord_extensions(root, extensions, expected):
    args = {"root": root, "type": ChordType.MINOR, "extensions": extensions}
    chord = Chord(**args)
    assert chord.get_notes() == expected


@pytest.mark.parametrize(
    "chord,scale,expected",
    [
        (
            Chord(root=NOTES["C"], type=ChordType.MAJOR),
            IonianScaleFact.generate_scale(NOTES["C"]),
            True,
        ),
        (
            Chord(root=NOTES["D"], type=ChordType.MAJOR),
            IonianScaleFact.generate_scale(NOTES["C"]),
            False,
        ),
        (
            Chord(root=NOTES["G"], type=ChordType.SEVENTH),
            IonianScaleFact.generate_scale(NOTES["C"]),
            True,
        ),
        (
            Chord(root=NOTES["A"], type=ChordType.SEVENTH),
            MixolydianFlat6Fact.generate_scale(NOTES["A" + SHARP]),
            False,
        ),
        (
            Chord(root=NOTES["A"], type=ChordType.MAJOR_SEVENTH),
            MixolydianFlat6Fact.generate_scale(NOTES["A" + SHARP]),
            False,
        ),
    ],
)
def test_is_diatonic(chord, scale, expected):
    assert chord.is_diatonic(scale) == expected
