import sys
import grp

# Todo: logging
# Todo: handle exceptions
# Todo: check process already running

def group_name_exists(group_name):
    group_names = []
    for group in grp.getgrall():
        group_names.append(group.gr_name)
    print(group_names)
    return group_name in group_names


def find_files(group_name):

    # Find all users in the group
    group_info = grp.getgrnam(group_name)
    users = group_info.gr_mem

    # Find all files belonging to those users
    file_names = []
    for user in users:
        for root, dirs, files in os.walk('/'):
            for file in files:
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)
                if file_stat.st_uid == pwd.getpwnam(user).pw_uid:
                    file_names.append(file_path)

    return file_names



    return

if __name__ == "__main__":

    if len(sys.argv) != 2:
        # Handle exception
        raise Exception()

    group_name = sys.argv[1]

    if not group_name_exists(group_name):
        raise Exception()

    file_names = find_files(group_name)

    print(file_names)