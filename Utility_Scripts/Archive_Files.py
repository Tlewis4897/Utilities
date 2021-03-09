from datetime import datetime
import shutil
import os
import json
from typing import Any


SCRIPT_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))


def read_json(json_data:str)-> Any:
    """reads a json file and returns the text as a dictionary"""
    try:
        with open(json_data, 'r') as json_file:
            get_json = json.load(json_file)
        return get_json
    except Exception as err:
        return err

config = read_json(os.path.join(CURRENT_DIR, 'config.json'))

directory_path = config["directory_path"]
archive_path = config["archive_path"]


def get_file_date(file: str) -> Any:
    try:
        file_time = os.path.getmtime(file)
    except OSError:
        file_time = 0
    last_modified_date = datetime.fromtimestamp(file_time)
    file_date = datetime.strftime(last_modified_date, '%Y-%m')
    return file_date

file_types = {"new_word": ".docx","old_word":".doc","pdf": ".pdf","ppt_docs":".pptx"}


def archive_docs(directory_path:str, new_folder_path:str) -> None:
    # Loop through dictionary for file types
    for key,vals in file_types.items():
        # Create dictionary if it doesn't exist
        if not os.path.exists(new_folder_path + key):
            os.makedirs(new_folder_path + key) 
        # Search directory for files              
        for root,dirs, files in os.walk(directory_path): 
            for name in files:
                if name.endswith(vals):
                    date_to_archive = datetime.strptime(config['date'],'%m-%Y')
                    to_archive_str = datetime.strftime(date_to_archive, '%Y-%m')
                    if get_file_date(root + '/' + name) < to_archive_str:
                        shutil.copy(root + '/'+ name, new_folder_path + key)
                        os.remove(root + '/' + name)


if __name__ == "__main__":
    try:
        archive_docs(directory_path, archive_path)
    except Exception as e:
        print(e)