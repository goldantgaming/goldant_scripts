import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import os
import time

from time import sleep

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Spin"
Website = "https://www.twitch.tv/goldant"
Description = "!spin will remove points from users."
Creator = "GoldAnt"
Version = "1.0.0.2"

#---------------------------------------
# Set Variables
#---------------------------------------
local_directory = "c:\\streamlabs"  # Don't change this folder
users_file_path = local_directory + os.path.sep + 'spin_users.txt'
count_file_path = local_directory + os.path.sep + 'spin_count.txt'
points_to_remove = 100
MAX_TICKETS = 10
tickets = []

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    reset()


def reset():
    global tickets
    tickets = []
    if not os.path.exists(local_directory):
        os.mkdir(path=local_directory)
    # Flush file since chatbot has restarted
    with open(users_file_path, 'w') as f:
        f.write('')
        f.flush()
    with open(count_file_path, 'w') as f:
        f.write('')
        f.flush()
    return


def Execute(data):
    message = data.Message
    user = data.User
    username = data.UserName
    points = Parent.GetPoints(user)
    
    if not message.startswith("!spin"):
        return
    if 'reset' in message:
        if not Parent.HasPermission(user, "Moderator", "na"):
            Parent.SendStreamMessage("Only moderators may use the reset command".format(user=user))
            return
        reset()
        Parent.SendStreamMessage("Resetting tickets.")
        return
    global tickets
    if len(tickets) > MAX_TICKETS:
        Parent.SendStreamMessage("All the tickets sold out, please wait until the next session.")
        return
    
    if user in tickets:
        Parent.SendStreamMessage("{user} has already purchased a ticket this session.".format(user=user))
        return

    if points - points_to_remove >= 0:
        Parent.AddPoints(user, username, -points_to_remove)
        remaining_points = Parent.GetPoints(user)
        text = "User {user} has spun the wheel for {points} points and has {remaining} points left.".format(user=user, points=points_to_remove, remaining=remaining_points)
        Parent.SendStreamMessage(text)
        Parent.Log("spin", text)
        tickets.append(user)
        # Add user to the file list
        with open(users_file_path, 'w') as f:
            text = '\n'.join(tickets)
            f.write(text)
            f.flush()
        with open(count_file_path, 'w') as f:
            f.seek(0)
            f.write('{count}'.format(count=len(tickets)))
            f.flush()
    else:
        remaining_points = Parent.GetPoints(user)
        text = "User {user} does not have the {points} points to spin the wheel, they currently have {remaining} points remaining.".format(user=user, points=points_to_remove, remaining=remaining_points)
        Parent.SendStreamMessage(text)
        Parent.Log('spin', text)
      
  
def Tick():
  return
