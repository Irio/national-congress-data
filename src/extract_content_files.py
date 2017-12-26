import glob
import os
import pandas as pd
from shutil import copy, rmtree
from tempfile import mkdtemp
from zipfile import ZipFile

def unzip_and_delete(zip_paths, destination_folder):
    for path in zip_paths:
        zip_file = ZipFile(path, 'r')
        zip_file.extractall(destination_folder)
        zip_file.close()
        os.remove(path)

def zip_filepaths(folder):
    pattern = '{}/*.zip'.format(folder)
    return glob.glob(pattern, recursive=False)


session_files = pd.read_csv('data/sources/sessions.csv')
for _, row in session_files.iterrows():
    file_paths = [file['path'] for file in eval(row.files)]
    temp_folder = mkdtemp()
    for filepath in file_paths:
        copy('data/sources/{}'.format(filepath), temp_folder)

    paths = zip_filepaths(temp_folder)
    while True:
        unzip_and_delete(paths, temp_folder)
        paths = zip_filepaths(temp_folder)
        if not paths:
            break

    pattern = '{}/**.TXT'.format(temp_folder)
    content_files = glob.glob(pattern, recursive=False)
    content_files += glob.glob(pattern.lower(), recursive=False)
    pattern = '{}/**/*.TXT'.format(temp_folder)
    content_files += glob.glob(pattern, recursive=False)
    content_files += glob.glob(pattern.lower(), recursive=False)
    content_files = list(set(content_files))

    import pathlib

    path = 'data/sources/sessions/{}'.format(row['term'])
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    for filepath in content_files:
        filename = filepath.split('/')[-1]
        copy(filepath, '{}/{}'.format(path, filename))
    rmtree(temp_folder)
