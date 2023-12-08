#!/usr/bin/env python3

# 20231208

#####################
# audio player
a_player = "aplay"
#####################

# whether to monitor the window manager - always 1
USE_XLIB = 1
#####################

import signal
import sys
import os, shutil
import subprocess
import threading

curr_path = os.getcwd()

############## audio player
# from pydub import AudioSegment
# from pydub.playback import play

def play_sound(_sound):
    # song = AudioSegment.from_wav("sounds/"+_sound)
    # play(song)
    sound_full_path = os.path.join(curr_path, "sounds", _sound)
    # os.system("{0} {1} 1> /dev/null 2> /dev/null".format(a_player, sound_full_path))
    command = [a_player, sound_full_path]
    try:
        subprocess.Popen(command, 
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
    except: pass
    return
#################

NOTIFYSEND = "notify-send"

################################

signal.signal(signal.SIGINT, signal.SIG_DFL)

################################

# disable sound notification if the file notification-xlib-no-sound
# is found in this program folder
NOTIFICATION_XLIB_NO_SOUND = 0

if USE_XLIB:
    from Xlib.display import Display
    from Xlib import X, Xatom, Xutil, error, threaded
    display = Display()

class cThread(threading.Thread):
    def __init__(self, display):
        super(cThread, self).__init__()
        self.display = display
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask=X.PropertyChangeMask)
        #
        self.window_list_init = []
        xlist = self.root.get_full_property(self.display.intern_atom('_NET_CLIENT_LIST'), Xatom.WINDOW)
        if xlist:
            self.window_list_init = xlist.value.tolist()
        # window id - name
        self.window_list_added_2 = []
        
    
    def net_list(self):
        window_list = []
        xlist = self.root.get_full_property(self.display.intern_atom('_NET_CLIENT_LIST'), Xatom.WINDOW)
        if xlist:
            window_list = xlist.value.tolist()
            #
            window_added = [x for x in window_list if x not in self.window_list_init] # if x not in self.window_list_added_2]
            #
            for wii in self.window_list_added_2:
                if wii[0] == window_added:
                    return
            # 
            for ii in window_added:
                try:
                    window = self.display.create_resource_object('window', ii)
                    prop = window.get_full_property(self.display.intern_atom('_NET_WM_WINDOW_TYPE'), X.AnyPropertyType)
                except:
                    prop = None
                if prop:
                    #if self.display.intern_atom('_NET_WM_WINDOW_TYPE_DOCK') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_DESKTOP') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_MENU') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_SPLASH') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_DND') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_NOTIFICATION') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_DROPDOWN_MENU') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_COMBO') in prop.value.tolist():
                    #    continue
                    #elif self.display.intern_atom('_NET_WM_WINDOW_TYPE_POPUP_MENU') in prop.value.tolist():
                    #    continue
                    #el
                    if self.display.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL') in prop.value.tolist() or self.display.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG') in prop.value.tolist():
                        # 
                        win_name_t = None
                        try:
                            win_name_t = window.get_wm_class()
                        except:
                            win_name_t = None
                        win_exec = "Unknown"
                        if win_name_t is not None:
                            win_exec = str(win_name_t[0])
                        #
                        if win_exec:
                            self.window_list_added_2.append([ii, win_exec])
                            self.window_list_init.append(ii)
                            # 
                            if not NOTIFICATION_XLIB_NO_SOUND:
                                play_sound("window-new.wav")
            #
            window_removed = [x[0] for x in self.window_list_added_2 if x[0] not in window_list]
            #
            for ii in window_removed:
                for el in self.window_list_added_2[:]:
                    if el[0] == ii:
                        self.window_list_added_2.remove(el)
                        #
                        if not NOTIFICATION_XLIB_NO_SOUND:
                            play_sound("window-close.wav")
                        break
                        return
        #
        return
                
    def run(self):
        while True:
            xevent = self.display.next_event()
            if (xevent.type == X.PropertyNotify):
                if xevent.atom == self.display.intern_atom('_NET_CLIENT_LIST'):
                    global NOTIFICATION_XLIB_NO_SOUND
                    NOTIFICATION_XLIB_NO_SOUND = 0
                    if os.path.exists(os.path.join(curr_path, "notification-xlib-no-sound")):
                        NOTIFICATION_XLIB_NO_SOUND = 1
                    #
                    self.net_list()
            if thread_stop:
                break
        if thread_stop:
            return


if USE_XLIB:
    threadc = cThread(display)
    threadc.start()
    thread_stop = False

###########################
