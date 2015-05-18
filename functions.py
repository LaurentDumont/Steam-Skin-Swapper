__author__ = 'Laurent Dumont'
__name__ = 'Steam Skin Swapper'

import os
import psutil
import win32security
import urllib
import zipfile
import getpass
import time
from Tkinter import *
from _winreg import *


#SKIN_PATH_XP = os.getenv('APPDATA')
STEAM_PROC_NAME = "Steam.exe"

# Create a skin object with @skin_url and @skin_name


class skin:

    def __init__(self, skin_url, skin_name, skin_archive_name):
        self.skin_url = skin_url
        self.skin_name = skin_name
        self.skin_archive_name = skin_archive_name


#Download the skin @skin_array
def download_skin(skins_array,skin_id):

    if skin_id == 1:
        index = 0
    if skin_id == 2:
        index = 1
    if skin_id == 3:
        index = 2

    if find_steam_path() == 'w7':
        SKIN_PATH = "C:\\Program Files (x86)\\Steam\\skins"

    if find_steam_path() == 'xp':
        SKIN_PATH = "C:\\Program Files\\Steam\skins"

    print "Downloading Skin " + skins_array[index].skin_name
    urllib.urlretrieve(skins_array[index].skin_url, skins_array[index].skin_name)
    with zipfile.ZipFile(skins_array[index].skin_name, "r") as skin_archive:
        if not os.path.exists(SKIN_PATH + "\\" + "\\" + skins_array[index].skin_name):
            os.makedirs(SKIN_PATH + "\\" + "\\" + skins_array[index].skin_name)
            skin_archive.extractall(SKIN_PATH + "\\" + "\\" + skins_array[index].skin_name)

    # for skin in skins_array:
    #     print "Downloading Skin " + skin.skin_name
    #     urllib.urlretrieve(skin.skin_url, skin.skin_name)
    #     with zipfile.ZipFile(skin.skin_name, "r") as skin_archive:
    #         if not os.path.exists(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name):
    #             os.makedirs(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name)
    #         skin_archive.extractall(SKIN_PATH + "\\" + "SteamSkins" + "\\" + skin.skin_name)


def find_steam_path():

    w7_path = "C:\\Program Files (x86)\\Steam\\skins"
    xp_path = "C:\\Program Files\\Steam\skins"
    global win_ver

    if os.path.exists(w7_path):
        win_ver = 'w7'

    if os.path.exists(xp_path):
        win_ver = 'xp'

    return win_ver

def edit_selected_skin(skins_array, skin_id):

    if skin_id == 1:
        index = 0
    if skin_id == 2:
        index = 1
    if skin_id == 3:
        index = 2


    user_name = getpass.getuser()
    sid = win32security.LookupAccountName(None, user_name)[0]
    sidstr = win32security.ConvertSidToStringSid(sid)

    connectRegistry = ConnectRegistry(None, HKEY_USERS)
    skin_key = OpenKey(connectRegistry, sidstr + "\Software\Valve\Steam", 0, KEY_WRITE)
    try:
        SetValueEx(skin_key, 'SkinV4', 0, REG_SZ, skins_array[index].skin_name)
    except EnvironmentError:
        print "Cannot change Registry key"

    CloseKey(connectRegistry)
    CloseKey(skin_key)


def kill_steam_restart():

    time.sleep(2)
    for process in psutil.process_iter():
        try:
            if process.name() == STEAM_PROC_NAME:
                try:
                    process.kill()
                except (os.Error):
                    print ('Cannot kill the Steam process. Please restart Steam manually')
        except (psutil.AccessDenied):
            print ('Cannot access process information')

    os.system('"C:\\Program Files (x86)\\Steam\\Steam.exe"')


def create_skin_objets():

    #Create the global variables containing the skins.
    global steamCompact
    global steamEnhanced
    global steamAir
    global skin_list

    skin_list = []
    #0
    steamCompact = skin("http://sss.coldnorthadmin.com/skins/compact/compact.zip", "compact", "compact.zip")
    #1
    steamEnhanced = skin("http://sss.coldnorthadmin.com/skins/enhanced/enhanced.zip", "enhanced", "enhanced.zip")
    #2
    steamAir = skin("http://sss.coldnorthadmin.com/skins/air/air.zip", "air", "air.zip")

    skin_list.append(steamCompact)
    skin_list.append(steamEnhanced)
    skin_list.append(steamAir)


def prompt_skin_choice():

    global skin_id
    skin_id = StringVar()

    try:
        skin_id = int(skin_id.get())
    except ValueError:
        pass

    # while True:
    #     try:
    #         print("1: Steam Compact\n2: Steam Enhanced\n3: Steam Air")
    #         skin_id = int(raw_input("Please enter the skin number : "))
    #     except ValueError:
    #         print "Your selection is invalid"
    #         continue
    #     else:
    #         print("Downloading skin ID : %s") % skin_id
    #         break
    #
    # return skin_id

def gui():
    main_window_root = Tk()
    main_window_root.title("Steam Skin Swapper - Laurent Dumont")

    main_window = Frame(main_window_root, )
    main_window.grid(column=0, row=0, sticky=(N, W, E, S))
    main_window.columnconfigure(0, weight=1)
    main_window.rowconfigure(0, weight=1)

    id_entry = Entry(main_window, width=7, textvariable="Steam skin ID")
    id_entry.grid(column=2, row=1, sticky=(W, E))
    Button(main_window, text="Select Skin", command=prompt_skin_choice) .grid(column=3, row=3, sticky=W)
    
    main_window.mainloop()
    
    

#Main function
def main():
    gui()

    # create_skin_objets()
    # find_steam_path()
    # prompt_skin_choice()
    # download_skin(skin_list, skin_id)
    # edit_selected_skin(skin_list, skin_id)
    # kill_steam_restart()

#MAIN PROCESS
main()