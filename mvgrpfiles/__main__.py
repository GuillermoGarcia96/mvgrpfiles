import os
import sys
import time
import logging

from mvgrpfiles.fs_interface import get_files_from_all_group_members, archive_files, create_lock, remove_lock, get_locked_groups
from mvgrpfiles.validators import validate_input, validate_program_not_running, validate_directories_exist

# TODO: logging
# TODO: handle exceptions
# TODO: setup.py to setup.cfg

ARCHIVE_DIR = os.path.expanduser("~/.mvgrpfiles/archive/")
LOGS_DIR = os.path.expanduser("~/.mvgrpfiles/logs/")
LOCKS_DIR = "/var/tmp/mvgrpfiles/locks/"

print("Starting the program...")

# Safety checks
validate_input(sys.argv)
group_name = sys.argv[1]

validate_directories_exist([ARCHIVE_DIR, LOGS_DIR, LOCKS_DIR])

locked_groups = get_locked_groups(LOCKS_DIR)
validate_program_not_running(group_name, locked_groups)

# Create log file
log_path = os.path.join(LOGS_DIR, str(time.time()) + "." + group_name + '.log')
logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.DEBUG)

# Create lock file
lock_path = os.path.join(LOCKS_DIR, group_name + '.lock')
create_lock(lock_path)

logging.info("Looking for files from users in the %s group", group_name)

# Get and archive files
group_files = get_files_from_all_group_members(group_name)
archive_full_path = os.path.join(ARCHIVE_DIR, group_name + "_" + str(time.time()) + ".tar")
archive_files(group_files, archive_full_path)

# Remove lock file
remove_lock(lock_path)
