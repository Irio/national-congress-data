import glob
import os
from shutil import copy, copytree, rmtree
from tempfile import mktemp
from zipfile import ZipFile

def unzip_and_delete(zip_paths, destination_folder):
    for path in zip_paths:
        zip_file = ZipFile(path, 'r')
        zip_file.extractall(destination_folder)
        zip_file.close()
        os.remove(path)

def zip_filepaths(folder):
    pattern = '{}/*.zip'.format(temp_folder)
    return glob.glob(pattern, recursive=False)

temp_folder = '{}/sources'.format(mktemp())
copytree('data/sources/full', temp_folder)

paths = zip_filepaths(temp_folder)
while True:
    unzip_and_delete(paths, temp_folder)
    paths = zip_filepaths(temp_folder)
    if not paths:
        break

pattern = '{}/**.TXT'.format(temp_folder)
content_files = glob.glob(pattern, recursive=False)
content_files += glob.glob(pattern.lower(), recursive=False)

import pathlib

pathlib.Path('data/sessions').mkdir(parents=True, exist_ok=True)

for filepath in content_files:
    filename = filepath.split('/')[-1]
    copy(filepath, 'data/sessions/{}'.format(filename))
rmtree(temp_folder)
