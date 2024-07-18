import streamlit as st
import pandas as pd
import numpy as np
#import json
#import config

from google.cloud import texttospeech
from google.oauth2 import service_account


@st.cache_data
def text_to_speech(text, language):
    # Instantiates a client
    creds = service_account.Credentials.from_service_account_info(st.secrets.google_creds)
    client = texttospeech.TextToSpeechClient(credentials=creds)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content


st.title("Text To Speech App")

text_to_transform = st.text_area(label="Entrez le texte que vous souhaitez convertir en audio", value="")

language = st.radio("Choisissez une langue", ["fr-FR", "en-US"])

transform_button = st.button("Transform")

if transform_button:
    if text_to_transform != '':
        audio = text_to_speech(text_to_transform, language)

        st.audio(audio)