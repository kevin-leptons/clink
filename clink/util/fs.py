from os import path
from os.path import realpath, dirname

_ASSET_DIR = realpath(path.join(dirname(__file__), '../asset'))


def asset_path(rel_path):
    '''
    Return absolute path to Clink's asset directory

    :param str path:
    :rtype: str
    '''

    return path.join(_ASSET_DIR, rel_path)
