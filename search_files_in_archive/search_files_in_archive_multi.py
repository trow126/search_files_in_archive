import io
import os
import zipfile
import tarfile
import gzip
import bz2
import datetime
from multiprocessing import Pool, cpu_count

def process_file(path):
    return search_files_in_archive(path, extension)

def search_files_in_archive(path, target_ext, parent_path=''):
    file_paths = []
    to_process = [path]

    while to_process:
        current_path = to_process.pop()
        if os.path.isdir(current_path):
            with os.scandir(current_path) as entries:
                for entry in entries:
                    if entry.is_file() or entry.is_dir():
                        to_process.append(entry.path)
        else:
            try:
                with open(current_path, 'rb') as file_data:
                    archive_obj = get_archive_obj(file_data)
            except FileNotFoundError:
                archive_obj = None

            if archive_obj:
                for member in get_archive_members(archive_obj):
                    full_path = parent_path + '/' + member.name
                    if member.name.endswith(target_ext):
                        file_paths.append(full_path)
                    else:
                        file_data = archive_obj.extractfile(member)
                        if file_data:
                            inner_archive = get_archive_obj(file_data)
                            if inner_archive:
                                to_process.append(file_data)
            elif current_path.endswith(target_ext):
                file_paths.append(current_path)

    return file_paths

def main():
    global extension
    path = 'path/to/compressed/or/directory'  # 圧縮ファイルまたはディレクトリのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    if os.path.isfile(path):
        file_paths = search_files_in_archive(path, extension)
    elif os.path.isdir(path):
        with os.scandir(path) as entries:
            paths = [entry.path for entry in entries if entry.is_file()]
            with Pool(cpu_count()) as pool:
                file_paths_list = pool.map(process_file, paths)
            file_paths = [file_path for sublist in file_paths_list for file_path in sublist]
    else:
        print("Invalid path.")
        return

    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f'{now}_file_paths.txt', 'w') as f:
        f.write('\n'.join(file_paths))

    for file_path in file_paths:
        print("Found file:", file_path)

if __name__ == '__main__':
    main()
