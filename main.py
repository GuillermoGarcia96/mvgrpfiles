import sys
import grp
import os
import pwd

# TODO: logging
# TODO: handle exceptions
# TODO: check process already running

TOP_DIRECTORY = os.getenv("MVGRPFILES_TOP_DIRECTORY", default="/")

def group_name_exists(group_name: str) -> bool:
    group_names = []
    for group in grp.getgrall():
        group_names.append(group.gr_name)
    return group_name in group_names


def get_files_from_all_group_members(group_name: str) -> dict[str, str]:

    # Find all users in the group
    group_info = grp.getgrnam(group_name)
    users = group_info.gr_mem

    group_files_by_user = {}
    for user in users:
        group_files_by_user[user] = get_files_owned_by_user(TOP_DIRECTORY, user)

    # Find all files belonging to those users
    # file_names = []
    # files_without_permission = []
    # for user in users:
    #     for root, dirs, files in os.walk('/home/ermo'):
    #         for file in files:
    #             file_path = os.path.join(root, file)

    #             try:
    #                 file_stat = os.stat(file_path)
    #             except PermissionError:
    #                 files_without_permission.append(file_path)
    #             except FileNotFoundError:
    #                 # print(FileNotFoundError)
    #                 pass

    #             if file_stat.st_uid == pwd.getpwnam(user).pw_uid:
    #                 file_names.append(file_path)

    return group_files_by_user


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


if __name__ == "__main__":

    if len(sys.argv) != 2:
        # Handle exception
        raise Exception()

    group_name = sys.argv[1]

    # Validating user input
    if not group_name_exists(group_name):
        raise Exception()

    group_files_by_user = get_files_from_all_group_members(group_name)

    # print(files_without_permission)
    print(group_files_by_user)
    for i in group_files_by_user.values():
        print(len(i))