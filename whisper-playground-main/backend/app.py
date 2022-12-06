import os
import tempfile
import ffmpeg
import flask
from flask import request
from flask_cors import CORS
import whisper
import pygame
from io import BytesIO
from gtts import gTTS
import torch
import numpy as np
import subprocess
from pydub.utils import mediainfo


app = flask.Flask(__name__)
CORS(app)


@app.route('/transcribe', methods=['POST'])
def transcribe():
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
def transcribe2():
    # Only works when language selected is "english"
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

        pygame.init()
        pygame.mixer.init()
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        mp3_player = BytesIO()

        result = audio_model.transcribe(save_path, **translate_options)

        predicted_text = result["text"]

        # Only send to gTTS if the string has alphabets, otherwise backend will crash
        if predicted_text and re.sub(r'[^a-zA-Z]', '', predicted_text):
            tts = gTTS(result["text"], lang='en')
            tts.write_to_fp(mp3_player)
            pygame.mixer.music.load(mp3_player, 'mp3')
            pygame.mixer.music.play()
            print("You said: " + predicted_text)

        return(predicted_text)


@app.route('/videosub', methods=['POST'])
def subtitle_the_video():
    if request.method == 'POST':
         language = "hindi"
         input_video = request.files['myFile']
         model = "small"
         input_video.save(input_video.filename)
    if model != 'large' and language == 'english':
            model = model + '.en'
    audio_model = whisper.load_model(model)
    def video2mp3(video_file, output_ext="mp3"):
        filename, ext = os.path.splitext(video_file)
        subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
        return f"{filename}.{output_ext}"
    
    audio_file = video2mp3(input_video.filename)
    def translate(audio):
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        result = audio_model.transcribe(audio_file,**translate_options)
        return result
    
    result = translate(audio_file)
    print(result["text"])
    audio_path = audio_file.split(".")[0]
    with open(os.path.join(audio_path + ".vtt"), "w") as vtt:
        whisper.utils.write_vtt(result["segments"], file=vtt)
    subtitle = audio_path + ".vtt"
    output_video = audio_path + "_subtitled.mp4"
    video = ffmpeg.input(input_video.filename)
    audio = video.audio
    ffmpeg.concat(video.filter("subtitles", subtitle), audio, v=1, a=1).output(output_video).run(overwrite_output=True)
    return flask.send_file(output_video,mimetype='video/mp4',as_attachment=True)
