from src.theory.scales import Scale, ScaleFactory
from src.theory.notes import Note, NoteGeneric
from src.theory.constants import IonianFormula


c_major = ScaleFactory("TestCase-CMaj", IonianFormula).generate_scale(
    root_note=NoteGeneric("C"),
)