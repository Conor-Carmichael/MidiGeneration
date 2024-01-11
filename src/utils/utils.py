"""
Utility functions.
Author: Conor Carmichael
"""

from typing import *
from numpy import random
from math import pow
import numpy as np
import re
from loguru import logger

from src.theory.constants import RevChordSymbMap, RE_ChordRootNote, RE_Fn_ChordType, RE_slash_value


def calc_semitone_diff_pitches(a: float, b: float) -> int:
    """Returns absolute value, no direction"""
    diff = 12.00 * np.log2(a / b)

    return np.absolute(round(diff))


def calc_semitone_diff_notes(a, b) -> int:
    return calc_semitone_diff_pitches(a.pitch, b.pitch)


def get_pitch_from_midi_value(midi) -> int:
    exp = midi - 69.00
    exp = exp / 12.00
    fact = np.power(2, exp)
    pitch = 440.00 * fact
    return round(pitch, 2)


def cycle_n_times(input: List, n: int) -> List:
    if not input is None:
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





def parse_root_from_str(input_str:str) -> str:
    """Returns parsed root, remainder of string

    Args:
        input_str (str): Input string to parse

    Returns:
        Tuple[str, str]: (RootStr, Remainder)
    """


    # Check for any note + Sharp or Flat
    match = re.match(
        RE_ChordRootNote,
        input_str
    )

    if match:
        match = match.group(0)
        logger.debug(f"input_str matched {match}")

        match = match.replace("#", "♯")
        match = match.replace("b", "♭")

    return match


def parse_chord_type(input_str:str) -> str:

    # Find Chord Symbol in text:
    # Try to find each chord symbol in the input
    i = 1
    chord_symbols = list(RevChordSymbMap.keys())
    while i < len(chord_symbols):
        curr_check = chord_symbols[i]
        # logger.debug(f"Checking {input_str} against RegEx {RE_Fn_ChordType(chord_type_str=curr_check)}")
        match = re.match(
            RE_Fn_ChordType(chord_type_str=curr_check),
            input_str,
            re.IGNORECASE
        )
        if match:
            logger.debug(f"input_str matched with chord symbol {curr_check}")
            break
        else:
            i += 1
            
    else:
        logger.debug(f"No matches on all chord types")
        i = 0 # index 0 should map to major chord empty symbol
              # If nothing matched, call it major

    # Get the type str that matched, theh use that to access the ChordType enum
    chord_type = RevChordSymbMap[
        list(RevChordSymbMap.keys())[i]
    ]
    return chord_type


def parse_chord_root_change(input_str:str) -> str:
    """Identify any slash chords or changed root notes.

    Args:
        input_str (str): string of chord input

    Returns:
        str: root note if found, None if not found
    """

    match = re.match(
        RE_slash_value,
        input_str
    )

    if match:
        match = match.group(0)
        return match.split("/")[1]
    else:
        return None

