import os
import tempfile
import unittest

from mvgrpfiles.fs_interface import *

class TestCreateLock(unittest.TestCase):
    def test_create_lock(self):
        # Test that create_lock creates a lock file
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = os.path.join(tmpdir, 'lock')
            create_lock(lock_path)
            self.assertTrue(os.path.exists(lock_path))

    def test_overwrite_lock(self):
        # Test that create_lock overwrites an existing lock file
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = os.path.join(tmpdir, 'lock')
            with open(lock_path, 'w'):
                pass
            create_lock(lock_path)
            self.assertTrue(os.path.exists(lock_path))

    def test_invalid_lock_path(self):
        # Test that create_lock raises an OSError for an invalid lock path
        with self.assertRaises(OSError):
            create_lock('/invalid/lock/path')

class TestRemoveLock(unittest.TestCase):
    def test_remove_lock(self):
        # Test that remove_lock removes a lock file
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = os.path.join(tmpdir, 'lock')
            with open(lock_path, 'w'):
                pass
            remove_lock(lock_path)
            self.assertFalse(os.path.exists(lock_path))

    def test_remove_nonexistent_lock(self):
        # Test that remove_lock raises an OSError for a nonexistent lock file
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = os.path.join(tmpdir, 'lock')
            with self.assertRaises(OSError):
                remove_lock(lock_path)

    def test_invalid_lock_path(self):
        # Test that remove_lock raises an OSError for an invalid lock path
        with self.assertRaises(OSError):
            remove_lock('/invalid/lock/path')

class TestGetLockedGroups(unittest.TestCase):
    def test_get_locked_groups(self):
        # Test that get_locked_groups returns a list of locked groups
        with tempfile.TemporaryDirectory() as tmpdir:
            locks_path = os.path.join(tmpdir, 'locks')
            os.mkdir(locks_path)
            with open(os.path.join(locks_path, 'group1.lock'), 'w'):
                pass
            with open(os.path.join(locks_path, 'group2.lock'), 'w'):
                pass
            locked_groups = get_locked_groups(locks_path)
            locked_groups.sort()
            self.assertEqual(locked_groups, ['group1', 'group2'])

    def test_empty_locks_path(self):
        # Test that get_locked_groups returns an empty list for an empty locks path
        with tempfile.TemporaryDirectory() as tmpdir:
            locks_path = os.path.join(tmpdir, 'locks')
            os.mkdir(locks_path)
            locked_groups = get_locked_groups(locks_path)
            self.assertEqual(locked_groups, [])

    def test_nonexistent_locks_path(self):
        # Test that get_locked_groups raises an OSError for a nonexistent locks path
        with self.assertRaises(OSError):
            get_locked_groups('/nonexistent/locks/path')


if __name__ == '__main__':
    unittest.main()
