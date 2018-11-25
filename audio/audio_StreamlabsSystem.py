import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import os
import json
import time
import threading

from time import sleep


#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Audio Commands"
Website = "https://www.twitch.tv/goldant"
Description = "Make audio commands from a folder automatically available."
Creator = "GoldAnt"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
local_directory = "c:\\streamlabs"

#------------
# Log Helper
#------------
def log(message):
    Parent.Log(ScriptName, message)

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    reset()
    return

def reset():
    # Reread settings
    chatbot_folder = os.path.dirname(__file__)
    settings_path = os.path.sep.join([chatbot_folder, "settings.json"])
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            log('it worked')
            log(f.read())
    # with f as open(settings_path, 'r'):
    #     settings = json.loads(open(settings_path, 'r').read())  # TODO make this safe if it doesn't exist
    #     log(settings)

    return

def playsound(filepath, volume=100.0):
    '''Helper to make sure the sound actually plays if multiple sound effects are colliding. Only one sound may play at a time'''
    for i in range(1000):
        if Parent.PlaySound(filepath, volume):
            return True
        sleep(1)
    return False

def print_audio_sources():
    sources = Parent.GetOBSSpecialSources(Parent.SendStreamMessage)
    sources = ','.join(sources)
    text = "Audio Sources are: {0}".format(sources)
    Parent.SendStreamMessage(text)

def test():
    Parent.Log('Custom_Commands', 'Running test command')

def Execute(data):
    message = data.Message
    user = data.User

    return # TODO remove this again
    try:
        if message.startswith("!antqueen"):
            antqueen()
        elif message.startswith("!audiosources"):
            print_audio_sources()

        # Place mod only commands below this check
        elif not Parent.HasPermission(user, "Moderator", "na"):
            return
        elif message.startswith("!scenes"):
            list_scenes()
        elif message.startswith("!scene "):
            switch_scene(message)
        elif message.startswith("!test "):
            test()
    except Exception as e:
        Parent.Log('Custom_Commands', 'Exception: {m}'.format(m=e.message))

    return  # Making this return to keep this logic here for now, will eventually want to add permissions like I did below

def Tick():
  return
