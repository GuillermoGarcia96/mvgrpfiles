import os
import grp


def validate_input(input_parameters: list[str]) -> None:

    # Check the program was given exactly 1 parameter
    if len(input_parameters) != 2:
        raise Exception()

    if not group_name_exists(input_parameters[1]):
        raise Exception()

    return


def group_name_exists(group_name: str) -> bool:

    # Check if group exists
    group_names: list[str] = []
    for group in grp.getgrall():
        group_names.append(group.gr_name)

    return group_name in group_names


def validate_program_not_running(group_name: str, locked_groups: list[str]) -> bool:

    # Exit if program running for the same group
    if group_name in locked_groups:
        print('This program is already running!')
        raise Exception()

    # Check if the group shares users with those in running programs
    for locked_group in locked_groups:
        if groups_share_members(group_name, locked_group):
            print('A group sharing members with %s is currently being archived.', group_name)
            raise Exception()

    return


def groups_share_members(group1: str, group2:str) -> bool:

    group_info1 = grp.getgrnam(group1)
    users1 = set(group_info1.gr_mem)

    group_info2 = grp.getgrnam(group2)
    users2 = set(group_info2.gr_mem)

    return not users1.isdisjoint(users2)


