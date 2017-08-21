# encoding=utf-8
import os
import requests
from playsound import playsound
import config


def get_voice_file(word):
    voice_file = os.path.join(config.VOICE_DIR, word + '.mp3')
    if not os.path.isfile(voice_file):
        r = requests.get(config.VOICE_URL.format(word=word))
        with open(voice_file, 'wb') as f:
            f.write(r.content)
    return voice_file


def play_voice_file(voice_file):
    playsound(voice_file)


def read_one_word(word):
    word = word.lower()
    voice_file = get_voice_file(word)
    try:
        play_voice_file(voice_file)
        return True
    except IOError:
        print "Sorry, can't find voice of world: " + word
        return False
