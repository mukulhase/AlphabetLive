import os
import subprocess
import sys
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()
print(model_path)

speech = LiveSpeech(
    verbose=False,
    sampling_rate=48000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'mukul.dict')
)

# speech.set_jsgf_file("letters", "vimium.gram")

wordtonum = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "escape": "Escape",
    "delete": "Delete",
    "back": "BackSpace",
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "enter": "Return",
    "at": "at",
    "dot": "period"
}

modifiers = {
    "shift": "Shift",
    "control": "Control_L",
    "capital": "Shift"
}


def get_window_id():
    arch = subprocess.check_output("xwininfo | grep \"Window id:\"", shell=True)
    return str(arch).split(" ")[3]


window_id = get_window_id()

for phrase in speech:
    modifier = False
    for i in str(phrase).split(" "):
        if i in modifiers.keys():
            modifier = modifiers[i]
        else:
            if i in wordtonum.keys():
                i = wordtonum[i]
            if modifier:
                i = "%s+%s" % (modifier, i)
            command = "xdotool windowactivate --sync %s key %s" % (window_id, i)
            os.system(command)
            modifier = False
    print(phrase)
