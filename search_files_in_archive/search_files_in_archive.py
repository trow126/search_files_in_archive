import io
import pandas as pd
import zipfile
import tarfile
import gzip
import bz2

def open_archive(file_data, file_name=None):
    try:
        archive_obj = zipfile.ZipFile(file_data)
        return archive_obj
    except zipfile.BadZipFile:
        pass

    file_data.seek(0)
    try:
        archive_obj = tarfile.open(fileobj=file_data)
        return archive_obj
    except tarfile.ReadError:
        pass

    file_data.seek(0)
    try:
        archive_obj = gzip.GzipFile(fileobj=file_data)
        if file_name and file_name.endswith(".gz"):
            return archive_obj
    except OSError:
        pass

    file_data.seek(0)
    try:
        archive_obj = bz2.BZ2File(file_data)
        if file_name and file_name.endswith(".bz2"):
            return archive_obj
    except OSError:
        pass

    return None

def search_files_in_archive(archive_obj, target_ext, parent_path=''):
    file_paths = []

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

    return file_paths

def main():
    archive = 'path/to/compressed/file.zip'  # 圧縮ファイルのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    archive_obj = open_archive(archive)
    if archive_obj:
        file_paths = search_files_in_archive(archive_obj, extension)
        for path in file_paths:
            print("Found file:", path)
    else:
        print("Failed to open the archive.")
