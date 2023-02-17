import src.settings as S

from src.theory.constants import *
from src.theory.datatypes import *
from src.theory.notes import Note, NoteGeneric
from src.theory.note_sequence import NoteSequence, NotesFactory
from src.theory.scales import Scale, ScaleFactory, AllScaleFactories
from src.theory.chords import Chord, ChordGeneric
from src.theory.chord_progression import Song, ChordProgression

from typing import *
from sys import stdout
import midiutil as midi

import logging

logger = logging.getLogger(__name__)
output_hndlr = logging.StreamHandler(stdout)
logger.addHandler(output_hndlr)
# handler = logging.StreamHandler()

level = logging.getLevelName(S.log_level)
logger.setLevel(level)
