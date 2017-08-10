#!/usr/bin/env python3

import i3ipc
import NetworkManager
import os
import sys
import time
import multiprocessing
import subprocess

def i3_plugin(i3, focused_color, unfocused_color, urgent_color, bg_color, focused_bg_color,u_color):
    """Return i3 workspaces information"""
    string = "%{A5:i3-msg workspace next:}%{A4:i3-msg workspace prev:}"
    try:
        ws_list = i3.get_workspaces()
    except:
        time.sleep(0.5)
        i3=i3ipc.Connection()
        ws_list = i3.get_workspaces()
    for ws in ws_list:
        string+="%{U"+u_color+"}%{F"
        if ws.urgent:
            string += urgent_color
        elif ws.focused:
            string += focused_color
        else:
            string += unfocused_color
        string+='}'
        if ws.focused:
            string += '%{B'+focused_bg_color+"}%{+u}"
        string += "  "+ws.name+"  "
        if ws.focused:
            string+="%{B"+bg_color+"}%{-u}"
    return string+"%{A}%{A}"

def wifi_plugin(colors):
    #BEWARE: color assignment is a bit messy
    """return wifi status"""
    string=''
    symbol = 'X'
    color = '#FFFFFF'
    symbol= '#'
    try:
        devices = NetworkManager.NetworkManager.GetAllDevices()
        for device in devices:
            if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
                state = device.State
                #Failed state
                if state <=20 or state == 120: 
                    color = colors["white"]
                    symbol = '%{F'+colors["red"]+"}"+'\uf1eb'+"%{F"+colors["dcolor7"]+"}%{-u}"
                #Connected state
                elif state == 100:
                    color = colors["dcolor7"]
                    power = device.ActiveAccessPoint.Strength
                    if power <=25:
                        symbol = '\uf1eb'
                    elif power >= 75:
                        symbol = '\uf1eb'
                    else: 
                        symbol = '\uf1eb'
                #Disconnected state
                elif state == 30:
                    color = colors["dcolor3"]
                    symbol = '\uf141'
                #Generic transition state
                else:
                    color = colors["dcolor5"]
                    symbol = '\uf1eb'
    except:
        color=colors["dcolor7"]
        symbol= '\uf066'
    string = "%{F" + color + "}" + symbol + "%{F" + colors["dcolor7"] + "}"
    return string

def lan_plugin(colors):
    try:
        devices = NetworkManager.NetworkManager.GetAllDevices()
        for device in devices:
            if device.DeviceType == NetworkManager.NM_DEVICE_TYPE_ETHERNET:
                state = device.State
                #Failed state
                if state <=20 or state == 120: 
                    color = colors["dcolor3"]
                    symbol = '\uf127'
                #Connected state
                elif state == 100:
                    color = colors["dcolor7"]
                    symbol = '\uf0c1'
                #Disconnected state
                elif state == 30:
                    color = colors["dcolor3"]
                    symbol = '\uf127'
                #Generic transition state
                else:
                    color = colors["dcolor5"]
                    symbol = '\uf127'
    except:
        color=colors["dcolor7"]
        symbol= '\uf066'
    string = "%{F" + color + "}" + symbol + "%{F" + colors["dcolor7"] + "}"
    return string

def fixedLen(num):
    """Print numbers <100 with fixed lenght"""
    string = ''
    if num<10:
        string += str(0)
    string += str(num)
    return string

def clock_plugin(colors):
    t = time.strftime("%a %e %b  |  %I:%M %p")
    string = '%{F'+colors["dcolor7"]+'}'+t
    return string

def freespace_plugin(colors):
    info = os.statvfs("/var/")
    freespace = info.f_bsize * info.f_bavail/1024/1024/1024
    string = "%{F"+colors["dcolor7"]+"}"+"\uf1c0  "+"%.1f"%freespace+"Gb"
    return string

def battery_plugin(colors,levelf,pluggedf):
    string='%{F'
    level=''
    while not level.isnumeric():
        levelf.seek(0,0)
        level=levelf.readline()
        level=level.replace("\n","")
    level=int(level)
    plugged=''
    while not plugged.isnumeric():
        pluggedf.seek(0,0)
        plugged=pluggedf.readline()
        plugged=plugged.replace("\n","")
    plugged=int(plugged)
    if level<100:
        if plugged:
            string+=colors["dcolor7"]
        elif level<=5:
                string+=colors["red"]
        else:
            string+=colors["dcolor7"]
    else:
        string+=colors["dcolor7"]
    string+="}"
    if plugged:
        string+='\uf1e6'
    else:
        if level<=20:
            string+='\uf244'
        elif level<=40:
            string+='\uf243'
        elif level<=60:
            string+='\uf242'
        elif level<=80:
            string+='\uf241'
        else: 
            string+='\uf240'
    string+="  "+str(level)+"%%{F"+colors["dcolor7"]+"}"
    return string

