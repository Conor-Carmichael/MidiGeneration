from src.theory.notes import Note, NoteGeneric
from src.theory.constants import ChordType, SHARP
from src.theory.chords import Chord
from src.theory.chord_progression import ChordProgression
from random import choice, choices
        
# Four chord C Major progression
prog_zero = ChordProgression(
    chords=[  
        Chord(
            root=NoteGeneric("C"),
            type=ChordType.MAJOR
        ),    
        Chord(
            root=NoteGeneric("F"),
            type=ChordType.MAJOR_SEVENTH
        ),    
        Chord(
            root=NoteGeneric("A"),
            type=ChordType.MINOR
        ),    
        Chord(
            root=NoteGeneric("F"),
            type=ChordType.MAJOR_SEVENTH
        ),    
        
    ],
    repeats=0,
    track=0
)
prog_one = ChordProgression(
    chords=[
        Chord(
            root=NoteGeneric("A"),
            type=ChordType.MINOR
        ),    
        Chord(
            root=NoteGeneric("C"),
            type=ChordType.MAJOR
        ),    
        Chord(
            root=NoteGeneric("F"),
            type=ChordType.MAJOR_SEVENTH
        ),    
        Chord(
            root=NoteGeneric("G"),
            type=ChordType.SEVENTH
        ),    
    ],
    repeats=0,
    track=0
)

# Amaj7 Dmaj7, E, Bmin6
prog_two = ChordProgression(
    chords=[
        Chord(
            root=NoteGeneric("A"),
            type=ChordType.MAJOR_SEVENTH
        ),    
        Chord(
            root=NoteGeneric("D"),
            type=ChordType.MAJOR_SEVENTH
        ),    
        Chord(
            root=NoteGeneric("E"),
            type=ChordType.MAJOR
        ),    
        Chord(
            root=NoteGeneric("B"),
            type=ChordType.MINOR_SIXTH
        ),    
    ],
    repeats=0,
    track=0
)
# E F#m x4
prog_three = ChordProgression(
    chords=[
        Chord(
            root=NoteGeneric("E"),
            type=ChordType.MAJOR
        ),    
        Chord(
            root=NoteGeneric("F"+SHARP),
            type=ChordType.MINOR
        )
    ],
    repeats=4,
    track=0
)