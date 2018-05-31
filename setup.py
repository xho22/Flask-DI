"""
Flask-DI
--------
Adds dependency injection to your Flask application.

Please see Github for a quick start guide.
"""
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

__version__ = 0.1


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='Flask-DI',
    version=__version__,
    url='http://github.com/chrismeh/flask-di',
    license='MIT',
    author='Christian Mehring',
    author_email='christian@sourcegoat.io',
    description='Adds dependency injection to your Flask application',
    long_description=__doc__,
    keywords='flask dependency injection service locator',
    packages=['flask_di'],
    zip_safe=False,
    platforms='any',
    install_requires=['flask'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)