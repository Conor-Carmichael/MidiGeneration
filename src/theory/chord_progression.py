from src.theory import *
import midiutil
from loguru import logger

class ChordProgression:
    def __init__(
        self, chords: List[Chord], repeats: int, track: int, channel: int = 0, designation: str = None
    ) -> None:
        self.chords = chords
        self.repeats = repeats
        self.track = track
        self.channel = channel
        self.designation = designation
        self.current = 0


    def __len__(self) -> int:
        return len(self.chords)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.chords):
            nxt = self.chords[self.current]
            self.current += 1
            return nxt
        else:
            self.current = 0
            raise StopIteration

    def __str__(self) -> str:
        if self.__len__() > 0:
            return " → ".join([str(c) for c in self.chords])
        else:
            return "ChordProgression is empty"

    def inc_repeats(self) -> None:
        self.repeats += 1

    def dec_repeats(self) -> None:
        self.repeats -= 1

    def add_chord(self, new_chord: Chord) -> None:
        self.chords.append(new_chord)

    def remove_last_chord(self, chord) -> None:
        if len(self.chords) > 1:
            self.chords = self.chords[:-1]

    def clear(self) -> None:
        self.chords = []

    def is_empty(self) -> bool:
        return self.chords == []
    
    def set_designation(self, desig:str) -> None:
        self.designation = desig

    @classmethod
    def empty(cls):
        return ChordProgression([], 0, 0, 0)


class Song:
    songs = 0

    def __init__(
        self,
        sections: List[ChordProgression],
        home_key: Scale,
        bpm: int,
        num_tracks: int,
        starting_beat: int = 0,
        full_loops: int = 0,
        title:str = None
    ) -> None:
        self.sections = sections
        self.home_key = home_key
        self.bpm = bpm
        self.num_tracks = num_tracks
        self.starting_beat = starting_beat
        self.full_loops = full_loops
        self.title = title

        self.curr_sect = 0


    def __len__(self) -> int:
        return len(self.sections)

    def is_empty(self) -> bool:
        return self.__len__() == 0

    def __str__(self) -> str:
        if self.__len__() > 0 :
            return " \n\n ".join([str(sect) for sect in self.sections]) 
        else:
            return "Song is empty"

    @classmethod
    def empty(cls) -> Any:
        return Song(sections=[], bpm=default_bpm, num_tracks=1, home_key=None)

    def remv_empty(self) -> None:
        self.sections = list(
            filter(
                lambda sect: sect.chords != None and sect.chords != [], self.sections
            )
        )
    

    def set_key(self, scale:Scale) -> None:
        self.home_key = scale

    def set_bpm(self, new_bpm: int) -> None:
        self.bpm = new_bpm

    def set_num_tracks(self, new_num_tracks: int) -> None:
        self.num_tracks = new_num_tracks

    def add_section(self, progression: ChordProgression) -> None:
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
            self.curr_sect = 0
            raise StopIteration


    def write_song_to_midi(self, dest: str, create_bass_track: bool, is_generic:bool, scale:Scale = None):
        logger.info("Generating MIDI results for song.")
        if create_bass_track:
            logger.info("Creating with a separate bass track.")
            self.set_num_tracks(self.num_tracks + 1)

        midi_file_writer = midiutil.MIDIFile(numTracks=self.num_tracks)
        curr_beat = self.starting_beat

        midi_file_writer.addTempo(
            track=0, time=curr_beat, tempo=self.bpm
        )
        if create_bass_track:
            midi_file_writer.addTempo(
                track=1, time=curr_beat, tempo=self.bpm
            )

        # Each loop creates a full song- can set to loop this multiple times
        full_song_write_count = 0
        while full_song_write_count < self.full_loops:

            for sect in self.sections:
                # Can loop indiv sections, so go until no longer needed
                section_write_count = 0
                while section_write_count < sect.repeats:
                    for chord in sect.chords:
                    
                        # Write each note of the chord to midi file at same
                        # point in time
                        for note in chord.get_notes():

                            midi_file_writer.addNote(
                                track=sect.track,
                                channel=0,
                                pitch=note.midi_value,
                                time=curr_beat,
                                duration=note.duration,
                                volume=note.velocity,
                            )
                        # If bass track requested, do so as well
                        if create_bass_track:
                            note = chord.get_notes()[0]
                            midi_file_writer.addNote(
                                track=1,
                                channel=0,
                                pitch=note.midi_value-24,
                                time=curr_beat,
                                duration=note.duration,
                                volume=note.velocity,
                            )

                        # Step to end of the chord being added
                        curr_beat += note.duration

                    section_write_count += 1  # Increment counter to repeat sections

            full_song_write_count += 1


        # Write to the requested destination
        with open("./"+dest, "wb") as file:
            midi_file_writer.writeFile(file)
            Song.songs += 1

