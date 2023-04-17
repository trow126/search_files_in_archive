import zipfile
import tarfile
import gzip
import bz2
import io

def open_archive(file_data):
    try:
        archive_obj = zipfile.ZipFile(file_data)
        print("Opened as ZIP")
        return archive_obj
    except zipfile.BadZipFile:
        pass

    file_data.seek(0)
    try:
        archive_obj = tarfile.open(fileobj=file_data)
        print("Opened as TAR")
        return archive_obj
    except tarfile.ReadError:
        pass

    file_data.seek(0)
    try:
        archive_obj = gzip.GzipFile(fileobj=file_data)
        print("Opened as GZ")
        return archive_obj
    except OSError:
        pass

    file_data.seek(0)
    try:
        archive_obj = bz2.BZ2File(file_data)
        print("Opened as BZ2")
        return archive_obj
    except OSError:
        pass

    return None
