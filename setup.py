#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs


try:
    from setuptools import setup, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, Command  # noqa
from distutils.command.install import INSTALL_SCHEMES

extra = {}

# -*- Python 3 -*-
is_py3k = sys.version_info[0] == 3
if is_py3k:
    extra.update(use_2to3=True)

NAME = 'django-postgres-audit'


class RunTests(Command):
    description = 'Run the django test suite from the tests dir.'
    user_options = []
    extra_env = {}
    extra_args = []

    def run(self):
        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, 'tests')
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_from_command_line as cli
        os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get(
                        'DJANGO_SETTINGS_MODULE', 'settings')

        prev_argv = list(sys.argv)
        try:
            sys.argv = [__file__, 'test', 'pgaudit', 'someapp'] + self.extra_args
            cli(sys.argv)
        finally:
            sys.argv = prev_argv
        os.chdir(this_dir)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See http://github.com/StefanKjartansson/django-postgres-audit'


setup(
    name=NAME,
    platforms=['any'],
    license='BSD',
    packages=['pgaudit'],
    zip_safe=False,
    install_requires=[
    ],
    cmdclass={'test': RunTests},
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
    },
    long_description=long_description,
    **extra
)
