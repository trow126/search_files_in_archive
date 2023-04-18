import io
import os
import pandas as pd
import zipfile
import tarfile
import gzip
import bz2
import datetime
from collections import deque

def open_archive(path):
    try:
        return zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        pass

    try:
        return tarfile.open(path)
    except tarfile.ReadError:
        pass

    try:
        if path.endswith('.gz'):
            return gzip.open(path)
    except OSError:
        pass

    try:
        if path.endswith('.bz2'):
            return bz2.open(path)
    except OSError:
        pass

    return None

def search_files_in_archive(path, target_ext, parent_path=''):
    file_paths = []
    paths_to_process = deque([(path, parent_path)])

    while paths_to_process:
        current_path, current_parent_path = paths_to_process.popleft()

        if os.path.isfile(current_path):
            if current_path.endswith(target_ext):
                file_paths.append(current_parent_path + '/' + os.path.basename(current_path))

            archive_obj = open_archive(current_path)

            if isinstance(archive_obj, zipfile.ZipFile):
                for member in archive_obj.namelist():
                    full_path = current_parent_path + '/' + member
                    if member.endswith(target_ext):
                        file_paths.append(full_path)

            elif isinstance(archive_obj, tarfile.TarFile):
                for member in archive_obj.getnames():
                    full_path = current_parent_path + '/' + member
                    if member.endswith(target_ext):
                        file_paths.append(full_path)

            elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
                file_data = io.BytesIO(archive_obj.read())
                inner_archive = open_archive(file_data)
                if inner_archive:
                    file_paths.extend(search_files_in_archive(inner_archive, target_ext, parent_path))

        elif os.path.isdir(current_path):
            with os.scandir(current_path) as entries:
                for entry in entries:
                    entry_path = os.path.join(current_path, entry.name)
                    new_parent_path = current_parent_path + '/' + entry.name
                    paths_to_process.append((entry_path, new_parent_path))

    return file_paths

def main():
    path = 'path/to/compressed/or/directory'  # 圧縮ファイルまたはディレクトリのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    file_paths = search_files_in_archive(path, extension)

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f'{now}_file_paths.txt', 'w') as f:
        f.write('\n'.join(file_paths))

    for file_path in file_paths:
        print("Found file:", file_path)

if __name__ == '__main__':
    main()
