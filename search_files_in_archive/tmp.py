import io
import os
import pandas as pd
import zipfile
import tarfile
import gzip
import bz2

def search_files_in_archive(path, target_ext, parent_path=''):
    def open_archive(file_data, file_name=None):
        # 省略: open_archiveのコードは変更せず、そのままここに移動します

    if isinstance(path, str):  # ファイルパスが渡された場合
        if os.path.isfile(path):  # ファイルが存在する場合
            with open(path, 'rb') as f:
                archive_obj = open_archive(f)
                if archive_obj:
                    return search_files_in_archive(archive_obj, target_ext, parent_path)
                else:
                    return []
        elif os.path.isdir(path):  # ディレクトリが存在する場合
            file_paths = []
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(target_ext):
                        file_paths.append(os.path.join(root, file))
            return file_paths
        else:
            return []

    file_paths = []

    # 省略: search_files_in_archiveのコードは変更せず、そのまま使います

    return file_paths

def main():
    path = 'path/to/compressed/or/directory'  # 圧縮ファイルまたはディレクトリのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    file_paths = search_files_in_archive(path, extension)
    for path in file_paths:
        print("Found file:", path)

if __name__ == '__main__':
    main()
