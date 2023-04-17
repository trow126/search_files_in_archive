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
            elif name.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2', '.tar.gz.bz2')):
                with archive_obj.extractfile(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data, name)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path + '/' + name))

    return file_paths
