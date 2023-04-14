import os
import io
import zipfile
import tarfile

def get_files_with_extension_recursive(archive, extension):
    file_paths = []

    if isinstance(archive, str):
        if zipfile.is_zipfile(archive):
            archive_obj = zipfile.ZipFile(archive, 'r')
        elif tarfile.is_tarfile(archive):
            archive_obj = tarfile.open(archive, 'r:*')
        else:
            raise ValueError("Unsupported file format")
    else:
        archive_obj = archive

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            if member.filename.endswith(extension):
                file_paths.append(member.filename)
            elif member.filename.endswith(('.zip', '.tar.gz', '.tar.bz2')):
                with archive_obj.open(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    file_paths.extend(get_files_with_extension_recursive(nested_archive_data, extension))
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            if member.isfile() and member.name.endswith(extension):
                file_paths.append(member.name)
            elif member.isfile() and member.name.endswith(('.zip', '.tar.gz', '.tar.bz2')):
                with archive_obj.extractfile(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    file_paths.extend(get_files_with_extension_recursive(nested_archive_data, extension))
    return file_paths

def main():
    archive = 'path/to/compressed/file.zip'  # 圧縮ファイルのパスを指定
    extension = '.txt'  # 目的の拡張子を指定

    file_paths = get_files_with_extension_recursive(archive, extension)
    print(file_paths)

if __name__ == '__main__':
    main()
