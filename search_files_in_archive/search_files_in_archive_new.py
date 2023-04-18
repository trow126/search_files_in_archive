import os
import io
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


def search_files_in_archive(path_or_data, target_ext, parent_path='', file_name=None):
    file_paths = []

    if isinstance(path_or_data, io.BytesIO):
        file_data = path_or_data
        archive_obj = open_archive(file_data, file_name)
    else:
        if os.path.isfile(path_or_data):
            with open(path_or_data, 'rb') as file_data:
                archive_obj = open_archive(file_data, path_or_data)
        elif os.path.isdir(path_or_data):
            for root, _, files in os.walk(path_or_data):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_paths.extend(search_files_in_archive(file_path, target_ext))
            return file_paths
        else:
            return []

    if archive_obj:
        if isinstance(archive_obj, zipfile.ZipFile):
            for member in archive_obj.infolist():
                full_path = parent_path + '/' + member.filename
                if member.filename.endswith(target_ext):
                    file_paths.append(full_path)
                elif not member.is_dir():
                    file_data = io.BytesIO(archive_obj.read(member))
                    inner_archive = open_archive(file_data, member.filename)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path, file_name=member.filename))
        elif isinstance(archive_obj, tarfile.TarFile):
            for member in archive_obj.getmembers():
                full_path = parent_path + '/' + member.name
                if member.name.endswith(target_ext):
                    file_paths.append(full_path)
                elif not member.isdir():
                    file_data = archive_obj.extractfile(member)
                    if file_data:
                        file_data = io.BytesIO(file_data.read())
                        inner_archive = open_archive(file_data, member.name)
                        if inner_archive:
                            file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path, file_name=member.name))
        elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
            file_data = io.BytesIO(archive_obj.read())
            inner_archive = open_archive(file_data, file_name)
            if inner_archive:
                file_paths.extend(search_files_in_archive(inner_archive, target_ext, parent_path, file_name=file_name))

    return file_paths


def main():
    path = 'path/to/compressed/file.zip'  # 圧縮ファイルのパスまたはフォルダパスを指定
    extension = '.log'  # 目的の拡張子を指定

    file_paths = search_files_in_archive(path, extension)
    for found_path in file_paths:
        print("Found file:", found_path)


