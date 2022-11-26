import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper
import pygame
from io import BytesIO
from gtts import gTTS
import torch
import numpy as np


app = flask.Flask(__name__)
CORS(app)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    print("HEYO!")
    if request.method == 'POST':
        language = request.form['language']
        model = request.form['model_size']

        # there are no english models for large
        if model != 'large' and language == 'english':
            model = model + '.en'
        audio_model = whisper.load_model(model)

        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'temp.wav')

        wav_file = request.files['audio_data']
        wav_file.save(save_path)

        if language == 'english':
            result = audio_model.transcribe(save_path, language='english')
        else:
            result = audio_model.transcribe(save_path)

        return result['text']
    else:
        return "This endpoint only processes POST wav blob"

@app.route('/transcribe2', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        language = request.form['language']
        model = request.form['model_size']

        # there are no english models for large
        if model != 'large' and language == 'english':
            model = model + '.en'
        audio_model = whisper.load_model(model)

        print("Say something!")
        pygame.init()
        pygame.mixer.init()
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        mp3_player = BytesIO()
        # get audio
        audio = request.files['audio_data']
        torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)

        result = audio_model.transcribe(torch_audio, **translate_options)

        predicted_text = result["text"]
        tts = gTTS(result["text"], lang='en')
        tts.write_to_fp(mp3_player)
        pygame.mixer.music.load(mp3_player, 'mp3')
        pygame.mixer.music.play()
        print("You said: " + predicted_text)
        return(predicted_text)




