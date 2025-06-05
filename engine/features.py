import re
# from pipes import quote
from pipes import quote
import subprocess
# from hugchat import hugchat
from hugchat import hugchat
from playsound import playsound
import eel
import os
import pyaudio
import struct
import pvporcupine
import pyautogui
import pygetwindow as gw
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import webbrowser
import sqlite3
import time

from engine.helper import extract_yt_term, remove_words,extract_google_term,extraxt_wiki_term

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# playing sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)



def opencommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
    app_name = query.strip()
    if app_name!="":
        print(app_name)
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()
            print(results)
            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])
                

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                print(results)
                if len(results) != 0:
                    print("opening instagram")
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])
                    print(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                       speak("not found")
            
            
        except:
            speak("some thing went wrong")
        eel.ShowHood()
 

       
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term is None:
        speak("Sorry, couldn't understand the command")
        return
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)
    




def search_wikipedia(query):
    import wikipedia
    try:
        summary = wikipedia.summary(query,sentences=5)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found: {e.options[:5]}")
        return f"Multiple results found: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        speak("No Wikipedia page found for the term.")
        return "No Wikipedia page found for the term."



def SearchGoogle(query):
    search_term = extract_google_term(query)  # reuse the same extractor
    # reuse the same extractor
    if search_term is None:
        speak("Sorry, couldn't understand the command")
        return
    speak("Searching " + search_term + " on Google")
    kit.search(search_term)
 

       
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa","jarvish"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
            
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
        
        
            

# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video','tu']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 5
        jarvis_message = "message send successfully to "+name

    elif flag == 'phone call':
        target_tab = 15
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 14
        message = ''
        jarvis_message = "starting video call with "+name


    
 
    
    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')  # Simulate pressing the Tab key
         # Add a small delay to ensure the tab switch is registered
        active_window = gw.getActiveWindow()  # Get the currently active window
        if active_window:
            print(f"Tab {i}: {active_window.title}")  # Print the tab number and its title
        else:
            print(f"Tab {i}: Unable to fetch the tab name")
    
   
    pyautogui.hotkey('enter')
    speak(jarvis_message)
    
# chat bot 
def chatBot(query):
    
    # from hugchat import hugchat
    from hugchat.login import Login

   # Log in to huggingface and grant authorization to huggingchat
   # DO NOT EXPOSE YOUR EMAIL AND PASSWORD IN CODES, USE ENVIRONMENT VARIABLES OR CONFIG FILES
    user_input = query.lower()
    EMAIL = "abhaychoudhary4578@gmail.com"
    PASSWD = "Abhay4578@"
    cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.chat(user_input).wait_until_done()
    print(response)
    speak(response)
    return response
    
    
    
    
    # chatbot = hugchat(token="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")
    # id = chatbot.new_conversation()
    # chatbot.change_conversation(id)
    # response =  chatbot.chat(user_input)
    # print(response)
    # speak(response)
    # return response


def hand_writting(query):
    from PIL import Image, ImageDraw, ImageFont

    # Your text
    text = query

     # Load a handwriting-style font
    font_path = "handwritten.ttf"  # Make sure this file is in the same folder
    font_size = 30
    font = ImageFont.truetype(font_path, font_size)

    # Create an image with white background
    image = Image.new("RGB", (800, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw the text
    draw.text((20, 60), text, font=font, fill=(0, 0, 139))  # black text

    # Save the image
    image.save("handwriting.png")
    speak("Handwritten-style image saved as handwriting.png")
    print("Handwritten-style image saved as handwriting.png")