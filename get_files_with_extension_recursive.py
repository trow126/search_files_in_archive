import zipfile
import tarfile
import io
import gzip
import bz2
import os


def open_archive(file_data, filename):
    if filename.endswith('.zip'):
        return zipfile.ZipFile(file_data)
    elif filename.endswith('.tar'):
        return tarfile.open(fileobj=file_data)
    elif filename.endswith('.tar.gz'):
        return tarfile.open(fileobj=file_data, mode='r:gz')
    elif filename.endswith('.tar.bz2'):
        return tarfile.open(fileobj=file_data, mode='r:bz2')
    elif filename.endswith('.gz'):
        return gzip.GzipFile(fileobj=file_data)
    elif filename.endswith('.bz2'):
        return bz2.BZ2File(file_data)
    else:
        return None


def search_files_in_archive(archive_obj, extension, current_path=''):
    file_paths = []

    if isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        nested_archive_data = io.BytesIO(archive_obj.read())
        nested_archive_obj = open_archive(nested_archive_data, archive_obj.name)
        if nested_archive_obj:
            file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))
    else:
        if isinstance(archive_obj, zipfile.ZipFile):
            members = archive_obj.infolist()
        else:
            members = archive_obj.getmembers()

        for member in members:
            if isinstance(archive_obj, zipfile.ZipFile):
                is_file = not member.filename.endswith('/')
                name = member.filename
            else:
                is_file = member.isfile()
                name = member.name

            if is_file:
                if name.endswith(extension):
                    file_paths.append(current_path + '/' + name)
                elif name.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2')):
                    nested_archive_data = io.BytesIO(archive_obj.read(member))
                    nested_archive_obj = open_archive(nested_archive_data, name)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path + '/' + name))
            else:
                if isinstance(archive_obj, tarfile.TarFile):
                    with archive_obj.extractfile(member) as nested_folder:
                        if nested_folder:
                            folder_data = io.BytesIO(nested_folder.read())
                            folder_obj = open_archive(folder_data, name)
                            if folder_obj:
                                file_paths.extend(search_files_in_archive(folder_obj, extension, current_path + '/' + name))

    return file_paths


file_data = open('your_compressed_file', 'rb')  # 圧縮ファイルの名前を指定
archive_obj = open_archive(file_data, 'your_compressed_file')  # 圧縮ファイルの名前を指定
file_paths = search_files_in_archive(archive_obj, '.log')
print(file_paths)
