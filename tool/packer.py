'''
SYNOPSIS

    dist_pip(spec)
    release_pip(spec)
    clear_dist(spec)

DESCRIPTION

    Pack this package into distribution format and push to PyPi
'''

from os import path

from .pip_builder import build_pip
from .shell import call, rm


def dist_pip(spec):
    build_pip(spec)


def release_pip(spec):
    clear_dist(spec)
    build_pip(spec)
    call(['twine', 'upload', path.join(spec.dist, '**')])


def clear_dist(spec):
    rm(spec.dist)
    rm(path.join(spec.root, 'build'))
    rm(path.join(spec.root, spec.name + '.egg-info'))
