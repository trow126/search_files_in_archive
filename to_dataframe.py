def search_files_in_archive(archive_obj, target_ext, parent_path=''):
    file_paths = []
    dataframes = defaultdict(pd.DataFrame)  # カラム数ごとにDataFrameをまとめる辞書

    def process_dataframe(data):
        dataframe = pd.read_csv(io.StringIO(data), header=None)
        num_columns = len(dataframe.columns)
        dataframes[num_columns] = dataframes[num_columns].append(dataframe, ignore_index=True)

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            full_path = parent_path + '/' + member.filename
            if member.filename.endswith(target_ext):
                file_paths.append(full_path)
                with archive_obj.open(member) as file_data:
                    data = file_data.read().decode()
                    process_dataframe(data)
            elif not member.is_dir():
                with archive_obj.open(member) as file_data:
                    inner_archive = open_archive(file_data, member.filename)
                    if inner_archive:
                        inner_file_paths, inner_dataframes = search_files_in_archive(inner_archive, target_ext, full_path)
                        file_paths.extend(inner_file_paths)
                        for num_columns, inner_dataframe in inner_dataframes.items():
                            dataframes[num_columns] = dataframes[num_columns].append(inner_dataframe, ignore_index=True)
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            full_path = parent_path + '/' + member.name
            if member.name.endswith(target_ext):
                file_paths.append(full_path)
                file_data = archive_obj.extractfile(member)
                if file_data:
                    data = file_data.read().decode()
                    process_dataframe(data)
            elif not member.isdir():
                file_data = archive_obj.extractfile(member)
                if file_data:
                    inner_archive = open_archive(file_data, member.name)
                    if inner_archive:
                        inner_file_paths, inner_dataframes = search_files_in_archive(inner_archive, target_ext, full_path)
                        file_paths.extend(inner_file_paths)
                        for num_columns, inner_dataframe in inner_dataframes.items():
                            dataframes[num_columns] = dataframes[num_columns].append(inner_dataframe, ignore_index=True)
    elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        file_data = io.BytesIO(archive_obj.read())
        inner_archive = open_archive(file_data)
        if inner_archive:
            inner_file_paths, inner_dataframes = search_files_in_archive(inner_archive, target_ext, parent_path)
            file_paths.extend(inner_file_paths)
            for num_columns, inner_dataframe in inner_dataframes.items():
                dataframes[num_columns] = dataframes[num_columns].append(inner_dataframe, ignore_index=True)

    return file_paths, dataframes




