#!/bin/bash
import -window root /tmp/screen.jpg
mogrify -blur 0x8 /tmp/screen.jpg
icon="$HOME/.lock_icon.png"
if [ -f $icon ]; then
	composite -gravity Center $HOME/.lock_icon.png /tmp/screen.jpg /tmp/screen.png
fi
i3lock -u -i /tmp/screen.png
rm /tmp/screen.*
