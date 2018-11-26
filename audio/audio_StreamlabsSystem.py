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

#-----------------
# Global Variables
#-----------------
settings = None
audio_commands = None

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
            t = f.read().decode('utf-8-sig')  # Settings files are encoded with utf-8 BOM
            settings = json.loads(t)
            log("Settings are: " + str(settings))
    else:
        message = "No audio folder location saved, please select a location and save it"
        log(message)
        raise Exception(message)
    global audio_commands
    audio_commands = get_audio_commands(settings['audio_folder'])

    return

def get_audio_commands(folder_path):
    audio_commands = {}
    if not os.path.exists(folder_path):
        Parent.SendStreamMessage("Audio folder does not exist: {0}".format(folder_path))
        raise Exception("folder does not exist: {0}".format(folder_path))
    folder_contents = os.listdir(folder_path)
    for i in folder_contents:
        path = folder_path + os.path.sep + i
        if not os.path.isfile(path):
            pass
        command_name = i.split('.')[0]
        command_name = command_name.split('_-_')[0]  # Remove potential command author
        audio_commands['!' + command_name] = path
    return audio_commands


def playsound(filepath, volume=100.0):
    '''Helper to make sure the sound actually plays if multiple sound effects are colliding. Only one sound may play at a time'''
    for i in range(1000):
        if Parent.PlaySound(filepath, volume):
            return True
        sleep(1)
    return False

def print_audio_commands():
    global audio_commands
    text = "Audio commands are: " + ", ".join(sorted(audio_commands.keys()))
    Parent.SendStreamMessage(text)

def play_audio_command(message):
    global audio_commands
    command = message.split()[0]
    if command in audio_commands:
        playsound(audio_commands[command])
        return True
    return False

def Execute(data):
    message = data.Message
    user = data.User

    try:
        if message.startswith("!audio"):  # TODO add generic text message abilities here too
            print_audio_commands()
        if play_audio_command(message):
            return
        # Place mod only commands below this check
        elif not Parent.HasPermission(user, "Moderator", "na"):
            return
    except Exception as e:
        log('Exception: {m}'.format(m=e.message))

def Tick():
  return
