import pytest
from src.theory.scales import (
    Scale,
    ScaleFactory,
    IonianScaleFact,
    PentatonicScaleFact,
    WholeToneScaleFact,
    MixolydianFlat6Fact,
)
from src.theory.notes import NOTES, Notes, NoteGeneric
from src.theory import SHARP, FLAT
from src.theory import *


def test_ionian_scale_factory():
    scale = IonianScaleFact.generate_scale(NOTES["C"])
    assert scale.notes == [
        NOTES["C"],
        NOTES["D"],
        NOTES["E"],
        NOTES["F"],
        NOTES["G"],
        NOTES["A"],
        NOTES["B"],
        NOTES["C"],
    ]
    scale = IonianScaleFact.get_mode_definition(IonianModes.DORIAN).generate_scale(
        NOTES["D"]
    )
    assert scale.notes == [
        NOTES["D"],
        NOTES["E"],
        NOTES["F"],
        NOTES["G"],
        NOTES["A"],
        NOTES["B"],
        NOTES["C"],
        NOTES["D"],
    ]

    scale = IonianScaleFact.get_mode_definition(IonianModes.AEOLIAN).generate_scale(
        NOTES["A"]
    )
    assert scale.notes == [
        NOTES["A"],
        NOTES["B"],
        NOTES["C"],
        NOTES["D"],
        NOTES["E"],
        NOTES["F"],
        NOTES["G"],
        NOTES["A"],
    ]


def test_pentatonic_scale_factory():
    scale = PentatonicScaleFact.generate_scale(NOTES["C"])
    assert scale.notes == [
        NOTES["C"],
        NOTES["D"],
        NOTES["E"],
        NOTES["G"],
        NOTES["A"],
        NOTES["C"],
    ]


def test_whole_tone_scale_factory():
    scale = WholeToneScaleFact.generate_scale(NOTES["C"])
    assert scale.notes == [
        NOTES["C"],
        NOTES["D"],
        NOTES["E"],
        NOTES["F" + SHARP],
        NOTES["G" + SHARP],
        NOTES["A" + SHARP],
        NOTES["C"],
    ]


def test_mix_flat_6_scale_factory():
    scale = MixolydianFlat6Fact.generate_scale(NOTES["C"])
    assert scale.notes == [
        NOTES["C"],
        NOTES["D"],
        NOTES["E"],
        NOTES["F"],
        NOTES["G"],
        NOTES["G" + SHARP],
        NOTES["A" + SHARP],
        NOTES["C"],
    ]
