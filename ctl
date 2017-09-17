#!/usr/bin/env python3

'''
SYNOPSIS

    ctl test
    clt dist

DESCRIPTION

    Command line interface allow perform tasks of software project.
'''

import os
import sys
import shutil
import click
from os import path
from os.path import realpath, dirname
from subprocess import Popen
from sys import executable

from tool.type import Version, PkgSpec, DepPkgSpec
from tool.builder import pkg_doc, pkg_test, pkg_dist, pkg_release, \
                         pkg_doc_clear, pkg_dist_clear
from tool.doc_builder import open_doc

ROOT = realpath(dirname(__file__))

pkg_ver = Version(0, 1, 0)
pkg_spec = PkgSpec('clink', pkg_ver, ROOT, path.join(ROOT, 'src'),
                    path.join(ROOT, 'dest'), path.join(ROOT, 'doc'),
                    path.join(ROOT, 'dist'), path.join(ROOT, 'test'))


@click.group()
def cli():
    pass

@cli.command(help='Build pip package')
@click.option('--clear', is_flag=True, help='Clear dist files')
def dist(clear):
    if clear:
        pkg_dist_clear(pkg_spec)
    else:
        pkg_dist(pkg_spec)


@cli.command(help='Build pip package and put to PyPi')
def release():
    pkg_release(pkg_spec)


@cli.command(help='Build document')
@click.option('--clear', is_flag=True, help='Clear dest/doc/ directory')
@click.option('--view', is_flag=True, help='Open HTML document')
@click.option('--force', is_flag=True, help='Force rebuild anythings')
def doc(clear, view, force):
    if clear:
        pkg_doc_clear(pkg_spec)
    elif view:
        open_doc(pkg_spec, 8081)
    else:
        pkg_doc(pkg_spec, force)


@cli.command(help='Run unit testing')
def test():
    pkg_test(pkg_spec)


cli()
