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

MajorModes = Enum(
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
        "MAJOR6TH",
        "MINOR6TH",
        "DIMINISHED",
        "SEVENTH",
        "MAJOR_SEVENTH",
        "MINOR_SEVENTH",
        "SUS2",
        "SUS4",
    ],
)
