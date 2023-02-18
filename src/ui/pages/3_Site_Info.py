"""
Description of site.

Author: Conor Carmichael
"""
import sys, os

sys.path.append(os.getcwd())

import streamlit as st
from src.ui.display import display_list
from src.theory.constants import SHARP, FLAT


st.title("Information About the Site")
author = "This site is developed by Conor Brooks Carmichael. If you have suggestions, \
    or would like to report an issue, please feel free to reach out to me at my gmail account\
    which is my '[first name][middle initial][last name]@[expected gmail domain]'"
st.markdown(f"<p>{author}</p>", unsafe_allow_html=True)

li_items = [
    "Create a chord progression from the home page.",
    "Create multiple chord progressions for increased complexity.",
    "Configure how the notes will be played in the Set Midi page",
    "Control the looping, loudness (velocity), duration...",
    "When content, scroll down and press 'Generate MIDI'",
    "Then a button to download your file will be created.",
]
st.header("Features")
display_list(li_items)

li_items = [
    "(Optionally) Restrict chord input options to diatonic chords",
    "Input generic chord sequences (by scale degree, and chord type)",
    "Input chords by text",
    "Maybe play the chords back through the pygame audio driver? Unlikely.",
    "Different time signatures, and utilize time signatures. Currently its \
        restricted to 4/4 but it isn't utilized. The beats should recommend or push towards adding up to a bar.",
    "<b>Let me know if you have ideas!</b>",
]
st.header("Planned Features")
display_list(li_items)

st.header("I am aware of some issues as the site stands")
li_items = [
    f"Notation issue: In a scale, say C natural minor, you might get C D <b>D{SHARP}</b> ... Instead of C D <b>E{FLAT}</b>. \
    If you don't know why this is an 'issue' ignore! \
    If this bothers you, it bothers me too. I have implemented the notes in a way where I may be able\
    to fix this soon. But it isn't as important as some other features, so its on the back burner",
    "Sometimes when switching pages Progressions -> Set Midi, the chord adding display doesn't disappear. I believe this is an \
        issue with the streamlit page management system, but I am looking into it."
]
display_list(li_items)
