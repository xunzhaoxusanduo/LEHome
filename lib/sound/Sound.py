#!usr/bin/env python
#coding=utf-8


import urllib
import urllib2
from util.log import *


def playwav(path):
    import pyaudio  
    import wave  

    chunk = 1024  
    f = wave.open(path, "rb")  
    p = pyaudio.PyAudio()  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                            channels = f.getnchannels(),  
                            rate = f.getframerate(),  
                            output = True)  
    data = f.readframes(chunk)  
    while data != '':  
        stream.write(data)  
        data = f.readframes(chunk)  
    stream.stop_stream()  
    stream.close()  
    p.terminate() 


AUDIO_SERVER_ADDRESS = None


def get_play_request_url(path, loop=-1):
    global AUDIO_SERVER_ADDRESS
    if AUDIO_SERVER_ADDRESS is None:
        WARN("audio server address is empty.")
        return None
    values = {'url': path}
    if inqueue:
        values["inqueue"] = True
    if not loop == -1:
        values["loop"] = loop
    data = urllib.urlencode(values)
    return AUDIO_SERVER_ADDRESS + '/play?' + data


def play(path, inqueue=False):
    url = get_request_url(path)
    if url is None:
        return
    INFO("sending audio url: " + url)
    try:
        response = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        INFO(e)
        WARN("audio server address is invaild")
    except urllib2.URLError, e:
        INFO(e)
        WARN("audio server unavailable.")
    else:
        INFO("audio response: " + response)