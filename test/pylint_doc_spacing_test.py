"""Unit tests for the PyLint Doc Spacing plugin."""

import unittest

import astroid
import mock
from pylint import interfaces
from pylint import testutils

import pylint_doc_spacing


class TestCase(unittest.TestCase, testutils.CheckerTestCase):
    """Unit tests for the DocSpacingChecker class."""

    CHECKER_CLASS = pylint_doc_spacing.DocSpacingChecker

    def setUp(self):
        super(TestCase, self).setUp()
        self.setup_method()
        patcher = mock.patch(pylint_doc_spacing.__name__ + '.linecache')
        mock_linecache = patcher.start()
        mock_linecache.getline.side_effect = self._linecache_getline
        self.addCleanup(patcher.stop)
        self._code = {}

    def _linecache_getline(self, path, lineno):
        return self._code[path][lineno - 1]

    def _parse_module(self, code, path):
        self._code[path] = code.splitlines(True)
        return astroid.parse(code, path=path)

    def test_correct_spacing_for_all(self):
        """Test module with perfect documentation."""

        module_node = self._parse_module('''"""Module documentation."""

import unittest

class A(object):
    """Documentation of A."""

    def b():
        """Documentation of b."""

        pass
''', path='/unittest/perfect_spacing.py')
        with self.assertNoMessages():
            self.walk(module_node)

    def test_module_missing_spacing(self):
        """Test module missing spacing after documentation."""

        module_node = self._parse_module('''"""Module documentation."""
import unittest

def a():
    pass
''', path='/unittest/module_missing_spacing.py')
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='doc-spacing-missing',
                node=module_node,
                line=2,
                args='module',
                confidence=interfaces.HIGH,
            ),
        ):
            self.walk(module_node)

    def test_module_extra_spacing(self):
        """Test module with extra spacing after documentation."""

        module_node = self._parse_module('''"""Module documentation."""



import unittest

def a():
    pass
''', path='/unittest/module_extra_spacing.py')
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='doc-spacing-extra',
                node=module_node,
                line=3,
                args='module',
                confidence=interfaces.HIGH,
            ),
            testutils.Message(
                msg_id='doc-spacing-extra',
                node=module_node,
                line=4,
                args='module',
                confidence=interfaces.HIGH,
            ),
        ):
            self.walk(module_node)

    def test_function_decorator(self):
        """Test a function with a decoartor but correct spacing."""

        module_node = self._parse_module('''class A(object):
    """Documentation of class."""

    @auth.require_user()
    def save(self):
        pass
''', path='/unittest/function_decorated.py')
        with self.assertNoMessages():
            self.walk(module_node)

    def test_commented_import(self):
        """Test an import with a comment above."""

        module_node = self._parse_module('''"""Module documentation."""

# Following imports are important.
import unittest
''', path='/unittest/commented_import.py')
        with self.assertNoMessages():
            self.walk(module_node)

    def test_commented_import_nospacing(self):
        """Test an import with a comment above replacing the spacing."""

        module_node = self._parse_module('''"""Module documentation."""
# Following imports are important.
import unittest
''', path='/unittest/commented_import_no_spacing.py')
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='doc-spacing-missing',
                node=module_node,
                line=2,
                args='module',
                confidence=interfaces.HIGH,
            ),
        ):
            self.walk(module_node)

    @testutils.set_config(
        function_doc_spacing='none',
        module_doc_spacing='any',
    )
    def test_correct_spacing_with_different_config(self):
        """Test module with perfect documentation on a different config."""

        module_node = self._parse_module('''"""Module documentation."""


import unittest

class A(object):
    """Documentation of A."""

    def b():
        """Documentation of b."""
        pass
''', path='/unittest/perfect_spacing.py')
        with self.assertNoMessages():
            self.walk(module_node)

    @testutils.set_config(module_doc_spacing='none')
    def test_extra_blank_line_for_none_config(self):
        """Test an extra blank line when config is set to none."""

        module_node = self._parse_module('''"""Module documentation."""

import unittest
''', path='/unittest/perfect_spacing.py')
        with self.assertAddsMessages(
            testutils.Message(
                msg_id='doc-spacing-extra',
                node=module_node,
                line=2,
                args='module',
                confidence=interfaces.HIGH,
            ),
        ):
            self.walk(module_node)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
