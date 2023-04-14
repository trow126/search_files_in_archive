import io
import zipfile
import tarfile
import gzip
import bz2

def open_archive(archive):
    if isinstance(archive, io.BytesIO):
        archive.seek(0)
        if zipfile.is_zipfile(archive):
            return zipfile.ZipFile(archive, 'r')
        elif tarfile.is_tarfile(archive):
            return tarfile.open(fileobj=archive, mode='r:*')
        elif gzip._GzipReader(archive).is_gzip():
            return gzip.GzipFile(fileobj=archive)
        elif bz2.BZ2Decompressor().is_valid_stream(archive.getvalue()[:10]):
            return bz2.open(archive)
        else:
            return None
    elif isinstance(archive, str):
        if zipfile.is_zipfile(archive):
            return zipfile.ZipFile(archive, 'r')
        elif tarfile.is_tarfile(archive):
            return tarfile.open(archive, 'r:*')
        elif gzip.open(archive).peek(10).startswith(b'\x1f\x8b\x08'):
            return gzip.open(archive)
        elif bz2.open(archive).peek(10).startswith(b'\x42\x5a\x68'):
            return bz2.open(archive)
        else:
            raise ValueError("Unsupported file format")
    else:
        raise ValueError("Unsupported archive type")


def decompress_gz_bz2(fileobj):
    with bz2.open(fileobj) as bz2_file:
        decompressed_data = bz2_file.read()
        gz_data = io.BytesIO(decompressed_data)
        tar_data = gzip.GzipFile(fileobj=gz_data)
        return tar_data

def search_files_in_archive(archive_obj, extension, parent=""):
    file_paths = []

    if isinstance(archive_obj, zipfile.ZipFile):
        for member in archive_obj.infolist():
            print("Processing ZIP member:", member.filename)
            current_path = f"{parent}/{member.filename}"
            if member.filename.endswith(extension):
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
            if member.isfile() and member.name.endswith(extension):
                file_paths.append(current_path)
            elif member.isfile() and member.name.endswith(('.zip', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.bz2', '.tar.gz.bz2')):
                with archive_obj.extractfile(member) as nested_archive:
                    nested_archive_data = io.BytesIO(nested_archive.read())
                    nested_archive_obj = open_archive(nested_archive_data)
                    if nested_archive_obj:
                        file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))
            elif member.isdir():  # .tar内のディレクトリを処理
                with archive_obj.extractfile(member) as nested_dir:
                    if nested_dir is not None:
                        nested_archive_data = io.BytesIO(nested_dir.read())
                        nested_archive_obj = open_archive(nested_archive_data)
                        if nested_archive_obj:
                            file_paths.extend(search_files_in_archive(nested_archive_obj, extension, current_path))

    elif isinstance(archive_obj, (gzip.GzipFile, bz2.BZ2File)):
        archive_data = archive_obj.read()
        nested_archive_data = io.BytesIO(archive_data)
        nested_archive_obj = open_archive(nested_archive_data)
        if nested_archive_obj:
            file_paths.extend(search_files_in_archive(nested_archive_obj, extension, parent))

    if hasattr(archive_obj, 'close'):
        archive_obj.close()
    return file_paths



def main():
    archive = 'path/to/compressed/file.zip'  # 圧縮ファイルのパスを指定
    extension = '.log'  # 目的の拡張子を指定

    archive_obj = open_archive(archive)
    if archive_obj:
        file_paths = search_files_in_archive(archive_obj, extension)
        print(file_paths)
    else:
        print("Failed to open the archive.")

if __name__ == '__main__':
    main()

