# Music Theory Base - Implementation Details


## Notes

`notes.py`

### NoteGeneric

Class to represent a single note, which holds no pitch/octave information, nor midi information.

Has the fields:
* `name` - foundation for equality checks
    * If the name of the note is 'Ab' (A flat), the name will be 'Ab' but the flat will be used to set the `alter` field, to denote that this is note holds an alteration.
* `next_note` used to form sequences
* `prev_note` used to form sequences


### Note

Expands the NoteGeneric class to include midi information- `midi_value`, `duration`, `velocity`, `start_time`, `pitch`

* `midi_value` is used for equality checks


## NoteSequence


## Chords



## Scales