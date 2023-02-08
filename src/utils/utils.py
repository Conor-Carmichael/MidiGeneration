from typing import *
from numpy import random
from math import pow
import numpy as np
from src.theory.notes import Note


def calc_semitone_diff_pitches(a:float, b:float) -> int:
    """Returns absolute value, no direction"""
    diff = 12.00 * np.log2(a / b)
   
    return np.absolute(round(diff))


def calc_semitone_diff_notes(a:Note, b:Note) -> int:
    return calc_semitone_diff_pitches(a.pitch, b.pitch)


def get_pitch_from_midi_value(midi) -> int:
    exp = midi - 69.00
    exp = exp / 12.00
    fact = np.power(2, exp)
    pitch = 440.00 * fact
    return round(pitch, 2)


def cycle_n_times(input: List, n: int) -> List:
    while n > 0:
        first = input[0]
        input = input[1:]
        input.append(first)
        n -= 1
    return input


def parse_roman_numeral_to_chord_type(input: str):
    quality = ""
    # Need regex
    # I/i II/ii, III/iii IV/iv
    rom_num = input[:3]
    # Check for major or minor notation
    if rom_num.isupper():
        quality = "MAJOR"
    elif rom_num.islower():
        quality = "MINOR"
    else:
        raise ValueError(f"Mixed case in roman numeral: {rom_num}")

    # Check for chord alterations:

    return None


def get_rand_velocities(mean: int, var: float, min: int, max: int):
    v = random.normal(mean, var)
    v = round(v, 0)
    v = 0 if v < min else v
    v = 127 if v > max else v
    return v
