import os
import tempfile
import unittest

from mvgrpfiles.validators import create_lock

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

if __name__ == '__main__':
    unittest.main()