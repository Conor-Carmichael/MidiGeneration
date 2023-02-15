"""
Description of site.

Author: Conor Carmichael
"""
import sys, os

sys.path.append(os.getcwd())

import streamlit as st
from src.ui.display import display_list


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
st.markdown(display_list(li_items), unsafe_allow_html=True)

li_items = [
    "(Optionally) Restrict chord input options to diatonic chords",
    "Input generic chord sequences (by scale degree, and chord type)",
    "Input chords by text",
    "Maybe play the chords back through the pygame audio driver? Unlikely.",
    "Different time signatures, and utilize time signatures. Currently its \
        restricted to 4/4 but it isn't utilized. The beats should recommend or push towards adding up to a bar."
    "<b>Let me know if you have ideas!</b>"
]   
st.header("Planned Features")
st.markdown(display_list(li_items), unsafe_allow_html=True)
