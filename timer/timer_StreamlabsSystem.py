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
ScriptName = "Timer"
Website = "https://www.twitch.tv/goldant"
Description = "!timer <time> will cause a countdown to occur in a local textfile."
Creator = "GoldAnt"
Version = "1.0.0.3"

#---------------------------------------
# Set Variables
#---------------------------------------
local_directory = "c:\\streamlabs"
path = local_directory + os.path.sep + 'timer.txt'
timer_thread = None
remaining_time = None
timer_title = None


#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    reset()
    return

def reset():
    # Create local directory
    if not os.path.exists(local_directory):
        os.mkdir(path=local_directory)
        
    # Shutdown existing thread if it exists
    global timer_thread
    if timer_thread:
        t = timer_thread  # Putting into a temp variable so that I can delete the reference and then join
        timer_thread = None
        t.join()
        
    # Reset global variables
    global remaining_time
    global timer_title
    remaining_time = None
    timer_title = None
    
    # Flush file
    global path
    with open(path, 'w') as f:
        f.seek(0)
        f.write('')
        f.flush()
    
    return

def Execute(data):
    message = data.Message
    user = data.User
    if message.startswith("!timer"):
        try:
            # Permissions check
            if not Parent.HasPermission(user, "Moderator", "na"):
                Parent.SendStreamMessage("Only moderators may use this command")
                return
            # Parse command
            message_split = message.split()
            Parent.Log('timer', 'Message_split is {m}'.format(m=message_split))
            seconds = int(message_split[1])

            title = None
            if len(message_split) > 2:
                title = ' '.join(message_split[2:])
            # Delete any old threads and start a new thread
            reset()
            Parent.SendStreamMessage("Timer started for {seconds} seconds with title: {title}".format(seconds=seconds, title=title))
            t = threading.Thread(target=run_timer, kwargs={'ttlseconds':seconds, 'title':title})
            global timer_thread
            timer_thread = t
            t.start()
        except Exception as e:
            Parent.Log('timer', 'Exception: {m}'.format(m=e.message))
            Parent.SendStreamMessage("Timer format: !timer <seconds> <Title>")
    return

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
