'''
SYNOPSIS

    build_doc(spec)
    open_doc(spec, port)
    clear_doc(spec)

DESCRIPTION

    Build documents.
'''

import webbrowser
from os import path
from time import sleep
from subprocess import Popen

from .shell import call, rm


def build_doc(spec, force=False):
    dest = path.join(spec.dest, 'doc')
    cmd = ['sphinx-build', '-b', 'html',  spec.doc, dest]
    if force:
        cmd.insert(3, '-a')
    call(cmd)


def clear_doc(spec):
    rm(path.join(spec.dest, 'doc'))


def open_doc(spec, port):
    doc_dir = path.join(spec.dest, 'doc')
    p = Popen(['python', '-m', 'http.server', str(port)], cwd=doc_dir)
    sleep(1)
    webbrowser.open('http://localhost:%i' % (port))

    input('Press any key to terminate document server')
    p.kill()
