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
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        archive_obj = open_archive(f)
                        if archive_obj:
                            file_paths.extend(search_files_in_archive(archive_obj, target_ext, file_path))
                        elif file.endswith(target_ext):
                            file_paths.append(file_path)
            return file_paths
        else:
            return []

    # 省略: 圧縮ファイルオブジェクトの処理は変更せず、そのまま使います

    return file_paths
