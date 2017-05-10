'''
SYNOPSIS

    class Version
    class PkgSpec

DESCRIPTION

    Common types are used by tools.
'''


class Version:
    def __init__(self, major, minor, rev=0):
        self._major = major
        self._minor = minor
        self._rev = rev
        self._pkg_ver = '{}.{}.{}'.format(major, minor, rev)

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def rev(self):
        return self._rev

    @property
    def pkg_ver(self):
        return self._pkg_ver


class PkgSpec:
    def __init__(self, name, version, root, src, dest, doc, dist, test):
        self._name = name
        self._version = version
        self._root = root
        self._src = src
        self._dest = dest
        self._doc = doc
        self._dist = dist
        self._test = test

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def root(self):
        return self._root

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest

    @property
    def doc(self):
        return self._doc

    @property
    def dist(self):
        return self._dist

    @property
    def test(self):
        return self._test


class DepPkgSpec:
    def __init__(self, src, dest, tmp):
        self._src = src
        self._dest = dest
        self._tmp = tmp

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest

    @property
    def tmp(self):
        return self._tmp
