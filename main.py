import sys
import grp
import os
import pwd
import time
import tarfile

# TODO: logging
# TODO: handle exceptions
# TODO: check process already running

TOP_DIRECTORY = os.getenv("MVGRPFILES_TOP_DIRECTORY", default="/")
ARCHIVE_LOCATION = os.getenv("MVGRPFILES_ARCHIVE_LOCATION", default="./archive/")

def group_name_exists(group_name: str) -> bool:

    # Check if group exists
    group_names: list[str] = []
    for group in grp.getgrall():
        group_names.append(group.gr_name)

    return group_name in group_names


def get_files_from_all_group_members(group_name: str) -> list[str]:

    # Get all users in the group
    group_info = grp.getgrnam(group_name)
    users = group_info.gr_mem

    # Get all files from all group members
    group_files = []
    for user in users:
        group_files += get_files_owned_by_user(TOP_DIRECTORY, user)

    return group_files


def get_files_owned_by_user(directory: str, user: str) -> list[str]:
    # Get the user's UID
    uid = pwd.getpwnam(user).pw_uid

    # Get files owned by the user inside the directory
    file_names = []
    try:
        with os.scandir(directory) as iterable:
            for entry in iterable:

                if entry.is_file() and os.stat(entry.path, follow_symlinks=False).st_uid == uid:
                    file_names.append(entry.path)

                elif entry.is_dir() and not entry.is_symlink():
                    # Recursively check the subdirectory
                    file_names += get_files_owned_by_user(entry.path, user)
    except PermissionError:
        # TODO: handle this case
        pass

    return file_names


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

    return


def remove_files(file_list: list[str]) -> None:

    # Remove archived files
    for file in file_list:
        try:
            os.remove(file)
        except Exception:
            pass

    return


if __name__ == "__main__":

    if len(sys.argv) != 2:
        # Handle exception
        raise Exception()

    group_name = sys.argv[1]

    # Validating user input
    if not group_name_exists(group_name):
        raise Exception()

    group_files = get_files_from_all_group_members(group_name)

    print(group_files)
    print(len(group_files))

    archive_path = ARCHIVE_LOCATION + group_name + "_" + str(time.time()) + ".tar"

    archive_files(group_files, archive_path)

    remove_files(group_files)
