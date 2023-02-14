# Music Generation Tools

With this tool, I aim to provide an interface for creating midi files to use as the starting point for music projects. If you want to loop some chords quickly to jam over, came up with a progression on your guitar, or want to share either to someone else in an easy way, this application can help. 

Quickly enter the chords, progression by progresssion. Set the midi instructions (loudness, duration, etc), then download your midi file. At this point, you can drag and drop it into your editor (tested with Logic and Garageband).

There are more features coming soon, primarily in streamlining the input. 

* Generic chord progressions:
    * Input based on scale degree, chord quality, and alterations. Choose the scale later.
* Restricted input:
    * Restrict the chords you can choose from, to only diatonic chords (chords which all notes exist naturally within a given scale)
* Text input: 
    * Type your input, "c major add 9" then press enter, and type your next chord...

* Command line interface:
    * Download the code, and use text input methods locally via command line




## Details of Implementation

```
src
|
|-generators "To auto generate progressions etc. TODO"
|
|-theory "Implementation of music theory principles"
|
|-ui "Streamlit user interface"
|
|-cli "Drivers for command line interface. TODO"
|
|-tests "All unit and e2e testing"
```


*Implementation details to be written soon*