def volume_plugin(colors):
    path=os.path.realpath(__file__)
    path=os.path.dirname(path)
    p=subprocess.run(['sh',path+"/volume_level.sh"], stdout=subprocess.PIPE)
    string=''
    for c in str(p.stdout):
        if c.isnumeric():
            string+=c
    level=int(string)
    p=subprocess.run(['sh', path+"/volume_muted.sh"], stdout=subprocess.PIPE)
    if str(p.stdout)[2]=='y':
        muted=True
    else:
        muted=False
    string='%{F'+colors["dcolor7"]+'}'
    if level>0 and not muted:
        if level>=50:
            string+='\uf028' 
        else:
            string+='\uf027'
    else:
        string+='\uf026'
    string+="  %{F"+colors["dcolor7"]+"}%3.0f"%level+'%'
    return string

def lock_plugin(colors,lock_script):
    string="%{F"+colors["dcolor7"]+"}%{A:sh "+lock_script+":}\uf023%{A}%{F"+colors["dcolor7"]+"}"
    return string
def shutdown_plugin(colors):
    string="%{F"+colors["dcolor5"]+"}%{A:shutdown now:}%{A3:reboot:}\uf011%{A}%{A}"
    return string

def status(i3,levelf,pluggedf,colors):
    """Print the final string that will piped to lemonbar """
    s="%{B"+colors['dcolor1']+"}%{F"+colors['dcolor7']+"}%"
    s+="{l}"+i3_plugin(i3,colors['dcolor7'],colors['dcolor7'],colors['red'],colors['dcolor1'],colors['dcolor3'],colors['dcolor3'])
    s+="%{c}"+clock_plugin(colors)+"%{r}"
    s+=wifi_plugin(colors)+"  |  "
    s+=volume_plugin(colors)+"  |  "
    s+=lan_plugin(colors)+"  |  "
    s+=freespace_plugin(colors)+"  |  "
    s+=battery_plugin(colors,levelf, pluggedf)+"  |  "
    s+=lock_plugin(colors,os.path.expanduser("~")+"/.lock_script.sh")+"  |  "
    s+=shutdown_plugin(colors)+"  "
    return s
def print_status(s):
    """Like status, but will also flush the buffer"""
    print(s)
    sys.stdout.flush()

def i3_print(i3,levelf,pluggedf,colors):
    """Function called by the child process to print the final string """
    s=status(i3,levelf,pluggedf,colors)
    print_status(s)

def i3_listener(levelf,pluggedf,colors):
    """It is called by the child process. It will listen to i3 event, and print 
    the status line if there is one, while the father process will print the status 
    if there are changes in the other plugins """
    while 0==0:
        i3=i3ipc.Connection()
        i3.on("workspace::focus",lambda self,e:i3_print(self,levelf,pluggedf,colors))
        i3.on("workspace::urgent",lambda self,e:i3_print(self,levelf,pluggedf,colors))
        i3.main()
        time.sleep(0.5)

if __name__=='__main__':
    #Open battery and ADP files and Xresources file
    try:
        levelf=open("/sys/class/power_supply/BAT0/capacity")
        pluggedf=open("/sys/class/power_supply/ADP1/online")
    except:
        print("Error while opening bat or plug file")
        exit(0)
    home=os.path.expanduser("~")+"/"
    try:
        xres=open(home+".Xresources")
    except:
        print("Error while opening Xresources")
    line=''
    colors={}
    #Read .Xresources color, if they are at the beginning of the file. 
    #They should be called "color" for dark colors and l"color" for 
    #light ones, like "red" and "lred"
    while line[:7]!="#define":
        line=xres.readline()
    while line[:7]=="#define":
        line=line.replace("\t"," ")
        line=line.replace("\n","")
        fields=line.split(" ")
        colors[fields[1]]=fields[2]
        line=xres.readline()
    #Connect to i3 and create child process
    i3=i3ipc.Connection()
    p=multiprocessing.Process(target=i3_listener,args=(levelf,pluggedf,colors,))
    p.start()
    old_s=''
    #Print s 2 times to fix the background color
    s=status(i3,levelf,pluggedf,colors)
    print_status(s)
    #It will print a new status line only if it's different from the last one. It will check every 0.5 sec,
    #instead of the child process, that is a lot more reactive to i3 events.
    while 0==0:
        s=status(i3,levelf,pluggedf,colors)
        if s != old_s:
            print_status(s)
            old_s = s
        time.sleep(0.5)
    levelf.close()
    pluggedf.close()

