import io
import os
import pandas as pd
import zipfile
import tarfile
import gzip
import bz2

# (open_archive 関数は変更なし)

def search_files_in_archive(path, target_ext, parent_path=''):
    file_paths = []

    if os.path.isfile(path):
        archive_obj = open_archive(path)
        if archive_obj:
            if isinstance(archive_obj, zipfile.ZipFile):
                for member in archive_obj.infolist():
                    full_path = parent_path + '/' + member.filename
                    if member.filename.endswith(target_ext):
                        file_paths.append(full_path)
                    elif not member.is_dir():
                        with archive_obj.open(member) as file_data:
                            inner_archive = open_archive(file_data, member.filename)
                            if inner_archive:
                                file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path))
            elif isinstance(archive_obj, tarfile.TarFile):
                for member in archive_obj.getmembers():
                    full_path = parent_path + '/' + member.name
                    if member.name.endswith(target_ext):
                        file_paths.append(full_path)
                        file_data = archive_obj.extractfile(member)
                    elif not member.isdir():
                        file_data = archive_obj.extractfile(member)
                        if file_data:
                            inner_archive = open_archive(file_data, member.name)
                            if inner_archive:
                                file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path))
            elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
                file_data = io.BytesIO(archive_obj.read())
                inner_archive = open_archive(file_data)
                if inner_archive:
                    file_paths.extend(search_files_in_archive(inner_archive, target_ext, parent_path))

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.extend(search_files_in_archive(file_path, target_ext))

    return file_paths

def main():
    path = 'path/to/compressed/file_or_folder'  # 圧縮ファイルまたはフォルダのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    file_paths = search_files_in_archive(path, extension)
    for file_path in file_paths:
        print("Found file:", file_path)

if __name__ == '__main__':
    main()
