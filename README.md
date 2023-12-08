# Desktop-sounds
How to get some sounds when some events happen.

* desktop_nofitication.py

With this python program, when a desktop notification appears a sound plays.
Some options can be changed at the beginning of the file.
A notification daemon is needed.
As audio player, aplay is already setted, but can be changed.
The dbus and gi python modules are required.
A different sound can be played based on the urgency level: low, normal or critic; or not played if setted by the user. A custom sound can be chosen based on the id option (this is one of the notification daemons and clients options). A specific program can be skipped, or a notification by its id. If the file 'desktop_notification_silent' is created - also at runtime - in this program folder, sounds will not be played until it is removed.


* USB-notification.py

This program plays a sound when an usb device in inserted or removed. Using notify-send, a notification will appear. Options, in the file: sounds and/or notifications can be disabled; 
if the file 'notification-usb-no-notification' is created, no notifications will be shown, and if the file 'notification-usb-no-sound' is also created, no sounds will be played (both until those file exist). The pyudev module is required. aplay is setted as default audio player.


* xlib-notification.py

This program plays a sound when a normal window appears or a dialog appears. If the file 'notification-xlib-no-sound' is created, no sounds will be played until that exists. The xlib module is required. aplay is setted as default audio player.
