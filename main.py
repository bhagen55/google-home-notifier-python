import hl1voxcombiner as vox
import sys
from flask import Flask, request
import socket
import pychromecast
import logging
from gtts import gTTS
from slugify import slugify
from pathlib import Path
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chromecast_name = "GoogleHome" #edit me to be your google home group
path = "/static/cache/"

app = Flask(__name__)
logging.info("Starting up chromecasts")
chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == chromecast_name)

def play_tts(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = slugify(text+"-"+lang+"-"+str(slow)) + ".mp3"

    cache_filename = "." + path + filename
    tts_file = Path(cache_filename)
    if not tts_file.is_file():
        logging.info(tts)
        tts.save(cache_filename)

    urlparts = urlparse(request.url)
    mp3_url = "http://" +urlparts.netloc + path + filename
    logging.info(mp3_url)
    play_mp3(mp3_url)


def play_mp3(mp3_url):
    print(mp3_url)
    cast.wait()
    mc = cast.media_controller
    mc.play_media(mp3_url, 'audio/mp3')

@app.route('/static/<path:path>')
def send_static(path):
        return send_from_directory('static', path)

@app.route('/play/<filename>')
def play(filename):
    urlparts = urlparse(request.url)
    mp3 = Path("./static/"+filename)
    if mp3.is_file():
        play_mp3("http://"+urlparts.netloc+"/static/"+filename)
        return filename
    else:
        return "False"

@app.route('/say/')
def say():
    text = request.args.get("text")
    lang = request.args.get("lang")
    if not text:
        return False
    if not lang:
        lang = "en"
    play_tts(text, lang=lang)
    return text

@app.route('/sayvox/')
def sayvox():
    text = request.args.get("text")
    if not text:
        return False
    play_vox(text)

def play_vox(text):
    vox.savetomp3(text)

    filename = slugify(text) + ".mp3"
    urlparts = urlparse(request.url)
    mp3_url = "http://" +urlparts.netloc + path + filename
    play_mp3(mp3_url)

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
