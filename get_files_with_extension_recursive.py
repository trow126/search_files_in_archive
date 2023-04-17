import zipfile
import tarfile
import io
import gzip
import bz2
import os


def open_archive(file_path):
    if file_path.endswith('.zip'):
        return zipfile.ZipFile(file_path)
    elif file_path.endswith('.tar'):
        return tarfile.open(file_path)
    elif file_path.endswith('.tar.gz'):
        return tarfile.open(file_path, mode='r:gz')
    elif file_path.endswith('.tar.bz2'):
        return tarfile.open(file_path, mode='r:bz2')
    elif file_path.endswith('.gz'):
        return gzip.open(file_path)
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path)
    else:
        return None


def search_files_in_archive(archive_obj, extension, current_path=''):
    file_paths = []

    if isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        nested_archive_data = io.BytesIO(archive_obj.read())
        nested_archive_obj = open_archive(nested_archive_data)
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
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path + '/' + name))
            else:
                if isinstance(archive_obj, tarfile.TarFile):
                    with archive_obj.extractfile(member) as nested_folder:
                        if nested_folder:
                            folder_data = io.BytesIO(nested_folder.read())
                            folder_obj = open_archive(folder_data)
                            if folder_obj:
                                file_paths.extend(search_files_in_archive(folder_obj, extension, current_path + '/' + name))

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


if __name__ == '__main__':
    main()
