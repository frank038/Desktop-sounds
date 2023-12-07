#!/usr/bin/env python3

# 20231207

# e.g.: "Thunderbird" because has its own sound notification
PROGRAMS_TO_SKIP = []

# ["*"] to skip all notifications containing id - id is a number e.g. [1111]
ID_TO_SKIP = ["*"]

# to play a different sound: [id, sound_file] e.g. [[id, sound_file], [id, sound_file], etc.]
# put the sound file in the sound folder
ID_SPECIAL = []

# program to play wav files
a_player = "aplay"

############## audio player
# from pydub import AudioSegment
# from pydub.playback import play

import os

def play_sound(_sound):
    # song = AudioSegment.from_wav("sounds/"+_sound)
    # play(song)
    #
    os.system("{0} {1} 1> /dev/null 2> /dev/null".format(a_player, "sounds/"+_sound))
    return


import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop


def dbus_to_python(data):
    '''
        convert dbus data types to python native data types
    '''
    if isinstance(data, dbus.String):
        data = str(data)
    elif isinstance(data, dbus.Boolean):
        data = bool(data)
    elif isinstance(data, dbus.Int64):
        data = int(data)
    elif isinstance(data, dbus.Double):
        data = float(data)
    elif isinstance(data, dbus.Byte):
        data = int(data)
    elif isinstance(data, dbus.UInt32):
        data = int(data)
    elif isinstance(data, dbus.Array):
        data = [dbus_to_python(value) for value in data]
    elif isinstance(data, dbus.Dictionary):
        new_data = dict()
        for key in data.keys():
            new_data[dbus_to_python(key)] = dbus_to_python(data[key])
        data = new_data
    return data


def notifications(bus, message):
    lvl_sound = None
    msg_lst = message.get_args_list()
    # get the sender program name
    prog = dbus_to_python(msg_lst[0])
    if prog in PROGRAMS_TO_SKIP:
        return
    #
    # play a different sound
    if ID_SPECIAL:
        prog_id = dbus_to_python(msg_lst[1])
        for el_id in ID_SPECIAL:
            if prog_id == el_id[0]:
                lvl_sound = el_id[1]
                break
    # program id
    # if msg_lst[1] or int(msg_lst[1]) == 0:
    if msg_lst[1]:
        if ID_TO_SKIP:
            if ID_TO_SKIP[0] == "*" and int(msg_lst[1]) != 0:
                if lvl_sound == None:
                    return
            else:
                prog_id = dbus_to_python(msg_lst[1])
                if prog_id in ID_TO_SKIP:
                    return
    #
    # get the urgency type
    data = msg_lst[6]
    new_data = dbus_to_python(data)
    lvl_urgency = int(new_data['urgency'])
    # play the sound
    if not lvl_sound:
        lvl_sound = "urgency-normal.wav"
        if lvl_urgency == 0:
            lvl_sound = "urgency-low.wav"
        elif lvl_urgency == 2:
            lvl_sound = "urgency-critical.wav"
    #
    play_sound(lvl_sound)
    
    
DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()

