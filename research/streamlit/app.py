import logging
import logging.handlers
import queue
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List

import av
import numpy as np
import pydub
import streamlit as st
import whisper

from streamlit_webrtc import WebRtcMode, webrtc_streamer

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)

def main():
    st.header("Real Time Speech-to-Text")
    st.markdown("This demo app is using [Whisper](https://github.com/openai/whisper), \
                an open speech-to-text engine.")

    sound_only_page = "Sound only (sendonly)"
    with_video_page = "With video (sendrecv)"

    src_lang_en = "English"

    dest_lang_hindi = "Hindi"
    dest_lang_chinese = "Chinese"

    app_mode = st.selectbox("Choose the app mode", [sound_only_page, with_video_page])
    src_lang = st.selectbox("Select source language", [src_lang_en])
    dest_lang = st.selectbox("Select destination language", [dest_lang_hindi, dest_lang_chinese])

    model = whisper.load_model("base")

    if app_mode == sound_only_page:
        speech_to_translation(model, src_lang, dest_lang)
    
def speech_to_translation(model, src_lang, dest_lang):
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Loading...")
    text_output = st.empty()
    stream = None

    while True:
        if webrtc_ctx.audio_receiver:
            if stream is None:

                # get a chunk of audio from the microphone
                sound_chunk = pydub.AudioSegment.empty()

                try:
                    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
                except queue.Empty:
                    time.sleep(0.1)
                    status_indicator.write("No frame arrived.")
                    continue
                
                status_indicator.write("Running. Say something!")

                for audio_frame in audio_frames:
                    sound = pydub.AudioSegment(
                        data=audio_frame.to_ndarray().tobytes(),
                        sample_width=audio_frame.format.bytes,
                        frame_rate=audio_frame.sample_rate,
                        channels=len(audio_frame.layout.channels),
                    )
                sound_chunk += sound

                if len(sound_chunk) > 0:
                    buffer = np.array(sound_chunk.get_array_of_samples())
                    options = dict(beam_size=5, best_of=5, language=dest_lang)
                    translate_options = dict(task="translate", **options)
                    stream.feedAudioContent(buffer)
                    text = model.transcribe(stream, **translate_options)

                    # we now need to translate to the target language
                    # also, check if whisper requires mp3 files or what is needed
                    # TODO: look at atharva's translation notebook to see how to do it
                    text_output.markdown(f"**Text:** {text['text']}")
            
            else:
                status_indicator.write("AudioReciver is not set. Abort.")
                break

if __name__ == "__main__":
    import os

    DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
        "%(message)s",
        force=True,
    )

    logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

    st_webrtc_logger = logging.getLogger("streamlit_webrtc")
    st_webrtc_logger.setLevel(logging.DEBUG)

    fsevents_logger = logging.getLogger("fsevents")
    fsevents_logger.setLevel(logging.WARNING)

    # we need to install whisper here
    os.system('pip install git+https://github.com/openai/whisper.git')

    main()