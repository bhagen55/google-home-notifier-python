# Takes strings as input and attempts to speak them
# using HL1 vox voice files.

# Alarm sounds:
#	- deeoo
#	- doop
#	- woop
#	- bizwarn
#	- buzwarn
import sys
from playsound import playsound
from pydub import AudioSegment

soundpath = "static/"
filetype = ".mp3"
combined_path = "static/cache/"

comma = "_comma"
period = "_period"
ing = "ing"


# Takes sentence and seperates into individual words
def convertsentence(sentence):
	words = sentence.split()

	output = []

	for word in words:
		if word[-3:] == 'ing':
			output.append(word[:-3])
			output.append(ing)
		elif word[-1:] == ",":
			output.append(word[:-1])
			output.append(comma)
		else:
			output.append(word)
	return output

# Play words
def playwords(words):
	for word in words:
		play(word)

# Wrapper to add path and filetype
def play(word):
	playsound(soundpath + word + filetype)

# Save words as an mp3
def savetomp3(words):
	mp3s = []
	combined = AudioSegment

	playlist = AudioSegment.silent(duration=500)
	for word in words:
		song = AudioSegment.from_mp3(soundpath + word + filetype)
		playlist = playlist.append(song)
	playlist.export(combined_path + "output.mp3", format="mp3")

if __name__ == "__main__":
	saystring = sys.argv[1];
	playwords(convertsentence(saystring))
	savetomp3(convertsentence(saystring))
