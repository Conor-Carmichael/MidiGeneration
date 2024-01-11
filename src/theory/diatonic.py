from src.theory.chords import Chord
from src.theory.scales import Scale
from src.theory.constants import ChordFormulas
from typing import Dict


def find_diatonic_chords(scale:Scale) -> Dict:
    diatonic_chords = {
        # Root Note -> [chord formulas]
    }

    for note in scale.notes:

        diatonic_chords[note.name] = []
        for chord_form in ChordFormulas:
            if Chord(root=note, type=chord_form).is_diatonic(scale=scale) :
                diatonic_chords[note.name].append(chord_form)

    return diatonic_chords