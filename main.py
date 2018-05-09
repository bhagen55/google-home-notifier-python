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

chromecast_name = "Techhouse" #edit me to be your google home group
path = "/static/cache/"

app = Flask(__name__)
logging.info("Starting up chromecasts")
chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == chromecast_name)
mc = cast.media_controller

force_cast = False
vol_level = 1

@app.route('/chromecast/<name>')
def switch_chromecast(name):
    print(name.strip())
    print(ascii(chromecasts))
    if name.strip() in chromecasts:
        cast = next(cc for cc in chromecasts if cc.device.friendly_name == name)
        mc = cast.media_controller
        return "Chromecast is now set to: " + cast
    else:
        return "Chromecast " + name + " is not available"

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

@app.route('/force/<choice>')
def force_play(choice):
    global force_cast
    if choice == "true":
        force_cast = True
        return "Force changed to " + str(force_cast)
    elif choice == "false":
        force_cast = False
        return "Force changed to " + str(force_cast)
    else:
        return "Invalid Input. Force is currently " + str(force_cast)

@app.route('/vol/<level>')
def set_vol(level):
    global vol_level
    level = int(level)
    if level <= 1 and level >= 0:
        vol_level = level
        return "vox volume set to " + str(vol_level)
    else:
        return "invalid input, please give a value between 0 and 1"

def play_mp3(mp3_url):
    print(cast.status.is_active_input)
    if str(cast.status.is_active_input) == "None":
        cast.wait()
        old_vol = cast.status.volume_level
        cast.set_volume(vol_level)
        mc.play_media(mp3_url, 'audio/mp3')
        cast.wait()
        #cast.set_volume(old_vol)
        return True
    else:
        return False


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


@app.route('/say/<text>')
def say(text):
    if not text:
        return False
    if not lang:
        lang = "en"
    play_tts(text, lang=lang)
    return text


@app.route('/sayvox/<text>')
def sayvox(text):
    if not text:
        return False
    else:
        filename = get_vox_mp3(text)
        if filename is None:
            return "Vox can't say any of those words"
        else:
            urlparts = urlparse(request.url)
            mp3_url = "http://" + urlparts.netloc + "/" + filename
            played = play_mp3(mp3_url)
            if played:
                return "vox says: " + filename
            else:
                return "cast is in use"

def get_vox_mp3(text):
    return vox.savetomp3(text)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
