from unittest import mock
from io import StringIO
import sys
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


class Test_get_args(unittest.TestCase):

    def setUp(self):
        self.stderr = mock.patch("sys.stderr", new_callable=StringIO).start()

        self.addCleanup(mock.patch.stopall)

    def test_no_args(self):
        # Technically we mean no args other than the program name.
        with mock.patch("sys.argv", ["pine"]):
            self.assertRaises(SystemExit, _pine.get_args)
            self.assertIn("the following arguments are required: -c/--config",
                          self.stderr.getvalue())

    def _test_get_args(self, arg, name, value, *names):
        config_path = "config.yaml"

        for config_arg in ("-c", "--config"):
            with self.subTest(config_arg=config_arg):
                args = ["pine", config_arg, config_path]
                if arg and value:
                    args.extend([arg, value])
                if names:
                    args.extend(names)

                with mock.patch("sys.argv", args):
                    rslt = _pine.get_args()
                    self.assertEqual(rslt.config_path, config_path)
                    if name:
                        self.assertEqual(getattr(rslt, name), value)
                    if names:
                        self.assertSequenceEqual(rslt.test_names, names)

    def test_defaults_only(self):
        self._test_get_args(None, None, None)

    def test_output_path(self):
        for arg in ("-o", "--output"):
            with self.subTest(arg=arg):
                self._test_get_args(arg, "output_path", "some_output.json")

    def test_run_id(self):
        for arg in ("-i", "--id"):
            with self.subTest(arg=arg):
                self._test_get_args(arg, "run_id", "123456789")

    def test_names(self):
        self._test_get_args(None, None, None, "lol", "rofl", "lmao")
