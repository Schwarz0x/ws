import json
import os
import requests
import shutil
import figlet
from colorama import init, Fore, Back, Style

init()  # Initialize colorama

def get_local_version():
    with open('qq.json', 'r') as f:
        data = json.load(f)
        return data

def get_remote_version(github_url):
    response = requests.get(github_url + '/qq.json')
    if response.status_code == 200:
        data = response.json()
        return data['version']['text']
    else:
        print("Error:", response.status_code)
        return None

def update_files(local_version, remote_version):
    if remote_version > local_version['version']['text']:
        # Move files to a new folder with the version number
        version_folder = f"v{remote_version}"
        os.mkdir(version_folder)
        for file in os.listdir():
            if file != 'qq.json' and file != version_folder:
                shutil.move(file, os.path.join(version_folder, file))
        
        # Move the version folder to WS_Old
        ws_old_folder = 'WS_Old'
        if not os.path.exists(ws_old_folder):
            os.mkdir(ws_old_folder)
        shutil.move(version_folder, os.path.join(ws_old_folder, version_folder))
        
        # Download and install the latest version
        # (We'll implement this part later)
        print("Updating to version", remote_version)
    else:
        print("You're already running the latest version")

def print_welcome_message(data):
    f = figlet.Figlet(font='slant')
    welcome_message = "Welcome to " + data['project_name']['text']
    color = data['project_name']['color']
    background = data['project_name']['background']
    color2 = data['project_name']['color2']
    background2 = data['project_name']['background2']
    print(f"{Back.{background.upper().replace('#', '')}}{Fore.{color.upper().replace('#', '')}}{f.renderText(welcome_message)}{Style.RESET_ALL}")
    print(f"{Back.{background2.upper().replace('#', '')}}{Fore.{color2.upper().replace('#', '')}}{f.renderText(welcome_message)}{Style.RESET_ALL}")

def print_project_info(data):
    f = figlet.Figlet(font='slant')
    for key, value in data.items():
        if key != 'project_name':
            text = value['text']
            color = value['color']
            background = value['background']
            color2 = value['color2']
            background2 = value['background2']
            print(f"{Back.{background.upper().replace('#', '')}}{Fore.{color.upper().replace('#', '')}}{f.renderText(text)}{Style.RESET_ALL}")
            print(f"{Back.{background2.upper().replace('#', '')}}{Fore.{color2.upper().replace('#', '')}}{f.renderText(text)}{Style.RESET_ALL}")

def main():
    github_url = 'https://github.com/your-username/your-repo-name'
    local_version = get_local_version()
    remote_version = get_remote_version(github_url)
    if remote_version:
        print_welcome_message(local_version)
        print_project_info(local_version)
        update_files(local_version, remote_version)

if __name__ == "__main__":
    main()