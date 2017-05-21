'''
SYNOPSIS

    pkg_test(spec)
    pkg_dist(spec)
    pkg_clean(spec)
    pkg_doc(spec)
    pkg_doc_clean(spec)

DESCRIPTION

    Control building of this package.
'''

from .shell import call
from .doc_builder import build_doc, clean_doc
from .packer import dist_pip, clean_dist, release_pip


def pkg_doc(spec, force):
    build_doc(spec, force)


def pkg_doc_clean(spec):
    clean_doc(spec)


def pkg_test(spec):
    call(['pytest', spec.test])


def pkg_dist(spec):
    dist_pip(spec)


def pkg_release(spec):
    release_pip(spec)


def pkg_dist_clean(spec):
    clean_dist(spec)
