from collections import OrderedDict


# Taken/adapted from stack overflow post:
# https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
def get_roman_numeral(num):

    roman = OrderedDict()
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])


def get_note_duration() -> int:

    duration = 0.0



    return duration