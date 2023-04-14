import io
import zipfile
import tarfile

def open_archive(archive):
    if isinstance(archive, io.BytesIO):
        archive.seek(0)
        if zipfile.is_zipfile(archive):
            return zipfile.ZipFile(archive, 'r')
        elif tarfile.is_tarfile(archive):
            return tarfile.open(fileobj=archive, mode='r:*')
        else:
            return None
    elif isinstance(archive, str):
        if zipfile.is_zipfile(archive):
            return zipfile.ZipFile(archive, 'r')
        elif tarfile.is_tarfile(archive):
            return tarfile.open(archive, 'r:*')
        else:
            raise ValueError("Unsupported file format")
    else:
        raise ValueError("Unsupported archive type")

def search_files_in_archive(archive_obj, extension):
    file_paths = []

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            if member.filename.endswith(extension):
                file_paths.append(member.filename)
            elif member.filename.endswith(('.zip', '.tar.gz', '.tar.bz2')):
                with archive_obj.open(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension))
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            if member.isfile() and member.name.endswith(extension):
                file_paths.append(member.name)
            elif member.isfile() and member.name.endswith(('.zip', '.tar.gz', '.tar.bz2')):
                with archive_obj.extractfile(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension))
    
    archive_obj.close()
    return file_paths

def main():
    archive = 'path/to/compressed/file.zip'  # 圧縮ファイルのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    archive_obj = open_archive(archive)
    if archive_obj:
        file_paths = search_files_in_archive(archive_obj, extension)
        print(file_paths)
    else:
        print("Failed to open the archive.")

if __name__ == '__main__':
    main()
