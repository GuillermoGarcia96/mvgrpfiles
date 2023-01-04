import os
import sys
import time
import logging

from groups import group_name_exists, get_files_from_all_group_members
from archive import archive_files

# TODO: logging
# TODO: handle exceptions
# TODO: check process already running

ARCHIVE_LOCATION = os.getenv("MVGRPFILES_ARCHIVE_LOCATION", default="./archive/")
LOG_LOCATION = os.getenv("MVGRPFILES_LOG_LOCATION", default="./logs/")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        # Handle exception
        raise Exception()

    group_name = sys.argv[1]

    logging.basicConfig(
        filename=LOG_LOCATION + str(time.time()) + "." + group_name + '.log',
        encoding='utf-8',
        level=logging.DEBUG
    )

    logging.info("Looking for files from users in the %s group", group_name)

    # Validating user input
    if not group_name_exists(group_name):
        raise Exception()

    group_files = get_files_from_all_group_members(group_name)

    print(group_files)
    print(len(group_files))

    archive_path = ARCHIVE_LOCATION + group_name + "_" + str(time.time()) + ".tar"

    archive_files(group_files, archive_path)
