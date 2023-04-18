def search_files_in_archive(path, target_ext, parent_path=''):
    file_paths = []

    if isinstance(path, str):  # ファイルパスが渡された場合
        if os.path.isfile(path):  # ファイルが存在する場合
            with open(path, 'rb') as f:
                archive_obj = open_archive(f)
                if archive_obj:
                    return search_files_in_archive(archive_obj, target_ext, parent_path)
                else:
                    return []
        elif os.path.isdir(path):  # ディレクトリが存在する場合
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(target_ext):
                        file_paths.append(os.path.join(root, file))
            return file_paths
        else:
            return []

    if isinstance(path, zipfile.ZipFile):
        for member in path.infolist():
            full_path = parent_path + '/' + member.filename
            if member.filename.endswith(target_ext):
                file_paths.append(full_path)
            elif not member.is_dir():
                with path.open(member) as file_data:
                    inner_archive = open_archive(file_data, member.filename)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path))
    elif isinstance(path, tarfile.TarFile):
        for member in path.getmembers():
            full_path = parent_path + '/' + member.name
            if member.name.endswith(target_ext):
                file_paths.append(full_path)
            elif not member.isdir():
                file_data = path.extractfile(member)
                if file_data:
                    inner_archive = open_archive(file_data, member.name)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path))
    elif isinstance(path, (gzip.GzipFile, bz2.BZ2File)):
        file_data = io.BytesIO(path.read())
        inner_archive = open_archive(file_data)
        if inner_archive:
            file_paths.extend(search_files_in_archive(inner_archive, target_ext, parent_path))

    return file_paths
