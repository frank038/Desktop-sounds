# Desktop-sounds
How to get some sounds when some events happen.

desktop_nofitication.py
With this python program, when a desktop notification appears a sound plays.
Some options can be changed at the beginning of the file.
A notification daemon is needed.
As audio player, aplay is already setted, but can be changed.
The dbus python module is also required.
A different sound can be played based on the urgency level: low, normal or critic. A custom sound can be chosen based on the id option (this is one of the notification daemons and clients options). A specific program can be skipped, or a notification by its id.
