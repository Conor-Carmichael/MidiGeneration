import pytest
from src.utils.utils import *

@pytest.mark.parametrize(
    "p1,p2,expected", [
        (440, 466.16, 1),
        (440, 659.26, 7),
        (440, 880.00, 12)
    ]
)
def test_calc_semitone_diff_pitches(p1, p2, expected):

    assert calc_semitone_diff_pitches(p1,p2) == expected


@pytest.mark.parametrize(
    "midi,expected", [
        (69, 440),
        (81, 880),
        (103, 3135.96),
    ]
)
def test_get_pitch_from_midi_value(midi, expected):
    assert get_pitch_from_midi_value(midi) == expected