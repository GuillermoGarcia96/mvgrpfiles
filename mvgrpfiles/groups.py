import grp
import os
import pwd

TOP_DIRECTORY = os.getenv("MVGRPFILES_TOP_DIRECTORY", default="/")

def groups_share_members(group1: str, group2:str) -> bool:

    group_info1 = grp.getgrnam(group1)
    users1 = set(group_info1.gr_mem)

    group_info2 = grp.getgrnam(group2)
    users2 = set(group_info2.gr_mem)

    return not users1.isdisjoint(users2)


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