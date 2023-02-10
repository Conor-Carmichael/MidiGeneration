"""
File for declaration of datatypes

Author: Conor Carmichael
"""

from typing import *
from enum import Enum, IntEnum
from dataclasses import dataclass


@dataclass
class MidiNote:
    value: int
    velocity: int
    timing: int
    duration: int


# TODO fix circular import error to avoid magic number 8
Octave = Enum("Octave", [str(i + 1) for i in range(8)])

# TODO: Implement notes as a graph
# Graph implementation of notes
# vertices = ['Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb', 'C',  'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#']
# n_vertices = len(vertices)
# edges = [
#
# ]


# Make 2d array


# Notes = [
#     "A",
#     "Asharp",
#     "B",
#     "C",
#     "Csharp",
#     "D",
#     "Dsharp",
#     "E",
#     "F",
#     "Fsharp",
#     "G",
#     "Gsharp",
# ]


# Note = Enum("Note", Notes)

IonianModes = Enum(
    "Modes",
    ["IONIAN", "DORIAN", "PHRYGIAN", "LYDIAN", "MIXOLYDIAN", "AEOLIAN", "LOCRIAN"],
)

PentatonicModes = Enum(
    "PentatonicModes", ["MAJOR", "SECOND", "THIRD", "FOURTH", "MINOR"]
)


class StepType(IntEnum):
    HALF = 1
    WHOLE = 2
    WHOLEHALF = 3


class StepSequence:
    def __init__(self, seq: List[StepType]) -> None:
        self.sequence = seq


ChordType = Enum(
    "ChordTypes",
    [
        "MAJOR",
        "MINOR",
        "DIMINISHED",
        "SEVENTH",
        "MAJOR_SEVENTH",
        "MINOR_SEVENTH",
        "SUS2",
        "SUS4",
    ],
)
