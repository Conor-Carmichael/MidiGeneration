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
    MajorModes,
)
from enum import Enum


midi_note_vals = {}
midi_start_val = 0
midi_end_val = 127

midi_piano_start = 21
midi_piano_end = 108

midi_vel_low = 0
midi_vel_high = 127

# note_lengths = ["1/16", '1/8','1/4','1/2', '1']
note_lengths = [16, 12, 8, 4, 2, 1, 0.5, 0.25]

default_bpm = 120
bpm_range = (60, 200)
beats_per_measure_range = (2, 8)
note_duration_per_beat_range = (2, 8)
octave_range = 8
inversion_values = [i for i in range(5)]
extension_values = [9, 11, 13, 15]

note_alterations = [
    # This should be changed to dynamic soon
    {"degree": 5, "fn": "flatten"},
    {"degree": 5, "fn": "sharpen"},
    {"degree": 9, "fn": "sharpen"},
    {"degree": 9, "fn": "flatten"},
    {"degree": 9, "fn": "flatten"},
    {"degree": 11, "fn": "sharpen"},
    {"degree": 11, "fn": "flatten"},
]

SHARP = "♯"
FLAT = "♭"
NATURAL = "♮"

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

# NOT TESTED
BluesFormula = [
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.HALF,
    StepType.HALF,
    StepType.HALF,
    StepType.WHOLE,
    StepType.WHOLE,
]

# NOT TESTED
HarmonicMinorFormula = [
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLEHALF,
    StepType.HALF,
]

# NOT TESTED
MelodicMinorFormula = [
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
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
    # First is for triad, second is for extended
    ChordType.MAJOR: ["", "maj"],
    ChordType.MINOR: ["m", "min"],
    ChordType.MAJOR6TH: ["6", "maj6"],
    ChordType.MINOR6TH: ["m6", "min6"],
    ChordType.DIMINISHED: ["°", "dim"],
    ChordType.SEVENTH: ["7", ""],
    ChordType.MAJOR_SEVENTH: ["maj7", "∆7"],
    ChordType.MINOR_SEVENTH: ["min7", "-7"],
    ChordType.SUS2: ["Sus2", "Sus2"],
    ChordType.SUS4: ["Sus4", "Sus4"],
}

ChordFormulas = {
    ChordType.MAJOR: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": MajorModes.IONIAN,
    },
    ChordType.MINOR: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": MajorModes.AEOLIAN,
    },
    ChordType.MAJOR6TH: {
        "description": "",
        "intervals": [1, 3, 5, 6],
        "scale": MajorModes.IONIAN,
    },
    ChordType.MINOR6TH: {
        "description": "",
        "intervals": [1, 3, 5, 6],
        "scale": MajorModes.AEOLIAN,
    },
    ChordType.DIMINISHED: {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": MajorModes.LOCRIAN,
    },
    ChordType.SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": MajorModes.MIXOLYDIAN,
    },
    ChordType.MAJOR_SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": MajorModes.IONIAN,
    },
    ChordType.MINOR_SEVENTH: {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": MajorModes.AEOLIAN,
    },
    ChordType.SUS2: {
        "description": "Suspended 2nd",
        "intervals": [1, 2, 5],
        "scale": MajorModes.IONIAN,
    },
    ChordType.SUS4: {
        "description": "Suspended 4th",
        "intervals": [1, 4, 5],
        "scale": MajorModes.IONIAN,
    },
}
