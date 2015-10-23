__author__ = 'Laurent Dumont'
__name__ = 'Steam Skin Swapper'

#Modules needed in order to run the program
import os
import platform
import psutil
import win32security
import urllib
import zipfile
import getpass
import time
import subprocess
from _winreg import *

#Global variables
SKIN_PATH_XP = os.getenv('APPDATA')
STEAM_PROC_NAME = "Steam.exe"

# Create a skin object with @skin_url and @skin_name
class skin:

    def __init__(self, skin_url, skin_name, skin_archive_name):
        self.skin_url = skin_url
        self.skin_name = skin_name
        self.skin_archive_name = skin_archive_name


#Get the OS type - Continue if on Windows / Exit if Mac or Linux.
def get_os_type():

    osType = platform.system()
    if osType != 'Windows':
        print "This program is currently only compatible with Windows"
        exit()

#Reset the skin selection back to the default ugly Steam skin.
def reset_skin_selection():

    user_name = getpass.getuser()
    sid = win32security.LookupAccountName(None, user_name)[0]
    sidstr = win32security.ConvertSidToStringSid(sid)

    connectRegistry = ConnectRegistry(None, HKEY_USERS)
    skin_key = OpenKey(connectRegistry, sidstr + "\Software\Valve\Steam", 0, KEY_WRITE)
    try:
        SetValueEx(skin_key, 'SkinV4', 0, REG_SZ, "")
    except EnvironmentError:
        print "Cannot change Registry key"

    CloseKey(connectRegistry)
    CloseKey(skin_key)

#Download the skin @skin_array.
def download_skin(skins_array,skin_id):

    if skin_id == 1:
        index = 0
    if skin_id == 2:
        index = 1
    if skin_id == 3:
        index = 2
    if skin_id == 4:
        index = 3

    if find_steam_path() == 'w7':
        SKIN_PATH = "C:\\Program Files (x86)\\Steam\\skins"

    if find_steam_path() == 'xp':
        SKIN_PATH = "C:\\Program Files\\Steam\skins"

    print "Downloading Skin : " + skins_array[index].skin_name
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

#Find the Steam folder path depending on the version of Windows.
def find_steam_path():

    w7_path = "C:\\Program Files (x86)\\Steam\\skins"
    xp_path = "C:\\Program Files\\Steam\skins"
    global win_ver

    if os.path.exists(w7_path):
        win_ver = 'w7'

    if os.path.exists(xp_path):
        win_ver = 'xp'

    return win_ver

#Change the selected skin in the registry.
def edit_selected_skin(skins_array, skin_id):

    if skin_id == 1:
        index = 0
    if skin_id == 2:
        index = 1
    if skin_id == 3:
        index = 2
    if skin_id == 4:
        index = 3

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

#Kill and restart the Steam process.
def kill_steam_restart():


    for process in psutil.process_iter():
        try:
            if process.name() == STEAM_PROC_NAME:
                try:
                    print "Killing the Steam process %s" % str(process.name())
                    print "... Please Wait ... ||| Starting the Steam process ||| ... Please Wait ..."
                    process.kill()
                    time.sleep(2)
                    steam_path = r'"C:\Program Files (x86)\Steam\Steam.exe"'
                    subprocess.Popen(steam_path)
                    exit(1)
                except (psutil.Error):
                    print ('Cannot kill the Steam process. Please restart Steam manually')
        except (psutil.AccessDenied):
            pass
        else:
            continue

    print "WARNING | Steam process is not running | WARNING"
    print "INFO | Starting Steam process| INFO"
    steam_path = r'"C:\Program Files (x86)\Steam\Steam.exe"'
    subprocess.Popen(steam_path)
    exit(1)

#Create the skin objects.
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
    #3
    steamMetro = skin("http://sss.coldnorthadmin.com/skins/metro/metro.zip", "metro", "metro.zip")

    skin_list.append(steamCompact)
    skin_list.append(steamEnhanced)
    skin_list.append(steamAir)
    skin_list.append(steamMetro)

#Create the prompt and check choice selection.
def prompt_skin_choice():

    global skin_id

    while True:
        try:
            print("1: Steam Compact\n2: Steam Enhanced\n3: Steam Air\n4: Steam Metro\n99: Reset default Steam skin")
            skin_id_input = int(raw_input("Please enter the skin number : "))
        except ValueError:
            print "Your selection is invalid"
            continue
        else:
            break

    skin_id = skin_id_input
    if skin_id == 99:
        reset_skin_selection()
        kill_steam_restart()
        exit(1)

#Main function
def main():

     create_skin_objets()
     find_steam_path()
     prompt_skin_choice()
     download_skin(skin_list, skin_id)
     edit_selected_skin(skin_list, skin_id)
     kill_steam_restart()

#MAIN PROCESS
main()