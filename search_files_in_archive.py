def search_files_in_archive(archive_obj, extension, parent=""):
    file_paths = []

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            print("Processing ZIP member:", member.filename)
            current_path = f"{parent}/{member.filename}"
            if member.filename.endswith(extension):
                print(f"Found target file: {current_path}")
                file_paths.append(current_path)
            elif member.filename.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2', '.tar.gz.bz2')):
                with archive_obj.open(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            print("Processing TAR member:", member.name)
            current_path = f"{parent}/{member.name}"
            if member.name.endswith(extension):
                print(f"Found target file: {current_path}")
                file_paths.append(current_path)
            elif member.name.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2', '.tar.gz.bz2')):
                with archive_obj.extractfile(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))

    return file_paths
