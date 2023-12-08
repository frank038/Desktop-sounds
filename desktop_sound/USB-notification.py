#!/usr/bin/env python3

# 20231208

#####################
# audio player
a_player = "aplay"

# whether to send notification
USE_USB_NOTIFICATION = 1
# 1 disable sound
NOTIFICATION_NO_SOUND = 0

#####################


# whether to monitor the usb devices - 1 mandatory
USE_USB_DEVICES = 1

if USE_USB_DEVICES:
    import pyudev
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


if USE_USB_DEVICES:
    # list of idV idP Name Class
    dev_lst = []
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    monitor.start()

    for device in iter(monitor.poll, None):
        if device.action == "add":
            if device.get('DEVTYPE') == "usb_device":
                vendor = device.get('ID_VENDOR_ID')
                product = device.get('ID_MODEL_ID')
                hw_model = device.get('ID_MODEL_FROM_DATABASE') or device.get('ID_MODEL_ID')
                device_type = device.get('ID_USB_MODEL') or device.get('ID_MODEL') or "USB device"
                # device_class = ""
                dev_lst.append([vendor, product, hw_model, device_type])
                #
                #global USE_USB_NOTIFICATION
                # disable notification
                if os.path.exists(os.path.join(curr_path, "notification-usb-no-notification")):
                    USE_USB_NOTIFICATION = 0
                else:
                    USE_USB_NOTIFICATION = 1
                #
                if USE_USB_NOTIFICATION and shutil.which("notify-send"):
                    iicon_type = "icons/usb-port.png"
                    icon_path = os.path.join(os.getcwd(), iicon_type)
                    command = ["notify-send", "-i", icon_path, "-t", "3000", "-u", "normal", hw_model, "Inserted"]
                    try:
                        subprocess.Popen(command)
                    except: pass
                #
                #global NOTIFICATION_NO_SOUND
                # disable sound
                if os.path.exists(os.path.join(curr_path, "notification-usb-no-sound")):
                    NOTIFICATION_NO_SOUND = 1
                else:
                    NOTIFICATION_NO_SOUND = 0
                #
                if not NOTIFICATION_NO_SOUND:
                    play_sound("USB-Insert.wav")
        #
        elif device.action == "remove":
            if device.get('DEVTYPE') == "usb_device":
                dvendor, dproduct, _ = device.get('PRODUCT').split("/")
                #
                dv_len = len(dvendor)
                if dv_len < 4:
                    zero_added = 4 - dv_len
                    dvendor = "0"*zero_added+dvendor
                dp_len = len(dproduct)
                if dp_len < 4:
                    zero_added = 4 - dv_len
                    dproduct = "0"*zero_added+dproduct
                # 
                device_type = device.device_type
                hw_model = "USB device: {} {}".format(dvendor, dproduct)
                for ddev in dev_lst:
                    if ddev[0] == dvendor and ddev[1] == dproduct:
                        if ddev[2]:
                            hw_model = ddev[2]
                        else:
                            hw_model = "{} {}".format(ddev[0], ddev[1])
                        dev_lst.remove(ddev)
                        break
                #
                #global USE_USB_NOTIFICATION
                # disable notification
                if os.path.exists(os.path.join(curr_path, "notification-usb-no-notification")):
                    USE_USB_NOTIFICATION = 0
                else:
                    USE_USB_NOTIFICATION = 1
                #
                if USE_USB_NOTIFICATION and shutil.which("notify-send"):
                    iicon_type = "icons/usb-port.png"
                    icon_path = os.path.join(os.getcwd(), iicon_type)
                    command = ["notify-send", "-i", icon_path, "-t", "3000", "-u", "normal", hw_model, "Removed"]
                    try:
                        subprocess.Popen(command)
                    except: pass
                #
                #global NOTIFICATION_NO_SOUND
                # disable sound
                if os.path.exists(os.path.join(curr_path, "notification-usb-no-sound")):
                    NOTIFICATION_NO_SOUND = 1
                else:
                    NOTIFICATION_NO_SOUND = 0
                #
                if not NOTIFICATION_NO_SOUND:
                    play_sound("USB-Remove.wav")
                
