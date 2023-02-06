from enum import Enum, IntEnum
from src.utils.utils import cycle_n_times


class StepType(IntEnum):
    HALF = 1
    WHOLE = 2
    WHOLEHALF = 3


# Notes = Graph


# Graph implementation of notes
# vertices = ['Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb', 'C',  'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#']
# n_vertices = len(vertices)
# edges = [
#
# ]


Notes = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#,Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]
Note = Enum("Note", Notes)

IonianModes = Enum(
    "Modes",
    ["IONIAN", "DORIAN", "PHRYGIAN", "LYDIAN", "MIXOLYDIAN", "AEOLIAN", "LOCRIAN"],
)
PentatonicModes = Enum("PentatonicModes", ["MAJOR", "SECOND", "THIRD", "FOURTH", "MINOR"])

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
    StepType.WHOLEHALF

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
    mode: cycle_n_times(_PentatonicFormula, idx) for idx, mode in enumerate(PentatonicModes)
}

ScaleFormulas = {
    **IonianModesFormulas,
    **PentatonicModesFormulas
}


ChordTypes = Enum(
    "ChordTypes",
    ["MAJOR", "MINOR", "DIMINISHED", "SEVENTH", "MAJOR_SEVENTH", "MINOR_SEVENTH"],
)


ChordSymbols = {
    "MAJOR": ["", "maj"],
    "MINOR": ["m", "min"],
    "DIMINISHED": ["°", "dim"],
    "SEVENTH": ["7", "dom7"],
    "MAJOR_SEVENTH": ["maj7", "∆7"],
    "MINOR_SEVENTH": ["min7", "-7"],
}

ChordFormulas = {
    "MAJOR": {"description": "", "intervals": [1, 3, 5], "scale": IonianModes.IONIAN},
    "MINOR": {"description": "", "intervals": [1, 3, 5], "scale": IonianModes.AEOLIAN},
    "DIMINISHED": {
        "description": "",
        "intervals": [1, 3, 5],
        "scale": IonianModes.LOCRIAN,
    },
    "SEVENTH": {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.MIXOLYDIAN,
    },
    "MAJOR_SEVENTH": {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.IONIAN,
    },
    "MINOR_SEVENTH": {
        "description": "",
        "intervals": [1, 3, 5, 7],
        "scale": IonianModes.AEOLIAN,
    },
}
