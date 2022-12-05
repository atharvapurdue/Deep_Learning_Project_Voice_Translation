import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper
import subprocess
from pydub.utils import mediainfo
from whisper.utils import write_vtt
app = flask.Flask(__name__)
CORS(app)

@app.route('/video', methods=['POST'])
def subtitle_the_video():
    if request.method == 'POST':
        language = request.form['language']
        input_video = request.form['video']
        model = request.form['model_size']
    if model != 'large' and language == 'english':
            model = model + '.en'
    audio_model = whisper.load_model(model)
    #print(audio_model.device)
    def video2mp3(video_file, output_ext="mp3"):
        filename, ext = os.path.splitext(video_file)
        subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
        return f"{filename}.{output_ext}"
    
    audio_file = video2mp3(input_video)
    
    audio_file_info = mediainfo(audio_file)
    print(audio_file_info)
    def translate(audio):
    
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        result = model.transcribe(audio_file,**translate_options)
        return result
    result = translate(audio_file)
    print(result["text"])
    audio_path = audio_file.split(".")[0]
    with open(os.path.join(audio_path + ".vtt"), "w") as vtt:
        write_vtt(result["segments"], file=vtt)
    subtitle = audio_path + ".vtt"
    output_video = audio_path + "_subtitled.mp4"
    return subtitle