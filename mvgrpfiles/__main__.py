import os
import sys
import time
import logging

from mvgrpfiles.groups import groups_share_members, group_name_exists, get_files_from_all_group_members
from mvgrpfiles.archive import archive_files

# TODO: logging
# TODO: handle exceptions
# TODO: check process already running

ARCHIVE_LOCATION = os.getenv("MVGRPFILES_ARCHIVE_LOCATION", default="./archive/")
LOGS_LOCATION = os.getenv("MVGRPFILES_LOGS_LOCATION", default="./logs/")
LOCKS_LOCATION = os.getenv("MVGRPFILES_LOCKS_LOCATION", default="./locks/")

if __name__ == "__main__":

    # Check the program was given 1 parameter
    if len(sys.argv) != 2:
        # Handle exception
        raise Exception()

    group_name = sys.argv[1]

    # Create the lock file path
    lock_file_name = group_name + '.lock'

    # Get the list of files in the directory
    lock_files = os.listdir(LOCKS_LOCATION)

    # Print the list of lock files
    print(lock_files)

    if lock_file_name in lock_files:
        print('This program is already running!')
        sys.exit(1)

    else:
        for lock in lock_files:
            locked_group = lock.split('.', 1)[0]
            if groups_share_members(group_name, locked_group):
                print('Another group sharing members with %s is already being archived.', group_name)
                sys.exit(1)

    # The lock file does not exist, so create it
    lock_file_path = LOCKS_LOCATION + lock_file_name
    pid = os.getpid()
    with open(lock_file_path, 'w') as f:
        f.write(str(pid))

    # Check that the parameter is a valid group name
    if not group_name_exists(group_name):
        raise Exception()

    # Create a log file
    logging.basicConfig(
        filename=LOGS_LOCATION + str(time.time()) + "." + group_name + '.log',
        encoding='utf-8',
        level=logging.DEBUG
    )

    logging.info("Looking for files from users in the %s group", group_name)

    # Get all files from users from the given group
    group_files = get_files_from_all_group_members(group_name)

    print(group_files)
    print(len(group_files))

    # Archives the obtained files
    archive_path = ARCHIVE_LOCATION + group_name + "_" + str(time.time()) + ".tar"

    archive_files(group_files, archive_path)

    os.remove(lock_file_path)
