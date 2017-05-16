from os.path import realpath, dirname

from tool.shell import call

_ROOT = realpath(dirname(dirname(__file__)))
_EXCLUDES = [
    'venv', 'dest', 'build', 'dist', 'tsrc', 'dsrc', 'tmp',
    '__init__.py', '__pycache__', 'conf.py', 'conftest.py',
    '.*', '*.pyc'
]


def test_coding():
    call(['flake8', _ROOT, '--exclude', ','.join(_EXCLUDES)])
