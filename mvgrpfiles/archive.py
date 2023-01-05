import tarfile
import os

def archive_files(file_list: list[str], archive_path: str) -> None:

    # Create archive
    with tarfile.open(archive_path, "x") as archive:
        for file in file_list:
            archive.add(file)

    # Move files to archive
    for file in file_list:
        try:
            os.rename(file, os.path.join(archive_path, file))
        except Exception:
            pass

    remove_files(file_list)

    return


def remove_files(file_list: list[str]) -> None:

    # Remove archived files
    for file in file_list:
        try:
            os.remove(file)
        except Exception:
            pass

    return