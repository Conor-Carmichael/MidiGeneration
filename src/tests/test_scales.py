import pytest
from src.theory.scales import (
    Scale,
    ScaleFactory,
    IonianScaleFact,
    PentatonicScaleFact,
    WholeToneScaleFact,
    MixolydianFlat6Fact,
)
from src.theory import *


def test_ionian_scale_factory():
    scale = IonianScaleFact.generate_scale(Note.C)
    assert scale.notes == [
        Note.C,
        Note.D,
        Note.E,
        Note.F,
        Note.G,
        Note.A,
        Note.B,
        Note.C,
    ]
    scale = IonianScaleFact.get_mode_definition(IonianModes.DORIAN).generate_scale(
        Note.D
    )
    assert scale.notes == [
        Note.D,
        Note.E,
        Note.F,
        Note.G,
        Note.A,
        Note.B,
        Note.C,
        Note.D,
    ]

    scale = IonianScaleFact.get_mode_definition(IonianModes.AEOLIAN).generate_scale(
        Note.A
    )
    assert scale.notes == [
        Note.A,
        Note.B,
        Note.C,
        Note.D,
        Note.E,
        Note.F,
        Note.G,
        Note.A,
    ]


def test_pentatonic_scale_factory():
    scale = PentatonicScaleFact.generate_scale(Note.C)
    assert scale.notes == [Note.C, Note.D, Note.E, Note.G, Note.A, Note.C]


def test_whole_tone_scale_factory():
    scale = WholeToneScaleFact.generate_scale(Note.C)
    assert scale.notes == [
        Note.C,
        Note.D,
        Note.E,
        Note.Fsharp,
        Note.Gsharp,
        Note.Asharp,
        Note.C,
    ]


def test_mix_flat_6_scale_factory():
    scale = MixolydianFlat6Fact.generate_scale(Note.C)
    assert scale.notes == [
        Note.C,
        Note.D,
        Note.E,
        Note.F,
        Note.G,
        Note.Gsharp,
        Note.Asharp,
        Note.C,
    ]
