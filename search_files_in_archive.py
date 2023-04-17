def search_files_in_archive(archive_obj, extension, current_path=''):
    file_paths = []
    
    if isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        nested_archive_data = io.BytesIO(archive_obj.read())
        nested_archive_obj = open_archive(nested_archive_data, archive_obj.name)
        if nested_archive_obj:
            file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))
    else:
        for member in archive_obj.getmembers():
            if isinstance(archive_obj, zipfile.ZipFile):
                is_file = member.filename.endswith('/')
            else:
                is_file = member.isfile()
            
            if is_file:
                if member.name.endswith(extension):
                    file_paths.append(current_path + '/' + member.name)
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
    return file_paths
