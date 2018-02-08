"""PyLint Doc Spacing extension."""

import linecache
import pdb

from pylint import checkers
from pylint import interfaces

__version__ = '0.0.3'


def register(linter):
    """Register this plugin."""

    linter.register_checker(DocSpacingChecker(linter))


class DocSpacingChecker(checkers.BaseChecker):
    """Checks the presence/absence of a blank line after documentations."""

    __implements__ = interfaces.IAstroidChecker

    name = 'doc_spacing'

    msgs = {
        'C4101': (
            'Missing a blank line after the %s documentation',
            'doc-spacing-missing',
            'Used when a documentation string is not followed by a blank line',
        ),
        'C4102': (
            'Too many blank lines after the %s documentation',
            'doc-spacing-extra',
            'Used when a documentation string is followed by more than one blank line',
        ),
    }

    def visit_classdef(self, node):
        """Check lints in a class definition."""

        self._check_doc_spacing(node, 'class')

    def visit_functiondef(self, node):
        """Check lints in a function/method definition."""

        self._check_doc_spacing(node, 'function')

    def visit_module(self, node):
        """Check lints in a module."""

        self._check_doc_spacing(node, 'module')

    def _check_doc_spacing(self, node, args):
        if node.doc is None or not node.body:
            return

        # Collect blank lines and comments above the first child node.
        lines_before_body = []
        for lineno in range(node.body[0].lineno - 1, node.lineno, -1):
            line = linecache.getline(node.root().file, lineno)

            if line.strip() and not line.lstrip().startswith('#'):
                break

            lines_before_body.append((lineno, line))
        lines_before_body = list(reversed(lines_before_body))

        try:
            lineno, first_empty_line = lines_before_body.pop(0)
        except IndexError:
            first_empty_line = 'Non empty'
            lineno = node.body[0].lineno

        if first_empty_line.strip():
            self.add_message(
                'doc-spacing-missing', line=lineno, node=node, args=args,
                confidence=interfaces.HIGH)

        for lineno, line in lines_before_body:
            if line.strip():
                break
            self.add_message(
                'doc-spacing-extra', node=node, line=lineno, args=args,
                confidence=interfaces.HIGH)
