import grp
import os
import pwd
import tarfile
import logging

# TOP_DIR = os.getenv("MVGRPFILES_TOP_DIR", default="/")
TOP_DIR = "/"

def create_lock(lock_path: str) -> None:
    with open(lock_path, 'w'):
        pass
    return


def remove_lock(lock_path: str) -> None:
    os.remove(lock_path)
    return


def get_locked_groups(locks_path: str):

    # Get the groups with an existing lock file
    lock_files =  os.listdir(locks_path)
    locked_groups = map(lambda x: x.split('.', 1)[0], lock_files)

    return list(locked_groups)


def get_files_from_all_group_members(group_name: str) -> list[str]:

    # Get all users in the group
    group_info = grp.getgrnam(group_name)
    users = group_info.gr_mem

    # Get all files from all group members
    group_files = []
    for user in users:
        user_files = get_files_owned_by_user(TOP_DIR, user)
        group_files += user_files

        logging.info("{} files from user {} archived.".format(len(user_files), user))

    return group_files


def get_files_owned_by_user(directory: str, user: str) -> list[str]:
    # Get the user's UID
    uid = pwd.getpwnam(user).pw_uid

    # Get files owned by the user inside the directory
    full_permissions = True
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
        full_permissions = False
    except FileNotFoundError:
        # Files in /proc sometimes throw this errror
        pass

    if not full_permissions:
        print("You don't have permission for the whole filesystem. Some files could be missing in the archive.")

    return file_names


def archive_files(file_list: list[str], archive_path: str) -> None:

    # Create archive
    with tarfile.open(archive_path, "x") as archive:
        for file in file_list:
            archive.add(file)

    # Move files to archive
    full_permissions = True
    total_archived = len(file_list)
    for file in file_list:
        try:
            os.rename(file, os.path.join(archive_path, file))
            os.remove(file)
        except PermissionError:
            full_permissions = False
        except OSError as e:
            total_archived -= 1
            logging.warning("File {} could not be archived, the following exception was raised:".format(file))
            logging.warning(str(e))
    
    if not full_permissions:
        print("You don't have permission for the whole filesystem. Some files could be missing in the archive.")

    logging.info("{}/{} total files archived in {}.".format(total_archived, len(file_list), archive_path))

    return
