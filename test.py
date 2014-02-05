# coding: utf-8
import os
import sys
from unittest.mock import Mock
sys.path.insert(0, os.getcwd())
import unittest
import webbrowser
try:
    import coverage
except ImportError:
    coverage = None

if not 'coverage' in sys.argv:
    coverage = None


class Coverage:
    omit = [
        'blvresearch/test.py'
    ]
    include = [
        'blvresearch/*'
    ]
    exclude = [
        'raise AssertionError',
        'raise NotImplementedError'
    ]
    _html_directory = '.coverage_html'

    def __init__(self, coverage):
        if not coverage:
            print('not measuring coverage')
            coverage = Mock()
        self.cov = coverage.coverage(omit=self.omit, include=self.include)
        self.add_excluded_lines()

    def __enter__(self):
        self.cov.start()

    def __exit__(self, type, value, traceback):
        self.cov.stop()
        if not isinstance(self.cov, Mock):
            self.create_html_report()
            self.open_report_in_browser()

    def add_excluded_lines(self):
        for e in self.exclude:
            self.cov.exclude(e)

    def create_html_report(self):
        if not os.path.exists(self._html_directory):
            os.makedirs(self._html_directory)
        self.cov.html_report(directory=self._html_directory)

    def open_report_in_browser(self):
        webbrowser.open('file:///' + os.getcwd() + '/' +
                        self._html_directory + '/index.html')

if __name__ == '__main__':
    with Coverage(coverage):
        testsuite = unittest.TestLoader().discover('blvresearch/tests',
                                                   pattern='*test*.py')
        exit_code = unittest.TextTestRunner(verbosity=1).run(testsuite)
    if exit_code.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
