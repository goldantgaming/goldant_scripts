import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import os
import time
import threading
import logging

from time import sleep

log = logging.getLogger(__name__)


#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Custom Commands"
Website = "https://www.twitch.tv/goldant"
Description = "Various custom commands"
Creator = "GoldAnt"
Version = "1.0.0.1"

#---------------------------------------
# Set Variables
#---------------------------------------
local_directory = "c:\\streamlabs"
path = local_directory + os.path.sep + 'timer.txt'
timer_thread = None
remaining_time = None
timer_title = None

scenes = ['game', 'starting', 'lobby', 'pushups', 'brb', 'credits']

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    reset()
    return

def reset():
    # Empty for now
    return

def playsound(filepath, volume=100.0):
    '''Helper to make sure the sound actually plays if multiple sound effects are colliding. Only one sound may play at a time'''
    for i in range(1000):
        if Parent.PlaySound(filepath, volume):
            return True
        sleep(1)
    return False

def antqueen():
    Parent.SendStreamMessage("Getting ripped for the Antqueen!")
    playsound("C:\\Users\\golda\\Google Drive\\documents\\Streaming\\Sounds\\effects\\antqueen\\antqueen.mp3")
    Parent.SetOBSSourceRender("antqueen", True, "Alerts and Avatars")
    sleep(10)
    Parent.SetOBSSourceRender("antqueen", False, "Alerts and Avatars")
    
def print_audio_sources():
    sources = Parent.GetOBSSpecialSources(Parent.SendStreamMessage)
    sources = ','.join(sources)
    text = "Audio Sources are: {0}".format(sources)
    Parent.SendStreamMessage(text)

def test():
    Parent.Log('Custom_Commands', 'Running test command')

def list_scenes():
    text = 'Scenes are: ' + ', '.join(scenes)
    Parent.SendStreamMessage(text)

def switch_scene(message):
    scene = ' '.join(message.split()[1:])
    Parent.SetOBSCurrentScene(scene, Parent.SendStreamMessage('scene switched to "{0}"'.format(scene)))

def Execute(data):
    message = data.Message
    user = data.User
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

def run_timer(ttlseconds, title=None):
    template = '{time_text}'
    global timer_title
    timer_title = title
    if title:
        template = '{title}: '.format(title=title) + template
    start_time = time.time()
    global remaining_time
    remaining_time = ttlseconds
    current_time = start_time
    try:
        global timer_thread
        while remaining_time > 0 and timer_thread:
            minutes, seconds = divmod(remaining_time, 60)
            hours, minutes = divmod(minutes, 60)
            time_text = ''
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            if hours > 0:
                time_text = '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(hours=hours, minutes=minutes, seconds=seconds)
            elif minutes > 0:
                time_text = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
            else:
                time_text = '{seconds:02d}'.format(seconds=seconds)

            text_to_write = template.format(time_text=time_text)
            global path
            with open(path, 'w') as f:
                f.seek(0)
                f.write(text_to_write)
                f.flush()

            remaining_time = ttlseconds - (time.time() - start_time)
            time_to_sleep = (remaining_time % 1) + .01
            sleep(time_to_sleep)           
            Parent.Log('timer', 'remaining_time: {0}, time_to_sleep: {1}'.format(remaining_time, time_to_sleep))
        text = "{ttlseconds} second timer finished".format(ttlseconds=ttlseconds)
        if title:
            text = text + ": {title}".format(title=title)
        Parent.SendStreamMessage(text)
        global path
        with open(path, 'w') as f:
            f.seek(0)
            f.write('')
            f.flush()
    except Exception as e:
        Parent.Log('timer', 'Exception: {m}'.format(m=e.message))
  
def Tick():
  return
