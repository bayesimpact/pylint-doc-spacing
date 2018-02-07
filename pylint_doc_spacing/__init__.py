"""PyLint Doc Spacing extension."""

import linecache

from pylint import checkers
from pylint import interfaces

__version__ = '0.0.1'


def register(linter):
    """Register this plugin."""

    linter.register_checker(DocSpacingChecker(linter))


# TODO(pascal): Add tests.


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
        first_body_lineno = node.body[0].fromlineno
        line_before_body = linecache.getline(node.root().file, first_body_lineno-1)
        if line_before_body.strip():
            self.add_message('doc-spacing-missing', line=first_body_lineno-1, node=node, args=args)
            return

        line_above = linecache.getline(node.root().file, first_body_lineno-2)
        if not line_above.strip():
            self.add_message('doc-spacing-extra', node=node, line=first_body_lineno-1, args=args)
