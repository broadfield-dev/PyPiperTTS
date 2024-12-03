PyPiper: A Python Interface for Piper Text-to-Speech
===========================================================
PyPiper is a Python library that provides a simple and intuitive interface to the Piper text-to-speech system. It allows you to generate high-quality speech from text using pre-trained models.
Installation
---------------
To use PyPiper, you'll need to have Python 3.6 or later installed on your system. You can install the required dependencies using pip:
Bash
pip install -r requirements.txt
Usage
-----
Initializing the PyPiper Object
To start using PyPiper, create an instance of the PyPiper class:
Python
from pypiper import PyPiper

piper = PyPiper()
Generating Speech
You can generate speech from text using the tts method:
Python
output_file = piper.tts("Hello, world!")
print(output_file)
This will generate a WAV file containing the synthesized speech.
Streaming Speech
You can also stream the synthesized speech in real-time using the stream_tts method:
Python
for audio_chunk in piper.stream_tts("Hello, world!"):
    # Process the audio chunk
    print(audio_chunk)
Saving and Loading Model Settings
You can save and load model settings using the save_set and load_set methods:
Python
# Save model settings
set_file = piper.save_set("en_US-joe-medium", 1, 1, 1, 1)

# Load model settings
model, length, noise, width, pause = piper.load_set(set_file)
print(model, length, noise, width, pause)
Requirements
------------
Python 3.6 or later
Piper text-to-speech system (https://github.com/rhasspy/piper)
pydub library for audio processing
requests library for downloading models
License
-------
PyPiper is released under the MIT License. See the LICENSE file for details.
