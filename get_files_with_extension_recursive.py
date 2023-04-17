def open_archive(file_data, file_name=None):
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
        if file_name and file_name.endswith(".gz"):
            print("Opened as GZ")
            return archive_obj
    except OSError:
        pass

    file_data.seek(0)
    try:
        archive_obj = bz2.BZ2File(file_data)
        if file_name and file_name.endswith(".bz2"):
            print("Opened as BZ2")
            return archive_obj
    except OSError:
        pass

    return None



def search_files_in_archive(archive_obj, extension, current_path=''):
    file_paths = []

    if isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        nested_archive_data = io.BytesIO(archive_obj.read())
        nested_archive_obj = open_archive(nested_archive_data, current_path)
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
                            folder_obj = open_archive(folder_data)
                            if folder_obj:
                                file_paths.extend(search_files_in_archive(folder_obj, extension, current_path + '/' + name))

    return file_paths
