from os import path
from os.path import realpath, dirname

from tool.shell import call


root = realpath(path.join(dirname(__file__), '..'))
exclude_files = ('venv,dest,dist,tsrc,dsrc,tmp,dpkg,__init__.py,.*,'
                 'conf.py')


def test_coding():
    call(['flake8', root, '--exclude', exclude_files])
