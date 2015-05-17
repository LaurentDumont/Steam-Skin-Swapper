import os
import psutil
import win32security
#import urllib2
#import requests
import zipfile
import getpass
from _winreg import *

SKIN_PATH = os.getenv('APPDATA')
STEAM_PROC_NAME = "Steam.exe"


#Create a skin object with @skin_url and @skin_name
class skin:
    def __init__(self, skin_url, skin_name, skin_archive_name):
        self.skin_url = skin_url
        self.skin_name = skin_name
        self.skin_archive_name = skin_archive_name

#Download the skin @skin_array
def download_skin(skins_array):

    for skin in skins_array:
        print "Downloading Skin "+skin.skin_name
        urllib.urlretrieve(skin.skin_url, skin.skin_name)

        with zipfile.ZipFile(skin.skin_name, "r") as skin_archive :
            if not os.path.exists(SKIN_PATH+"\\"+"SteamSkins"+"\\"+skin.skin_name):
                    os.makedirs(SKIN_PATH+"\\"+"SteamSkins"+"\\"+skin.skin_name)
            skin_archive.extractall(SKIN_PATH+"\\"+"SteamSkins"+"\\"+skin.skin_name)

def find_steam_path():

    w7_path = "C:\\Program Files (x86)\\Steam\\skins"
    xp_path = "C:\\Program Files\\Steam\skins"
    global win_ver

    if os.path.exists(w7_path):
        win_ver='w7'

    if os.path.exists(xp_path):
        win_ver='xp'

def edit_selected_skin():

    user_name = getpass.getuser()
    sid = win32security.LookupAccountName(None, user_name)[0]
    sidstr = win32security.ConvertSidToStringSid(sid)


    connectRegistry = ConnectRegistry(None, HKEY_USERS)
    skin_key = OpenKey(connectRegistry,sidstr+"\Software\Valve\Steam", 0 , KEY_WRITE)
    try:
        SetValueEx(skin_key, 'SkinV4', 0, REG_SZ, "air")
    except EnvironmentError:
        print "Cannot change Registry key"

    CloseKey(connectRegistry)
    CloseKey(skin_key)


def kill_steam():

    for process in psutil.process_iter():
        try:
            if process.name() == STEAM_PROC_NAME:
                try:
                    process.kill()
                except (os.Error):
                    print ('Cannot kill the Steam process. Please restart Steam manually')
        except (psutil.AccessDenied):

   # try:
    #     os.system("taskkill /im"+STEAM_PROC_NAME+"/f")
    # except: (os.Error)
    #pythons_psutil = []

    #for p in psutil.process_iter():
    #    pythons_psutil.append(p)
    #for x in pythons_psutil:
    #    print

    #os.system('taskkill /f /im Steam.exe')
    # #for proc in psutil.process_iter():
    #     #if proc.name == STEAM_PROC_NAME:
    #         proc.kill()


    #for proc in psutil.process_iter():
        #if proc.as_dict(attrs=['name']) == STEAM_PROC_NAME:
        #if proc.name == STEAM_PROC_NAME:
            #print 'MATCH FOUND'

            #os.system("taskkill /im"+STEAM_PROC_NAME+"/f")

def create_skin_objets():
        global steamCompact,steamEnhanced,steamAir
        globva
        steamCompact = skin("http://sss.coldnorthadmin.com/skins/compact/SteamCompact_1.5.27.zip", "compact", "compact.zip")
        steamEnhanced = skin("http://sss.coldnorthadmin.com/skins/enhanced/enhanced.zip", "enhanced", "enhanced.zip")
        steamAir = skin("http://sss.coldnorthadmin.com/skins/enhanced/air.zip", "air", "air.zip")

def main():
         edit_selected_skin()
         kill_steam()



main()