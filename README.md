# Deep Learning Project: Voice Translation

This project aims to utilize existing speech translation models to create a application that can do translation, ideally in real time. The following models and platforms are currently being investigated by the group as we work through the semester.

# OpenAI Whisper

One of the models we are investigating is OpenAI's [Whisper](https://openai.com/blog/whisper/). In brief, Whisper is an automatic speech recognition system developed by OpenAI that has been trained on 680k hours of multilingual speech. It uses an encoder-decoder Transformer, with samples chunked into 30-second segments.

# ESPNet

Another model we are investigating is [ESPNet](https://github.com/espnet/espnet), a speech processing toolkit. 

# PaddleSpeech

[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech) is another model that we are investigating, that runs on the PaddlePaddle platform. The package was developed by researchers at Baidu, and is designed to facilitate further research and development in speech translation.

# AssemblyAI

We also looked at AssembyAI, but it was a paid service and not fully opensource.
Brief Description -
AssemblyAI, an API platform for state-of-the-art AI models, is a leading name in the Speech-to-Text API market. The AI startup is growing quickly thanks to industry-best accuracy, an easy-to-use interface, and cutting-edge AI models such as Speaker Diarization, Topic Detection, Entity Detection, Automated Punctuation and Casing, Content Moderation,, Sentiment Analysis, Text Summarization, and more.
The company offers several free transcription hours for audio files or video streams per month before transitioning to an affordable paid tier.
Its high accuracy and collection of AI models like Speaker Diarization and Sentiment Analysis makes AssemblyAI a sound option for developers looking for a free Speech-to-Text API. The API also supports virtually every audio and video file format out-of-the-box for easier transcription.
AssemblyAI has expanded the languages it supports to include English, Spanish, French, German, Japanese, Korean, and much more, with additional languages being released monthly. See the full list here. AssemblyAI’s easy-to-use models also allow for quick set-up and transcription in any programming language. You can even copy/paste code examples in your preferred language directly from the AssemblyAI Docs.


# Google Speech to text

We will not be going with Google Speech to text as we want our project to be completely open-source.
Brief Description -
Google Speech-to-Text is a well known speech transcription API. Google gives users 60 minutes free transcription, with $300 in free credits for Google Cloud hosting.
However, since Google only supports transcribing files already in a Google Cloud Bucket, the free credits won’t get you very far. Google can also be a bit difficult to get started with since you need to sign up for a GCP account and project, even to use the free tier, which is surprisingly complicated.
Still, with good accuracy and 63+ languages supported, Google is a decent choice if you’re willing to put in some initial work.

# AWS Transcribe
We will not be going with AWS Trascribe as we want our project to be completely open-source.
Brief Description -
AWS Transcribe offers one hour free per month for the first 12 months of use.
Like Google, you must create an AWS account first if you don’t already have one, which is a complex process. AWS also has lower accuracy compared to alternative APIs and only supports transcribing files already in an Amazon S3 bucket.
However, if you’re looking for a specific feature, like medical transcription, AWS has some intriguing options. Its Transcribe Medical API is a medical-focused ASR option that is available today.

# DeepSpeech

We are currently exploring DeepSpeech but most of the code is in C++. For over the air translation, DeepSpeech is a good option.
Brief Description -
[DeepSpeech](https://github.com/mozilla/DeepSpeech) is an open source embedded Speech-to-Text engine designed to run in real-time on a range of devices, from high-powered GPUs to a Raspberry Pi 4. The DeepSpeech library uses end-to-end model architecture pioneered by Baidu.
DeepSpeech also has decent out-of-the-box accuracy for an open source option, and is easy to fine tune and train on your own data.

# Kaldi

We are currently exploring Kaldi. A good starting point is this [tutorial.](https://www.assemblyai.com/blog/kaldi-speech-recognition-for-beginners-a-simple-tutorial/)
Brief Description -
[Kaldi](https://github.com/kaldi-asr/kaldi) is a speech recognition toolkit that has been widely popular in the research community for many years.
Like DeepSpeech, Kaldi has good out-of-the-box accuracy and supports the ability to train your own models. It’s also been thoroughly tested --a lot of companies currently use Kaldi in production and have used it for a while--making more developers confident in its application.

# Wav2Letter

We will not be going with Wav2Letter as it is majorly written in C++.
Brief Description -
[Wav2Letter](https://github.com/flashlight/wav2letter) is Facebook AI Research’s Automatic Speech Recognition (ASR) Toolkit, also written in C++, and using the ArrayFire tensor library.
Like DeepSpeech, Wav2Letter is decently accurate for an open source library and is easy to work with on a small project.

# SpeechBrain

We will be actively looking at Speechbrain and compare it against Whisper to see its performance. 
Brief Description -
[SpeechBrain](https://github.com/speechbrain/speechbrain) is a PyTorch-based transcription toolkit. The platform releases open implementations of popular research works and offers a tight integration with HuggingFace for easy access.
Overall, the platform is well-defined and constantly updated, making it a straightforward tool for training and finetuning.

# CoQui

Coqui is majorly written in C++. We will not be considering it for our project.
Brief Description -
[Coqui](https://github.com/coqui-ai/STT) is another deep learning toolkit for Speech-to-Text transcription. Coqui is used in over twenty languages for projects and also offers a variety of essential inference and productionization features.
The platform also releases custom trained models and has bindings for various programming languages for easier deployment.


# Readme and setup for whisper-playground for 'as-real-as-it-gets' time translation

## Setup
1. Whisper requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) and [`portaudio`](http://portaudio.com/docs/v19-doxydocs/index.html) to be installed on your system, which is available from most package managers:
```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg
sudo apt install portaudio19-dev

# on Arch Linux
sudo pacman -S ffmpeg
sudo pacman -S portaudio

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg
brew install portaudio

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
### note: if you are using node version greater than 16, please also use the following command on the second terminal where you run yarn from. (for best results, use node version 16 itself)
2. for node version greater than 16:  `export NODE_OPTIONS=--openssl-legacy-provider`
3. Clone or fork this repository
4. Install the backend and frontend environmet `sh install_playground.sh`
5. Run the backend `cd backend && source venv/bin/activate && flask run --port 8000`
6. In a different terminal, run the React frontend `cd interface && yarn start` for the real time translation functionality's frontend
7. In yet another terminal, run `cd video_subs/my-app && npm start` to start the frontend for the video subtitle feature
## License
This repository and the code and model weights of Whisper are released under the MIT License.