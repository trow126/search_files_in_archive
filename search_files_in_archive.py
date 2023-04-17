def search_files_in_archive(archive_obj, extension, current_path=''):
    ...
    for member in archive_obj.getmembers():
        ...
        elif member.name.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2', '.tar.gz.bz2')):
            with archive_obj.extractfile(member) as nested_archive:
                nested_archive_data = io.BytesIO(nested_archive.read())
                if hasattr(nested_archive, 'name'):
                    nested_archive_name = nested_archive.name
                else:
                    nested_archive_name = member.name
                nested_archive_obj = open_archive(nested_archive_data, nested_archive_name)
                if nested_archive_obj:
                    file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))
        ...
