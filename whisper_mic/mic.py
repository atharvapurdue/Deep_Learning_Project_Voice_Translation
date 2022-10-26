import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import click
import pygame
from io import BytesIO
from gtts import gTTS


temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")


@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large"]))
@click.option("--english", default=False, help="Whether to use English model",is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic engergy", type=bool)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
def main(model, english,verbose, energy, pause,dynamic_energy):
    # there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)

    # load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        pygame.init()
        pygame.mixer.init()
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        while True:
            mp3_player = BytesIO()
            # get and save audio to wav file
            audio = r.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")

            if english:
                result = audio_model.transcribe(save_path, language='english')
            else:
                result = audio_model.transcribe(save_path, **translate_options)

            if not verbose:
                predicted_text = result["text"]
                print("You said: " + predicted_text)
                tts = gTTS(result["text"], lang='en')
                tts.write_to_fp(mp3_player)
                pygame.mixer.music.load(mp3_player, 'mp3')
                pygame.mixer.music.play()
            else:
                print(result)
                
main()