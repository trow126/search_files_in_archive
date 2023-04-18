if isinstance(archive_obj, zipfile.ZipFile):
    for member in archive_obj.infolist():
        full_path = parent_path + '/' + member.filename
        if member.filename.endswith(target_ext):
            file_paths.append(full_path)
        elif not member.is_dir():
            file_data = io.BytesIO(archive_obj.read(member))
            inner_archive = open_archive(file_data, member.filename)
            if inner_archive:
                file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path, file_name=member.filename))
