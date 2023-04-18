def search_files_in_archive(path_or_data, target_ext, parent_path='', file_name=None):
    file_paths = []

    if isinstance(path_or_data, io.BytesIO):
        file_data = path_or_data
        archive_obj = open_archive(file_data, file_name)
    else:
        if os.path.isfile(path_or_data):
            with open(path_or_data, 'rb') as file_data:
                archive_obj = open_archive(file_data, path_or_data)
        elif os.path.isdir(path_or_data):
            for root, _, files in os.walk(path_or_data):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_paths.extend(search_files_in_archive(file_path, target_ext))
            return file_paths
        else:
            return []

    if archive_obj:
        # (search_files_in_archive の処理は変更なし)

    return file_paths
