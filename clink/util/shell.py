import os
from subprocess import Popen, CalledProcessError
from os import makedirs, remove
from os.path import isdir, isfile, exists, basename, dirname
from shutil import copyfile, copytree, rmtree


def call(args, cwd=None):
    '''
    Perform new processing

    :param list[str] args:
    :param str cwd:
    '''

    exit_code = Popen(args, cwd=cwd).wait()
    if exit_code != 0:
        raise CalledProcessError(exit_code, args)


def cp(src, dest, exist_ignore=True):
    '''
    Copy file or directory

    :param str src:
    :param str dest:
    :param bool exist_ignore:
    '''

    if isdir(src):
        return _cp_dir(src, dest, exist_ignore)
    else:
        return _cp_file(src, dest, exist_ignore)


def rm(path, exist_ignore=True):
    '''
    Remove files

    :param str path:
    :param bool exist_ignore:
    '''

    if (not exists(path)) and exist_ignore:
        return
    if isdir(path):
        rmtree(path)
    else:
        remove(path)


def mkdir(path):
    '''
    Create new directory

    :param str path:
    '''

    if not isdir(path):
        makedirs(path)


def chmod(path, mode):
    '''
    Change mode of file

    :param str path:
    :param int mode:
    '''

    os.chmod(path, mode)


def touch(path, mode):
    '''
    Create new empty file

    :param str path:
    :param int mode:
    '''

    mkdir(dirname(path))
    f = open(path, 'w+')
    f.close()
    os.chmod(path, mode)


def _cp_dir(src, dest, exist_ignore):
    if isdir(dest):
        dest_dir = os.path.join(dest, basename(src))
        if isdir(dest_dir) and exist_ignore:
            return dest_dir
        copytree(src, dest_dir)
        return dest_dir
    else:
        copytree(src, dest)
        return dest


def _cp_file(src, dest, exist_ignore):
    if isfile(dest) and exist_ignore:
        return dest
    if isdir(dest):
        dest_file = os.path.join(dest, basename(src))
        copyfile(src, dest_file)
        return dest_file
    else:
        copyfile(src, dest)
        return dest
