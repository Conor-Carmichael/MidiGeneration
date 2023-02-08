from src.theory import *
import numpy as np 


class Note:

    """
    To allow for more significant alterations, the Note class.
    """

    def __init__(
        self,
        base_note_name:str,
        alter:Alteration,
        pitch:float,
        next_note,
        prev_note  
    ) -> None:

        self.base_note_name = base_note_name
        self.alter = alter #if alter else ""
        self.pitch = pitch
        self.next_note = next_note
        self.prev_note = prev_note

    def sharpen(self, alter_note:bool = True):
        """Does not change base note name"""
        self.pitch = self.pitch * np.power(2, 1/12)
        if alter_note:
            self.base_note_name = self.next_note.base_note_name


    def flatten(self, alter_note:bool = True):
        """Does not change base note name"""
        self.pitch = self.pitch * np.power(2, -1*(1/12))
        if alter_note:
            self.base_note_name = self.prev_note.base_note_name





# class Notes:
#     """ Graph Structure to encode distance between notes """

#     def __init__(self) -> None:
#         pass


#     def __getitem__(self, item):
#         ...

