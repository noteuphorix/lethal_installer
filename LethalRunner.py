import winreg #Used to find lethal directory
import os
import requests #Downloading files
import hashlib #Calculates Hash
import zipfile as zf #Unzips download
import shutil # ez removal of directory
import subprocess
import time
import logging

log_file = os.path.join(os.path.dirname(__file__), 'info.log')
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

scriptdirectory = os.getcwd()
modfolder = os.getcwd() + "/mods.zip"
dbxlink = "https://www.dropbox.com/scl/fi/z7okd48fxs8pc59apsa8c/Mods.zip?rlkey=a17k1677geu0cneka731y5i66&dl=1"


#Locates directory of Lethal Company
def findlethalpath():
    #Opens key containing path to steam
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") 
        path, _ = winreg.QueryValueEx(key, "SteamPath")
        winreg.CloseKey(key)
        path += "/steamapps/common/Lethal Company"
    except Exception as e:
        logging.warn(e)
    logging.info(path)
    return path

#Checks hashes, runs downloadmods if needed
def checkforupdate(link):
    print("Checking for updates...\n")
    request = requests.get(link, allow_redirects=True)
    #Checks if mods.zip already exists, compares hashes if true
    if os.path.exists(modfolder):
            hash = calculatecurrenthash()
            dbxhash = hashlib.md5(request.content).hexdigest()
            if dbxhash == hash:
                 print("No Update Needed!")
                 logging.info(dbxhash)
                 logging.info(hash)
                 return True
    if request.status_code == 200:
        downloadmods(modfolder, request)
        return False     
    else:
         print("Error:" + request.status_code)

#Downloads mods via Dropbox, deletes old
def downloadmods(savepath, request):
    delete()
    with open(savepath, 'wb') as file:
            print("Downloading...")
            file.write(request.content)
            print("Success!\n")
            
#Grabs hash off current mods .zip if it exists
def calculatecurrenthash():
     hash_object = hashlib.new('md5')
     with open(modfolder, 'rb') as file:
          content = file.read()
          hash_object.update(content)
          return hash_object.hexdigest()
     
#Extract .zip
def extract(path, directory):
    with zf.ZipFile(path, 'r') as zip_ref:
        print("Extracting...")
        zip_ref.extractall(directory)
        

#Cleans old files
def delete():
    path = lethalpath
    os.remove(path + "/doorstop_config.ini") if os.path.exists(path + "/doorstop_config.ini") else logging.info("doorstop doesn't exist")
    os.remove(path + "/winhttp.dll") if os.path.exists(path + "/winhttp.dll") else logging.info("winhttp doesn't exist")
    os.remove(modfolder) if os.path.exists(modfolder) else logging.info(".zip doesn't exist")
    shutil.rmtree(path + "/BepInEx") if os.path.exists(path + "/BepInEx") else logging.info("BepInEx doesn't exist")
    print("Old files removed")


def end():
    print("\nCreated With Love By: Euphoria7910 <3")
    print("\nLaunching Lethal Company...")
    subprocess.Popen(lethalpath + "/Lethal Company.exe")
    time.sleep(10)

lethalpath = findlethalpath()
result = checkforupdate(dbxlink)
if result == True: end()
else:
    extract(modfolder, lethalpath)
    print("\nMods Successfully Installed!")
    end()

     


























