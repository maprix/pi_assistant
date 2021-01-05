#!/usr/bin/env python3
import os
import subprocess
import pyaudio
import deepspeech
import numpy as np
from queue import SimpleQueue

# references:
# https://github.com/mozilla/DeepSpeech
# https://github.com/AASHISHAG/deepspeech-german
# https://tradokk.com/echtzeit-spracherkennung-mit-deepspeech/
# https://www.cnx-software.com/2019/08/30/using-sony-ps3-eye-camera-as-an-inexpensive-microphone-array/
BUFFERS_PER_SECOND = 10
SAMPLE_WIDTH = 2
BEAM_WIDTH = 512
LANG='de-DE'

#switch between English and German model
#MODEL_PATH = 'models/en/deepspeech-0.9.3-models.tflite'
#SCORER_PATH = 'models/en/deepspeech-0.9.3-models.scorer'
MODEL_PATH = 'models/de/AASHISHAG/release_v0.9.0/output_graph.tflite'
SCORER_PATH = 'models/de/AASHISHAG/release_v0.9.0/kenlm.scorer'

buffer_queue = SimpleQueue()


def audio_callback(in_data, frame_count, time_info, status_flags):
    buffer_queue.put(np.frombuffer(in_data, dtype='int16'))
    return (None, pyaudio.paContinue)


def find_device(pyaudio, device_name):
    ''' find specific device or return default input device'''
    default = pyaudio.get_default_input_device_info()
    for i in range(pyaudio.get_device_count()):
        name = pyaudio.get_device_info_by_index(i)['name']
        if name == device_name:
            return (i, name)
    return (default['index'], default['name'])

def say(text, language='en-GB', file='output.wav'):
    p = subprocess.Popen(['pico2wave -l ' + language + ' -w ' + file + ' "' + text + '" && aplay -q ' + file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    if err:
        print(err)
    #This makes the wait possible
    p_status = p.wait()

def main():
    model = deepspeech.Model(MODEL_PATH)
    model.setBeamWidth(BEAM_WIDTH)
    model.enableExternalScorer(SCORER_PATH)

    stream = model.createStream()

    audio = pyaudio.PyAudio()
    index, name = find_device(audio, 'cap') # use cap stream from PS3 cam as defined in /etc/asound.conf

    buffer_size = model.sampleRate() // BUFFERS_PER_SECOND
    audio_stream = audio.open(rate=model.sampleRate(),
                            channels=1,
                            format=audio.get_format_from_width(
                                SAMPLE_WIDTH, unsigned=False),
                            input_device_index=index,
                            input=True,
                            frames_per_buffer=buffer_size,
                            stream_callback=audio_callback)

    num_iterations = BUFFERS_PER_SECOND * 1
    i = 0
    samecount = 0
    textold = ''
    while audio_stream.is_active():
        stream.feedAudioContent(buffer_queue.get())
        if i % num_iterations == 0:
            text = stream.intermediateDecode()
            if text.find('stop') >= 0:
                break
            
            # compare old text with latest recognized text
            if text != '' and text == textold:
                samecount += 1
            textold = text

            # reset stream if recognition is unchanded after 2 seconds
            if samecount >= 1:
                samecount = 0
                textold = ''
                result_text = stream.finishStream() # close decoding stream
                audio_stream.stop_stream()          # stop audio stram before audio autput
                say('Ich habe etwas erkannt', LANG)
                print(f'=> Result: {result_text}')
                audio_stream.start_stream()         # restart audio stram before audio autput
                stream = model.createStream()       # ceate new decoding stream

        i += 1

    print(stream.finishStream())
    audio_stream.close()


if __name__ == '__main__':
    main()