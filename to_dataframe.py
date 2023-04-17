import io
import pandas as pd
from collections import defaultdict

def search_files_in_archive(archive_obj, target_ext, parent_path='', grouped_dataframes=None):
    if grouped_dataframes is None:
        grouped_dataframes = defaultdict(list)

    # 以前のコードと同じ

    if member.name.endswith(target_ext):
        file_paths.append(full_path)
        file_data = archive_obj.extractfile(member)
        if file_data:
            data = file_data.read().decode()
            dataframe = pd.read_csv(io.StringIO(data))
            num_columns = len(dataframe.columns)
            grouped_dataframes[num_columns].append(dataframe)

    # 以前のコードと同じ

    return file_paths, grouped_dataframes

# main関数内
if archive_obj:
    file_paths, grouped_dataframes = search_files_in_archive(archive_obj, extension)
    print("Found files:", len(file_paths))
    print("Grouped DataFrames:")
    for num_columns, dataframes in grouped_dataframes.items():
        combined_dataframe = pd.concat(dataframes, ignore_index=True)
        print(f"Combined DataFrame for {num_columns} columns:")
        print(combined_dataframe)
else:
    print("Failed to open the archive.")
