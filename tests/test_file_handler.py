from src.helpers import file_handler

import os

from pyfakefs.fake_filesystem_unittest import TestCase


class FileHandler(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @staticmethod
    def test_replace_line():
        result = file_handler.replace_line("Testing 123", "123", "456")
        assert result == "Testing 456"

    def test_remove_tmp_folders(self):
        self.fs.create_dir('/tmp/folder0')
        self.fs.create_dir('/tmp/folder1')
        self.fs.create_dir('/tmp/folder2')
        assert os.path.isdir('tmp/folder0')
        assert os.path.isdir('tmp/folder1')
        assert os.path.isdir('tmp/folder2')
        file_handler.remove_tmp_folders(['folder0', 'folder1', 'folder2'])
        assert not os.path.isdir('tmp/folder0')
        assert not os.path.isdir('tmp/folder1')
        assert not os.path.isdir('tmp/folder2')

    def test_get_files_in_dir(self):
        self.fs.create_file('/tmp/test.scala')
        self.fs.create_file('/tmp/test.sbt')
        self.fs.create_file('/tmp/test.ignored')
        result = file_handler.get_files_in_dir(['sbt', 'scala'], '/tmp/')
        assert "test.scala" in result
        assert "test.sbt" in result
        assert not ("test.ignored" in result)

    def test_find_lines(self):
        self.fs.create_file('/tmp/test.scala', contents='1\n2\n1\n4\n3')
        result = file_handler.find_lines("1", '/tmp/test.scala')
        assert len(result) == 2

