import platform
# import pyaudio
import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
# from nltk import tokenize as tk
from nltk.corpus import stopwords, wordnet
# from operator import itemgetter
# import math
# import pocketsphinx
import sys
import vosk
import json
from vosk import SetLogLevel

SetLogLevel(-1)
# nltk.download("averaged_perceptron_tagger")
# nltk.download("punkt")
# nltk.download("wordnet")

p = platform.system()


def listen():
    rec = sr.Recognizer()
    with sr.Microphone() as src:
        rec.adjust_for_ambient_noise(src)
        audio = rec.listen(src)
    try:
        cmd = rec.recognize_vosk(audio)  # language="en-in")
        # print(f"Command: {cmd}")
    except Exception:
        print("Sorry, couldn't hear. Mind trying typing it?")
        cmd = input()
    # cmd=cmd.split(" ")
    return cmd


# def psphinx():
#     sp = pocketsphinx.LiveSpeech()
#     return sp


def pos_tagger(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatizer(src):
    w = WordNetLemmatizer()
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(src))
    wn_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    ls = []  # lemmatized sentence
    for word, tag in wn_tagged:
        if tag is None:
            ls.append(word)
        else:
            ls.append(w.lemmatize(word, tag))
    return ls


def make_tokens(lms):
    stop_words = set(stopwords.words('english')) # +['Maryam']-['ok'])
    src3 = []
    for i in lms:
        if i in stop_words:
            pass
        else:
            src3.append(str(i)+" ")
    print("Keywords are:", end=' ')
    for i in src3:
        print(i, end=' ')


try:
    while True:
        print("\nSay some words: ")
        c = listen()
        print("Listened value=",c)
        d = json.loads(c)
        print("Command =", d["text"])
        if str(d["text"]).rstrip(" ") in ['stop', 'exit', 'bye', 'quit', 'terminate', 'kill', 'end']:
            print("\n\nExit command triggered from command! Exiting...")
            sys.exit()
        lemmatized = lemmatizer(d["text"])
        make_tokens(lemmatized)
except KeyboardInterrupt:
    print("\n\nExit command triggered from Keyboard! Exiting...")
