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
import os

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
		# if word[-3:] == 'ing':
		# 	output.append(word[:-3])
		# 	output.append(ing)
		if word[-1:] == ",":
			output.append(word[:-1])
			output.append(comma)
		elif word[-1:] == ".":
			output.append(word[:-1])
			output.append(period)
		else:
			output.append(word)
	return output


# Play sentence
def playwords(sentence):
	words = convertsentence(sentence)
	for word in words:
		play(word)


# Wrapper to add path and filetype
def play(word):
	playsound(soundpath + word + filetype)


# Save sentence as an mp3
def savetomp3(sentence):
	if os.path.isfile(combined_path + sentence + ".mp3"):
		print("Sentence already in cache, not re-creating")
	else:
		words = convertsentence(sentence)
		playlist = AudioSegment.silent(duration=500)
		for word in words:
			if not os.path.isfile(soundpath + word + filetype):
				print(word + " does not exist, skipping")
				sentence = sentence.replace(word, '')
			else:
				word_mp3 = AudioSegment.from_mp3(soundpath + word + filetype)
				playlist = playlist.append(word_mp3)
		playlist.export(combined_path + sentence + ".mp3", format="mp3", bitrate="100k")
	return(combined_path + sentence + ".mp3")


if __name__ == "__main__":
	saystring = sys.argv[1];
	# playwords(saystring)
	savetomp3(saystring)
