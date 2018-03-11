import unittest

import _pine


class Test_make_test_name(unittest.TestCase):

    def test_names(self):
        for path in ("/etc/pine/test.yaml",
                     "../conf/test.yaml",
                     "test.yaml",
                     "test"):
            with self.subTest(path=path):
                self.assertEqual(_pine.make_test_name(path), "test")
