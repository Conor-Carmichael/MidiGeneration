import src.settings as S

from src.theory.constants import *
from src.theory.datatypes import *
from src.theory.notes import Note, NoteGeneric
from src.theory.note_sequence import NoteSequence, NotesFactory
from src.theory.scales import Scale, ScaleFactory, AllScaleFactories
from src.theory.chords import Chord, ChordGeneric
from src.theory.chord_progression import Song, ChordProgression
from src.theory.visualizer import Visualizer

from typing import *
from sys import stdout
import midiutil as midi

from loguru import logger


logger.add(stdout, level=S.log_level.upper())
