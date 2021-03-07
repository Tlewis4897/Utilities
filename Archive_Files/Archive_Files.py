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
word_document_path = config["word_document_path"]

def get_file_date(file: str):
    try:
        mtime = os.path.getmtime(file)
    except OSError:
        mtime = 0
    last_modified_date = datetime.fromtimestamp(mtime)
    file_date = datetime.strftime(last_modified_date, '%Y-%m')
    print(file_date)
    return file_date

def archive_word_docs(directory_path:str, new_folder_path:str) -> None:
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    # Search directory for JPG's and PNG's                
    for root,dirs, files in os.walk(directory_path): 
        for name in files:
            if name.endswith(".docx") or name.endswith(".doc"):
                date_to_archive = datetime.strptime(config['date'],'%m-%Y')
                to_archive_str = datetime.strftime(date_to_archive, '%Y-%m')
                if get_file_date(root + '/' + name) < to_archive_str:
                    print(name)
                    shutil.copy(root + '/'+ name, new_folder_path)
                    os.remove(root + '/' + name)

archive_word_docs(directory_path, word_document_path)