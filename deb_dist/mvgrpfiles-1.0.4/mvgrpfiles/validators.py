import os
import grp
import logging


class InvalidArgument(ValueError):
    pass

class ProgramRunning(RuntimeError):
    pass


def validate_input(input_parameters):

    # Check the program was given exactly 1 parameter
    if len(input_parameters) != 2:
        print("Only one valid group name should be introduced as parameter.")
        logging.error("User introduced invalid parameters.")
        raise InvalidArgument()

    if not group_name_exists(input_parameters[1]):
        print("Only one valid group name should be introduced as parameter.")
        logging.error("User introduced invalid parameters.")
        raise InvalidArgument()

    return


def group_name_exists(group_name):

    # Check if group exists
    group_names = []
    for group in grp.getgrall():
        group_names.append(group.gr_name)

    return group_name in group_names


def validate_program_not_running(group_name, locked_groups):

    # Exit if program running for the same group
    if group_name in locked_groups:
        print("This program is already running for group {}.".format(group_name))
        logging.error("Another instance of the program was running for the same group.")
        raise ProgramRunning()

    # Check if the group shares users with those in running programs
    for locked_group in locked_groups:
        if groups_share_members(group_name, locked_group):
            print("A group sharing members with {} is currently being archived.".format(group_name))
            logging.error("Another instance of the program was running for a group with shared members.")
            raise ProgramRunning()

    return


def groups_share_members(group1, group2):

    group_info1 = grp.getgrnam(group1)
    users1 = set(group_info1.gr_mem)

    group_info2 = grp.getgrnam(group2)
    users2 = set(group_info2.gr_mem)

    return not users1.isdisjoint(users2)


def validate_directories_exist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, mode=0o766)
    return
