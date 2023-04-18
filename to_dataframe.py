import io
import pandas as pd

def search_files_in_archive(archive_obj, target_ext, parent_path='', df_dict=None):
    if df_dict is None:
        df_dict = {}

    file_paths = []

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            full_path = parent_path + '/' + member.filename
            if member.filename.endswith(target_ext):
                file_paths.append(full_path)
                with archive_obj.open(member) as file_data:
                    data = file_data.read().decode()
                    dataframe = pd.read_csv(io.StringIO(data), header=None)
                    num_columns = len(dataframe.columns)
                    if num_columns not in df_dict:
                        df_dict[num_columns] = []
                    df_dict[num_columns].append(dataframe)
            elif not member.is_dir():
                with archive_obj.open(member) as file_data:
                    inner_archive = open_archive(file_data, member.filename)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path, df_dict))
    elif isinstance(archive_obj, tarfile.TarFile):
        for member in archive_obj.getmembers():
            full_path = parent_path + '/' + member.name
            if member.name.endswith(target_ext):
                file_paths.append(full_path)
                file_data = archive_obj.extractfile(member)
                if file_data:
                    data = file_data.read().decode()
                    dataframe = pd.read_csv(io.StringIO(data), header=None)
                    num_columns = len(dataframe.columns)
                    if num_columns not in df_dict:
                        df_dict[num_columns] = []
                    df_dict[num_columns].append(dataframe)
            elif not member.isdir():
                file_data = archive_obj.extractfile(member)
                if file_data:
                    inner_archive = open_archive(file_data, member.name)
                    if inner_archive:
                        file_paths.extend(search_files_in_archive(inner_archive, target_ext, full_path, df_dict))
    elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        file_data = io.BytesIO(archive_obj.read())
        inner_archive = open_archive(file_data)
        if inner_archive:
            file_paths.extend(search_files_in_archive(inner_archive, target_ext, parent_path, df_dict))

    return file_paths,df_dict




def main():
    ...
    if archive_obj:
        df_dict = search_files_in_archive(archive_obj, extension)
        
        for num_columns, dataframes in df_dict.items():
            combined_df = pd.concat(dataframes, ignore_index=True)
            print(f"Number of columns: {num_columns}")
            print(combined_df.head())  # 先頭部分のみを表示。全て表示する場合は、`print(combined_df)`に変更。
    ...

