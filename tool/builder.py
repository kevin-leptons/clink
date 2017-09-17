'''
SYNOPSIS

    pkg_test(spec)
    pkg_dist(spec)
    pkg_clear(spec)
    pkg_doc(spec)
    pkg_doc_clear(spec)

DESCRIPTION

    Control building of this package.
'''

from .shell import call
from .doc_builder import build_doc, clear_doc
from .packer import dist_pip, clear_dist, release_pip


def pkg_doc(spec, force):
    build_doc(spec, force)


def pkg_doc_clear(spec):
    clear_doc(spec)


def pkg_test(spec):
    call(['pytest', spec.test])


def pkg_dist(spec):
    dist_pip(spec)


def pkg_release(spec):
    release_pip(spec)


def pkg_dist_clear(spec):
    clear_dist(spec)
