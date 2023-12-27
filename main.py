import requests
import os
import zipfile
import shutil
import msvcrt

lethal_directory = 'C:/Program Files (x86)/Steam/steamapps/common/Lethal Company/' # Lethal Company Directory
files_to_delete = ['winhttp.dll', 'doorstop_config.ini']  # List of files to delete from Lethal directory
BepInEx_Directory = lethal_directory + 'BepInEx'
confirm_message = []
source_directory = os.path.dirname(os.path.abspath(__file__))
source_directory = source_directory.replace("\\", "/")
print("Where am I? " + source_directory + '\n')

def cleanup (newzip, bepfolder, files):
    print('')
    if os.path.exists(newzip): 
        os.remove(newzip)  
        print(newzip + ' cleaned')
    else:
        print("Error: {newzip} doesn't exist: TELL BRANDON")

    for file_name in files:
        final_path = source_directory + '/' + file_name
        if os.path.exists(final_path):  # Checks if path to folder exists
            os.remove(final_path)  # Remove the file
            print(final_path + ' cleaned')
        else:
            print("Error: {final_path} doesn't exist: TELL BRANDON")
    if os.path.exists(bepfolder):  # Delete Old BepInEx
        shutil.rmtree(bepfolder)
        print(bepfolder + " cleaned")
    else:
        print("Error: {bepfolder} doesn't exist: TELL BRANDON")
    
def rmfiles_MAINDIRECTORY (files):
    print("Removing Old Files:")
    for file_name in files:
        final_path = lethal_directory + file_name
        if os.path.exists(final_path):  # Checks if path to folder exists
            os.remove(final_path)  # Remove the file
            confirm_message.append(final_path + ' deleted')
        else:
            confirm_message.append(final_path + " doesn't exist")

def rmfolder_MAINDIRECTORY (folder):
    if os.path.exists(folder):  # Delete Old BepInEx
        shutil.rmtree(folder)
        confirm_message.append(folder + " deleted")
    else:
        confirm_message.append(folder + " doesn't exist")

rmfiles_MAINDIRECTORY(files_to_delete)
rmfolder_MAINDIRECTORY(BepInEx_Directory)

for text in confirm_message:
    print(text)

#Download Dropbox Link as .Zip
def download_dropbox_folder(dropbox_link, destination):

    # Fetch folder contents from the Dropbox link
    response = requests.get(dropbox_link)
    
    # Check if request was successful
    if response.status_code == 200:
        # Create a directory to store downloaded files
        os.makedirs(destination, exist_ok=True)
        
        # Save the fetched content as a file
        with open(os.path.join(destination, 'dbox.zip'), 'wb') as file:
            file.write(response.content)
        
        print("\nMods Folder Downloaded!")
    else:
        print("Failed to download the folder. Please yell at Brandon")

def extract_zip(file_path):
    # Check if the file exists and it is a ZIP file
    if os.path.exists(file_path) and file_path.lower().endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(file_path))
        print(f"Extracted {file_path} ...\n")
    else:
        print(f"{file_path} either does not exist or is not a ZIP file.")

dropbox_link = 'https://www.dropbox.com/scl/fi/z7okd48fxs8pc59apsa8c/Mods.zip?rlkey=a17k1677geu0cneka731y5i66&dl=1'
download_dropbox_folder(dropbox_link, source_directory)

zip_file_path = source_directory + "/dbox.zip"
extract_zip(zip_file_path)

try:
    shutil.copytree(source_directory + '/BepInEx', lethal_directory + 'BepInEx')
    print("Mods Folder Copied")
    shutil.copy(source_directory + '/winhttp.dll', lethal_directory)
    shutil.copy(source_directory + '/doorstop_config.ini', lethal_directory)
    print("Essential Files Copied")
except shutil.Error as e:
    print(f"Error: {e}")

cleanup(source_directory + '/dbox.zip', source_directory + '/BepInEx', files_to_delete )
print("\nSuccess! -Love Brandon")
print("\nPress any key to exit...")
msvcrt.getch()
