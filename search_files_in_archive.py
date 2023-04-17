def search_files_in_archive(archive_obj, target_ext):
    file_paths = []

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            if member.filename.endswith(target_ext):
                file_paths.append(member.filename)
            elif not member.is_dir():
                with archive_obj.open(member) as file_data:
                    inner_archive = open_archive(file_data, member.filename)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext))
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            if member.name.endswith(target_ext):
                file_paths.append(member.name)
            elif not member.isdir():
                file_data = archive_obj.extractfile(member)
                if file_data:
                    inner_archive = open_archive(file_data, member.name)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext))
    elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        file_data = io.BytesIO(archive_obj.read())
        inner_archive = open_archive(file_data)
        if inner_archive:
            file_paths.extend(search_files_in_archive(inner_archive, target_ext))

    return file_paths
