#pip install pyttsx3

import pyttsx3

tx=pyttsx3.init()

while True:
    robo=input('Enter the text : ')
    if robo=='quit':
        break
    else:
        tx.say(robo)
        tx.runAndWait()