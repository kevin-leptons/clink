from sys import executable
from tool.shell import call


def test_build_and_dist():
    call([executable, 'ctl', 'doc', '--clean'])
    call([executable, 'ctl', 'doc'])
    call([executable, 'ctl', 'dist', '--clean'])
    call([executable, 'ctl', 'dist'])
