import os
import unittest
import shutil

from mvgrpfiles.validators import *

class TestValidators(unittest.TestCase):
    def test_group_name_exists(self):
        # Test group that exists
        assert group_name_exists('root')

        # Test group that does not exist
        assert not group_name_exists('fake_group')

    def test_groups_share_members(self):
        # Test groups with no shared members
        assert not groups_share_members('group1', 'group2')

        # Test groups with shared members
        assert groups_share_members('group1', 'group4')

    def test_validate_directories_exist(self):
        # Create a temporary directory for testing
        temp_dir = 'temp'
        os.makedirs(temp_dir, mode=0o766)

        # Test directories that do not exist
        validate_directories_exist([temp_dir + '/dir1', temp_dir + '/dir2', temp_dir + '/dir3'])
        assert os.path.exists(temp_dir + '/dir1')
        assert os.path.exists(temp_dir + '/dir2')
        assert os.path.exists(temp_dir + '/dir3')

        # Test directories that already exist
        validate_directories_exist([temp_dir + '/dir1', temp_dir + '/dir2', temp_dir + '/dir3'])
        assert os.path.exists(temp_dir + '/dir1')
        assert os.path.exists(temp_dir + '/dir2')
        assert os.path.exists(temp_dir + '/dir3')

        # Clean up
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
