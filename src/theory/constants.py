"""
File for declaration of constants:
* Scale and Chord formulas
* Midi Note ranges

Author: Conor Carmichael
"""


from src.utils.utils import cycle_n_times
from typing import *
from src.theory.datatypes import StepType, ChordType, IonianModes, PentatonicModes

midi_note_vals = {}
midi_start_val = 21
midi_end_val = 108
midi_vel_low = 0
midi_vel_high = 127

octave_range = 8

_WholeToneFomula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
]

_PentatonicFormula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLEHALF,
    StepType.WHOLE,
    StepType.WHOLEHALF,
]

_IonianFormula = [
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.WHOLE,
    StepType.HALF,
]

IonianModesFormulas = {
    mode: cycle_n_times(_IonianFormula, idx) for idx, mode in enumerate(IonianModes)
}

PentatonicModesFormulas = {
    mode: cycle_n_times(_PentatonicFormula, idx)
    for idx, mode in enumerate(PentatonicModes)
}

ScaleFormulas = {**IonianModesFormulas, **PentatonicModesFormulas}


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
}
