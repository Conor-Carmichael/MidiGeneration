from src.theory import *


class ChordProgression:

    def __init__(self, chords:List[Chord], repeats:int, track:int, channel:int=0) -> None:
        self.chords = chords
        self.repeats = repeats
        self.track = track
        self.channel = channel

        self.current = 0

    def __iter__(self) :
        return self

    def __next__(self):
        if self.current < len(self.chords):
            nxt = self.chords[self.current]
            self.current += 1
            return nxt
        else:
            raise StopIteration


class Song:

    def __init__(
        self,
        sections:List[ChordProgression],
        bpm:int,
        num_tracks:int,
        starting_beat:int = 0
    ) -> None:
        self.sections = sections
        self.bpm = bpm
        self.num_tracks = num_tracks
        self.starting_beat = starting_beat

        self.curr_sect = 0

    def set_bpm(self,new_bpm:int) -> None:
        self.bpm = new_bpm
    
    def set_num_tracks(self, new_num_tracks:int) -> None:
        self.num_tracks = new_num_tracks
        
    def add_section(self, progression:ChordProgression) -> None:
        """Adds a new chord progression to the song

        Args:
            progression (List[Chord]): Adds a new progession to the list.
        """
        # Could add some validation
        self.sections.append(progression)

    def __iter__(self):
        return self

    def __next__(self):

        if self.curr_sect < len(self.sections):
            nxt = self.sections[self.curr_sect]
            self.curr_sect += 1
            return nxt
        else:
            raise StopIteration

    def write_song_to_midi(self, dest:str) -> bool:
        success = False
        try:
            logger.info("Creating MIDI tracks for song.")
            midifle = midi.MIDIFile(numTracks=self.num_tracks)
            curr_beat = self.starting_beat
            notes_count = 0

            for sect in self:
                midifle.addTempo(track=sect.track, time=curr_beat, tempo=self.bpm)
                for chord in sect:
                    for note in chord.get_notes():
                        midifle.addNote(
                            track=sect.track,
                            channel=0,
                            pitch=note.midi_value,
                            time=curr_beat,
                            duration=note.duration,
                            volume=note.velocity
                        )
                        notes_count+=1

                    curr_beat += note.duration
            logging.info(f"Added {notes_count} notes to project.")

            success = True

        except Exception as e:
            logger.error("Error writing ChordProgression to midi file.")
            logger.error(e)

        finally:
            return success