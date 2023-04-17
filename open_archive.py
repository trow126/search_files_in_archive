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

    return None
