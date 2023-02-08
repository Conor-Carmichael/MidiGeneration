from typing import *


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
