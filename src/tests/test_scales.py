import pytest
from src.theory.note_sequence import NotesFactory, NoteSequence
from src.theory.scales import (
    Scale,
    ScaleFactory,
    IonianScaleFact,
    PentatonicScaleFact,
    WholeToneScaleFact,
    MixolydianFlat6Fact,
)
from src.theory.notes import NoteGeneric
from src.theory import SHARP, FLAT
from src.theory import *


NOTES = NotesFactory.get_generic_notes()


@pytest.mark.parametrize(
    "root,alts,exp",
    [
        (
            NOTES["C"][0],
            [{"degree": 7, "fn": "flatten"}],
            f"C, D, E, F, G, A, B{FLAT}, C",
        ),
        (
            NOTES["C"][0],
            [{"degree": 7, "fn": "flatten"}, {"degree": 6, "fn": "flatten"}],
            f"C, D, E, F, G, A{FLAT}, B{FLAT}, C",
        ),
    ],
)
def test_ionian_note_alteration(root, alts, exp):
    scale = IonianScaleFact.generate_scale(root, altered_notes=alts)
    assert str(scale) == exp


@pytest.mark.parametrize(
    "root,alts,exp",
    [
        (
            NOTES["C"][0],
            [{"degree": 0, "fn": "flatten"}],
            f"C, D, E, F, G, A, B{FLAT}, C",
        ),
        (
            NOTES["C"][0],
            [{"degree": 47, "fn": "flatten"}, {"degree": 6, "fn": "flatten"}],
            f"C, D, E, F, G, A{FLAT}, B{FLAT}, C",
        ),
    ],
)
def test_ionian_note_alteration_ioob(root, alts, exp):
    with pytest.raises(Exception):
        scale = IonianScaleFact.generate_scale(root, altered_notes=alts)


def test_ionian_scale_factory():
    scale = IonianScaleFact.generate_scale(NOTES["C"][0])
    assert str(scale) == str(
        NoteSequence(
            notes=[
                NOTES["C"][0],
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["F"][0],
                NOTES["G"][0],
                NOTES["A"][0],
                NOTES["B"][0],
                NOTES["C"][0],
            ]
        )
    )
    scale = IonianScaleFact.get_mode_definition(IonianModes.DORIAN).generate_scale(
        NOTES["D"][0]
    )
    assert str(scale) == str(
        NoteSequence(
            [
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["F"][0],
                NOTES["G"][0],
                NOTES["A"][0],
                NOTES["B"][0],
                NOTES["C"][0],
                NOTES["D"][0],
            ]
        )
    )

    scale = IonianScaleFact.get_mode_definition(IonianModes.AEOLIAN).generate_scale(
        NOTES["A"][0]
    )
    assert str(scale) == str(
        NoteSequence(
            [
                NOTES["A"][0],
                NOTES["B"][0],
                NOTES["C"][0],
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["F"][0],
                NOTES["G"][0],
                NOTES["A"][0],
            ]
        )
    )


def test_pentatonic_scale_factory():
    scale = PentatonicScaleFact.generate_scale(NOTES["C"][0])
    assert str(scale) == str(
        NoteSequence(
            [
                NOTES["C"][0],
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["G"][0],
                NOTES["A"][0],
                NOTES["C"][0],
            ]
        )
    )


def test_whole_tone_scale_factory():
    scale = WholeToneScaleFact.generate_scale(NOTES["C"][0])
    assert str(scale) == str(
        NoteSequence(
            [
                NOTES["C"][0],
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["F" + SHARP][0],
                NOTES["G" + SHARP][0],
                NOTES["A" + SHARP][0],
                NOTES["C"][0],
            ]
        )
    )


def test_mix_flat_6_scale_factory():
    scale = MixolydianFlat6Fact.generate_scale(NOTES["C"][0])
    assert str(scale) == str(
        NoteSequence(
            [
                NOTES["C"][0],
                NOTES["D"][0],
                NOTES["E"][0],
                NOTES["F"][0],
                NOTES["G"][0],
                NOTES["G" + SHARP][0],
                NOTES["A" + SHARP][0],
                NOTES["C"][0],
            ]
        )
    )
