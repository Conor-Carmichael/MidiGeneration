from src.theory.notes import Note, NoteGeneric
from src.theory.constants import ChordType
from src.theory.chords import Chord
from src.theory.chord_progression import ChordProgression, Song

from src.tests.artifacts.chord_progressions import prog_zero, prog_one, prog_two, prog_three
from src.tests.artifacts.scales import c_major


from random import choice, choices


song_one = Song(
    sections=[
        prog_zero,
        prog_one,
        prog_zero,
        prog_one
    ],
    home_key=c_major,
    bpm=120,
    num_tracks=1,
    starting_beat=0,
    full_loops=0
)