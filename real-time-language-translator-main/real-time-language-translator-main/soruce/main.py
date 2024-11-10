import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize translator and mixer
translator = Translator()
pygame.mixer.init()

# Create a mapping between language names and codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load a sound
    audio.play()
    os.remove("cache_file.mp3")

def main_process(output_placeholder, from_language, to_language):
    global isTranslateOn

    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.markdown("<p class='status'>🎙️ Listening...</p>", unsafe_allow_html=True)
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            output_placeholder.markdown("<p class='status'>🔄 Processing...</p>", unsafe_allow_html=True)
            spoken_text = rec.recognize_google(audio, language=from_language)
            output_placeholder.markdown(f"<p class='success'>✅ You said: {spoken_text}</p>", unsafe_allow_html=True)

            output_placeholder.markdown("<p class='status'>🌐 Translating...</p>", unsafe_allow_html=True)
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text.text, to_language)
            output_placeholder.markdown(f"<p class='result'>🎉 Translated: {translated_text.text}</p>", unsafe_allow_html=True)
    
        except Exception as e:
            output_placeholder.markdown(f"<p class='error'>⚠️ Error: {str(e)}</p>", unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(page_title="Translingo - Language Translator", page_icon="🌐", layout="centered")

# CSS for a beautiful gradient background
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #a3a8fc, #f9c4d2); /* Soft purple to light pink gradient */
        color: #333333;
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #2C3E50;
        margin-top: 20px;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 20px;
    }
    .status {
        font-size: 18px;
        color: #3498DB; /* Blue for ongoing status */
    }
    .success {
        font-size: 18px;
        color: #2ECC71; /* Green for success */
    }
    .error {
        font-size: 18px;
        color: #E74C3C; /* Red for errors */
    }
    .result {
        font-size: 20px;
        font-weight: bold;
        color: #2980B9; /* Deep blue for results */
    }
    .dropdown-label {
        font-size: 18px;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #2C3E50; /* Dark button */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #34495E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="main-title">🌐 Translingo: Real-Time Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Speak, Translate, and Hear in Any Language!</div>', unsafe_allow_html=True)

# Dropdowns for language selection
st.markdown('<div class="dropdown-label">🎤 Select Source Language:</div>', unsafe_allow_html=True)
from_language_name = st.selectbox("", list(LANGUAGES.values()))

st.markdown('<div class="dropdown-label">🎧 Select Target Language:</div>', unsafe_allow_html=True)
to_language_name = st.selectbox(" ", list(LANGUAGES.values()))

# Convert language names to codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Buttons to control the process
col1, col2 = st.columns(2)
with col1:
    start_button = st.button("🌐 Start Translation")
with col2:
    stop_button = st.button("🛑 Stop Translation")

# Placeholder for dynamic messages
output_placeholder = st.empty()

# Translation process
if start_button:
    isTranslateOn = True
    main_process(output_placeholder, from_language, to_language)

if stop_button:
    isTranslateOn = False
    output_placeholder.info("🛑 Translation Stopped.")
