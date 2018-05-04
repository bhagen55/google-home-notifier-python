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

soundpath = "vox/"
filetype = ".wav"
comma = "_comma"
period = "_period"


# Takes a string and forms it into filepaths of sounds
def saysentence(saystring):
	words = saystring.split()

	for word in words:
		try:
			if word[-3:] == 'ing':
				play(word[:-3])
				play('ing')
			if word[-1:] == ',':
				play(word[:-1])
				play(comma)
			else:
				play(word)
		except:
			print("Couldn't find " + word)
# Wrapper to add path and filetype
def play(word):
	playsound(soundpath + word + filetype)

if __name__ == "__main__":
	saystring = sys.argv[1];
	saysentence(saystring)
