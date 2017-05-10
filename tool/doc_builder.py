'''
SYNOPSIS

    build_doc(spec)
    open_doc(spec, port)

DESCRIPTION

    Build documents.
'''

import webbrowser
from os import path
from time import sleep
from subprocess import Popen

from .shell import call, rm


def build_doc(spec):
    dest = path.join(spec.dest, 'doc')

    call(['sphinx-build', '-b', 'html',  spec.doc, dest])


def clean_doc(spec):
    rm(path.join(spec.dest, 'doc'))


def open_doc(spec, port):
    doc_dir = path.join(spec.dest, 'doc')
    p = Popen(['python', '-m', 'http.server', str(port)], cwd=doc_dir)
    sleep(1)
    webbrowser.open('http://localhost:%i' % (port))

    input('Press any key to terminate document server')
    p.kill()
