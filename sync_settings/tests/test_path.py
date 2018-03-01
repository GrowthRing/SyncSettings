# -*- coding: utf-8 -*-

import unittest
import os
import sys
from ..libs import path

if sys.version_info < (3,):
    import mock
else:
    from unittest import mock


class PathTest(unittest.TestCase):
    def test_encode(self):
        paths = [{
            'case': '/some/path with spaces/to/file.txt',
            'expected': '%2Fsome%2Fpath%20with%20spaces%2Fto%2Ffile.txt',
        }, {
            'case': '_some_ path/f a k e/-to/file._.py',
            'expected': '_some_%20path%2Ff%20a%20k%20e%2F-to%2Ffile._.py'
        }, {
            'case': 'Default (OSX).sublime-keymap',
            'expected': 'Default%20%28OSX%29.sublime-keymap'
        }, {
            'case': 'Shell-Unix-Generic.sublime-settings',
            'expected': 'Shell-Unix-Generic.sublime-settings'
        }, {
            'case': 'Shell-Unix-Generic.sublíme-settings',
            'expected': 'Shell-Unix-Generic.subl%C3%ADme-settings'
        }, {
            'case': 'Shell-шедцвфиле.sublime',
            'expected': 'Shell-%D1%88%D0%B5%D0%B4%D1%86%D0%B2%D1%84%D0%B8%D0%BB%D0%B5.sublime'
        }]

        for p in paths:
            self.assertEqual(path.encode(p['case']), p['expected'])

    def test_decode(self):
        paths = [{
            'case': 'Color%20Highlighter%2Fthemes%2FZeus-Sublime-Text.tmTheme',
            'expected': 'Color Highlighter/themes/Zeus-Sublime-Text.tmTheme'
        }, {
            'case': 'Shell-Unix-Generic.sublime-settings',
            'expected': 'Shell-Unix-Generic.sublime-settings'
        }, {
            'case': 'Default%20%28OSX%29.sublime-keymap',
            'expected': 'Default (OSX).sublime-keymap'
        }, {
            'case': 'Shell-Unix-Generic.subl%C3%ADme-settings',
            'expected': 'Shell-Unix-Generic.sublíme-settings'
        }, {
            'case': 'Shell-%D1%88%D0%B5%D0%B4%D1%86%D0%B2%D1%84%D0%B8%D0%BB%D0%B5.sublime',
            'expected': 'Shell-шедцвфиле.sublime'
        }]

        for p in paths:
            self.assertEqual(path.decode(p['case']), p['expected'])

    @mock.patch('platform.system', return_value='Windows')
    def test_join_as_windows(self, _):
        self.assertEqual(path.join('this', 'is', 'my', 'path'), 'this\\is\\my\\path')

    @mock.patch('platform.system', return_value='Linux')
    def test_join_as_unix_platform(self, _):
        self.assertEqual(path.join('this', 'is', 'my', 'path'), 'this/is/my/path')

    def test_folder_existence(self):
        cases = [
            ('./', True),
            ('some/path', False),
        ]

        for case in cases:
            test, expected = case
            self.assertEqual(path.exists(test, folder=True), expected)

    def test_file_existence(self):
        cases = [
            (path.join('.', __file__), True),
            ('.', False),
            ('another_path/to_/file', False),
            (path.join(os.getcwd(), 'tests', 'test_gist.py'), False),
            (path.join(os.getcwd(), 'sync_settings', 'tests', 'test_gist.py'), True),
        ]

        for case in cases:
            test, expected = case
            self.assertEqual(path.exists(test), expected)
