"""
File for declaration of constants:
* Scale and Chord formulas
* Midi Note ranges

Author: Conor Carmichael
"""
from typing import *
from src.theory.datatypes import (
    StepType,
    ChordType,
    IonianModes,
)  
from enum import Enum


midi_note_vals = {}
midi_start_val = 21
midi_end_val = 108
midi_vel_low = 0
midi_vel_high = 127

octave_range = 8

Alteration = Enum("Alteration", ["NATURAL", "SHARP", "FLAT", "DOUBLESHARP", "DOUBLEFLAT"])

# Scale Formula Definitions
WholeToneFomula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
]

MixolydianFlat6Formula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.WHOLE,
]

PentatonicFormula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLEHALF,
    StepType.WHOLE,
    StepType.WHOLEHALF,
]

IonianFormula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
]

# Chord Formula definitions

IonianChordFormulas = [
    ChordType.MAJOR,
    ChordType.MINOR,
    ChordType.MINOR,
    ChordType.MAJOR,
    ChordType.SEVENTH,
    ChordType.DIMINISHED,
]

ChordSymbols = {
    ChordType.MAJOR: ["", "maj"],
    ChordType.MINOR: ["m", "min"],
    ChordType.DIMINISHED: ["°", "dim"],
    ChordType.SEVENTH: ["7", "dom7"],
    ChordType.MAJOR_SEVENTH: ["maj7", "∆7"],
    ChordType.MINOR_SEVENTH: ["min7", "-7"],
}

ChordFormulas = {
    ChordType.MAJOR: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": IonianModes.IONIAN,
    },
    ChordType.MINOR: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": IonianModes.AEOLIAN,
    },
    ChordType.DIMINISHED: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": IonianModes.LOCRIAN,
    },
    ChordType.SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.MIXOLYDIAN,
    },
    ChordType.MAJOR_SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.IONIAN,
    },
    ChordType.MINOR_SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.AEOLIAN,
    },
    ChordType.SUS2: {
        "description": "Suspended 2nd",
        "intervals": [1, 2, 5],
        "scale": IonianModes.IONIAN,
    },
    ChordType.SUS4: {
        "description": "Suspended 4th",
        "intervals": [1, 4, 5],
        "scale": IonianModes.IONIAN,
    },
}
