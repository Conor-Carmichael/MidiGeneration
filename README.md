# Music Generation Tools


The goal of the project is to be able to quickly generate midi files to use in logic, or however. The midi files should be able to generate chord progressions, bass lines, etc. from simple inputs. Take in BPM, chords or roman numerals and a key, consider slash chords and inversions, allow for arpegiattion, note duration, secondary fifths... so on and so forth. 

The inputs are to be determined, but plans are for a streamlit user interface, and a command line interface. For CLI, something like:

`$python generate_chord_progression.py C MAJOR 85 I:w IV:w V:h vi:h iv:h 3x`

*Would indicate* In the key of C major, at 85 beats per minute, generate a chord progression that plays; C major whole notes, F major whole notes, G major half notes, Am half notes, Fm half notes. Played three times.

`$python generate_chord_progression.py {root note} {scale} {bpm} {chord:duration:velocity for chord in progression} {repetitions}`


