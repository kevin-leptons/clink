'''
SYNOPSIS

    build_pip(spec)

DESCRIPTION

    Build pip packages.
'''

import sys

from .shell import call


def build_pip(spec):
    cmd = [sys.executable, 'setup.py', 'sdist', 'bdist_wheel']
    call(cmd)
