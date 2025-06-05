import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[2].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
    


    
def takecommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listining")
        eel.DisplayMessage("Listining...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 5)
    try:
        print("Reconizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(1)
        
        
    except Exception as e:
        return ""
    return query.lower()


@eel.expose
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        print(query)
        eel.senderText(query)
    
    
    
    try:
        # query = takecommand()
        # print(query)
    
        if "open" in query:
             from engine.features import opencommand
             opencommand(query)
             eel.ShowHood()
        elif "on youtube" in query:
             from engine.features import PlayYoutube
             PlayYoutube(query)
             eel.ShowHood()
        elif "on google" in query or "search for" in query or "search on google" in query:
             from engine.features import SearchGoogle
             SearchGoogle(query)
             eel.ShowHood()
            
        elif "wikipedia" in query:
            from engine.features import search_wikipedia
            info = search_wikipedia(query)
            speak(info)
            eel.ShowHood()
           
        elif "convert into handwritten" in query:
            query = query.replace("convert into handwritten","")
            from engine.features import hand_writting
            
            
            hand_writting(query)
            eel.ShowHood()
            
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag=""
            contact_no, name = findContact(query)
            if(contact_no != 0):
                # speak("Which mode you want to use whatsapp or mobile")
                # preferance = takecommand()
                # print(preferance)

                # if "mobile" in preferance:
                if "send message" in query:
                    flag='message'
                    speak("what message to send")
                    query = takecommand()
                elif "phone call" in query:
                    flag='phone call' 
                else:
                    flag= "video call"                    
                whatsApp(contact_no, query, flag, name)
                eel.ShowHood()
            else:
                print("not exist in contacts")
                eel.ShowHood()
        else:
             from engine.features import chatBot
             chatBot(query)
             eel.ShowHood()
    except Exception as e:
        print(f"error:{e}")
        eel.ShowHood()
        


# text = takecommand()
# speak(text)

