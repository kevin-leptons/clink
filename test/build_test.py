from sys import executable
from tool.shell import call


def test_build_and_dist():
    call([executable, 'ctl', 'doc', '--clear'])
    call([executable, 'ctl', 'doc'])
    call([executable, 'ctl', 'dist', '--clear'])
    call([executable, 'ctl', 'dist'])
