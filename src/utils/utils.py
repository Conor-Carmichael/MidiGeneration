from typing import *


def cycle_n_times(input: List, n) -> List:
    while n > 0:
        first = input[0]
        input = input[1:]
        input.append(first)
        n -= 1
    return input
