import io
import os
import pandas as pd
import zipfile
import tarfile
import gzip
import bz2


def open_archive(file_data, file_name=None):
    # (中略) この部分は変更されていません


def search_files_in_archive(path, target_ext, parent_path=''):
    file_paths = []

    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                file_paths.extend(search_files_in_archive(item_path, target_ext, item_path))
            else:
                with open(item_path, 'rb') as file_data:
                    archive_obj = open_archive(file_data, item)
                    if archive_obj:
                        file_paths.extend(search_files_in_archive(archive_obj, target_ext, item_path))
                    elif item_path.endswith(target_ext):
                        file_paths.append(item_path)
    else:
        with open(path, 'rb') as file_data:
            archive_obj = open_archive(file_data, path)
            if archive_obj:
                file_paths.extend(search_files_in_archive(archive_obj, target_ext, parent_path))
            elif path.endswith(target_ext):
                file_paths.append(path)

    return file_paths


def main():
    path = 'path/to/compressed/file.zip'  # 圧縮ファイルまたはフォルダのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    file_paths = search_files_in_archive(path, extension)
    for path in file_paths:
        print("Found file:", path)


if __name__ == '__main__':
    main()
