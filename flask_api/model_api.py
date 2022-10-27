import flask
import io
import string
import time
import os 
import numpy as np
import whisper

model = whisper.load_model('medium')

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_snippet():
    pass


@app.route('/', methods=['GET'])
def index():
    return 'Speech Translation'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')