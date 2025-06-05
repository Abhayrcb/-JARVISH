import os
import time
import cv2
import eel

from engine.features import *
from engine.command import *
from engine.auth import recognize



def start():
    eel.init("www")
    playAssistantSound()
    
    @eel.expose
    def init():
        
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recognize.AuthenticateFace()
        
        if flag==1:
            eel.hideFaceAuth()
            speak("Face Authenticaton Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome sir How Can I Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            eel.showloader()
            speak("Face Authenticaton failed")
        
    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost',block=True)