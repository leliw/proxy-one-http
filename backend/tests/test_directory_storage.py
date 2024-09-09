import unittest
import sys
import logging

project_path = '/'.join(__file__.split('/')[:-2])
sys.path.append(project_path)
logging.basicConfig(level=logging.INFO)

from storage.directory_storage import DirectoryStorage


DIR_KEY = 'dir/key'
DIR_1_KEY = 'dir/1/key'
DIR_2_KEY = 'dir/2/key'

class TestDirectoryStorage(unittest.TestCase):

    def setUp(self):
        self.storage = DirectoryStorage("test/tmp")

    def test_dir(self):        
        self.storage.put(DIR_KEY, 'value')
        self.assertEqual(self.storage.get(DIR_KEY), 'value')
        self.storage.delete(DIR_KEY)
        self.assertIsNone(self.storage.get(DIR_KEY))

    def test_dirs(self):        
        self.storage.put(DIR_1_KEY, 'value1')
        self.storage.put(DIR_2_KEY, 'value2')
        self.assertEqual(self.storage.get(DIR_1_KEY), 'value1')
        self.assertEqual(self.storage.get(DIR_2_KEY), 'value2')
        tree = self.storage.get_directory_tree()
        self.assertEqual("dir", tree[0]["name"])
        self.assertEqual(2, len(tree[0]["children"]))
        print(self.storage.get_directory_tree())
        self.storage.delete(DIR_1_KEY)
        self.storage.delete(DIR_2_KEY)
        self.assertIsNone(self.storage.get(DIR_1_KEY))


if __name__ == '__main__':
    unittest.main()