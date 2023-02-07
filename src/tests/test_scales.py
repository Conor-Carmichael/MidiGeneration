import pytest
from src.theory.scales import Scale
from src.theory import *


def test_scale_constants():
    assert ScaleFormulas[IonianModes.IONIAN] == IonianModesFormulas[IonianModes.IONIAN]
    assert ScaleFormulas[IonianModes.AEOLIAN] == [2, 1, 2, 2, 1, 2, 2]


@pytest.mark.parametrize(
    "root,formula",
    [
        (Note.C, ScaleFormulas.get(IonianModes.IONIAN)),
        (Note.C, ScaleFormulas.get(IonianModes.DORIAN)),
        (Note.C, ScaleFormulas.get(IonianModes.PHRYGIAN)),
        (Note.B, ScaleFormulas.get(IonianModes.LOCRIAN)),
    ],
)
def test_scale_is_cyclical(root, formula):
    scale = Scale(root=root, formula=formula, name="TestScale")
    assert scale.notes[0] == scale.notes[-1], "Scale must start an end with same note"


@pytest.mark.parametrize("root", [Note.C])
def test_major_scale(root):
    scale = Scale(
        root=root, formula=ScaleFormulas.get(IonianModes.IONIAN), name="C Major"
    )
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


@pytest.mark.parametrize("root", [Note.A])
def test_minor_scale(root):
    scale = Scale(
        root=root, formula=ScaleFormulas.get(IonianModes.AEOLIAN), name="A Minor"
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


def test_major_pentatonic():
    scale = Scale(
        root=Note.C, formula=ScaleFormulas.get(PentatonicModes.MAJOR), name="C Maj Pent"
    )
    assert scale.notes == [Note.C, Note.D, Note.E, Note.G, Note.A, Note.C]


def test_minor_pentatonic():
    scale = Scale(
        root=Note.A, formula=ScaleFormulas.get(PentatonicModes.MINOR), name="A Min Pent"
    )
    assert scale.notes == [Note.A, Note.C, Note.D, Note.E, Note.G, Note.A]
