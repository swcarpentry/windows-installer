#!/usr/bin/env python

"""Software Carpentry Windows Installer

Helps mimic a *nix environment on Windows with as little work as possible.

The script:
* Installs GNU Make and makes it accessible from msysGit
* Installs nano and makes it accessible from msysGit
* Installs SQLite and makes it accessible from msysGit
* Creates a ~/nano.rc with links to syntax highlighting configs
* Provides standard nosetests behavior for msysGit
* Adds R's bin directory to the path (if we can find it)

To use:

1. Install Python, IPython, and Nose.  An easy way to do this is with
   the Anaconda Python distribution
   http://continuum.io/downloads
2. Install msysGit
   https://github.com/msysgit/msysgit/releases
3. Install R (if your workshop uses R)
   http://cran.r-project.org/bin/windows/base/rw-FAQ.html#Installation-and-Usage
4. Run swc-windows-installer.py.
   You should be able to simply double click the file in Windows

"""

import glob
import hashlib
try:  # Python 3
    from io import BytesIO as _BytesIO
except ImportError:  # Python 2
    from StringIO import StringIO as _BytesIO
import logging
import os
import re
import sys
import tarfile
try:  # Python 3
    from urllib.request import urlopen as _urlopen
except ImportError:  # Python 2
    from urllib2 import urlopen as _urlopen
import zipfile


__version__ = '0.3'

LOG = logging.getLogger('swc-windows-installer')
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)


if sys.version_info >= (3, 0):  # Python 3
    _MakeDirsError = OSError
    open3 = open
else:
    _MakeDirsError = os.error
    def open3(file, mode='r', newline=None):
        if newline:
            if newline != '\n':
                raise NotImplementedError(newline)
            f = open(file, mode + 'b')
        else:
            f = open(file, mode)
        return f


def download(url, sha1=None, sha512=None):
    """Download a file and verify its hash"""
    LOG.debug('download {}'.format(url))
    r = _urlopen(url)
    byte_content = r.read()
    for name, expected, hasher in [
            ('SHA-1', sha1, hashlib.sha1),
            ('SHA-512', sha512, hashlib.sha512),
            ]:
        if expected:
            download_hash = hasher(byte_content).hexdigest()
            if download_hash != expected:
                raise ValueError(
                    'downloaded {!r} has the wrong {} hash: {} != {}'.format(
                        url, name, download_hash, expected))
        LOG.debug('{} for {} matches the expected {}'.format(
            name, url, expected))
    return byte_content


def splitall(path):
    """Split a path into a list of components

    >>> splitall('nano-2.2.6/doc/Makefile.am')
    ['nano-2.2.6', 'doc', 'Makefile.am']
    """
    parts = []
    while True:
        head, tail = os.path.split(path)
        if tail:
            parts.insert(0, tail)
        elif head:
            parts.insert(0, head)
            break
        else:
            break
        path = head
    return parts


def transform(tarinfo, strip_components=0):
    """Transform TarInfo objects for extraction"""
    path_components = splitall(tarinfo.name)
    try:
        tarinfo.name = os.path.join(*path_components[strip_components:])
    except TypeError:
        if len(path_components) <= strip_components:
            return None
        raise
    return tarinfo


def tar_install(url, install_directory, compression='*', strip_components=0,
                **kwargs):
    """Download and install a tar bundle"""
    if not os.path.isdir(install_directory):
        tar_bytes = download(url=url, **kwargs)
        tar_io = _BytesIO(tar_bytes)
        filename = os.path.basename(url)
        mode = 'r:{}'.format(compression)
        tar_file = tarfile.open(filename, mode, tar_io)
        LOG.info('installing {} into {}'.format(url, install_directory))
        os.makedirs(install_directory)
        members = [
            transform(tarinfo=tarinfo, strip_components=strip_components)
            for tarinfo in tar_file]
        tar_file.extractall(
            path=install_directory,
            members=[m for m in members if m is not None])
    else:
        LOG.info('existing installation at {}'.format(install_directory))


def zip_install(url, install_directory, path=None, **kwargs):
    """Download and install a zipped bundle"""
    if path is None:
        path = install_directory
    if not os.path.exists(path):
        zip_bytes = download(url=url, **kwargs)
        zip_io = _BytesIO(zip_bytes)
        zip_file = zipfile.ZipFile(zip_io)
        LOG.info('installing {} into {}'.format(url, install_directory))
        try:
            os.makedirs(install_directory)
        except _MakeDirsError:
            pass
        zip_file.extractall(install_directory)
    else:
        LOG.info('existing installation at {}'.format(install_directory))


def install_make(install_directory):
    """Download and install GNU Make"""
    zip_install(
        url='http://downloads.sourceforge.net/project/gnuwin32/make/3.81/make-3.81-bin.zip',
        sha1='7c1e23a93e6cb78975f36efd22d598241b1f0e8b',
        sha512='7b67c9a32c727e3929900272ef05f5c52035b5731ab3d46abe9e641c2f28c049d094e497e5097f431ee680ace342542854d541a09ebece7730af25e69d033447',
        install_directory=install_directory,
        path=os.path.join(install_directory, 'bin', 'make.exe'))
    zip_install(
        url='http://downloads.sourceforge.net/project/gnuwin32/make/3.81/make-3.81-dep.zip',
        sha1='ee90e45c1bacc24a0c3852a95fc6dcfbcabe802b',
        sha512='bd4467c0d708c1deec3604754cea9428e4aa5f6e7d9ec24f62bc4d68308f12dec4661b900c1787b50327bc7eb9a482a0ae6ee863c21937c1faea414e5ccb5c04',
        install_directory=install_directory,
        path=os.path.join(install_directory, 'bin', 'libiconv2.dll'))


def install_nano(install_directory):
    """Download and install the nano text editor"""
    zip_install(
        url='http://www.nano-editor.org/dist/v2.2/NT/nano-2.2.6.zip',
        sha1='f5348208158157060de0a4df339401f36250fe5b',
        sha512='83a4cdf56232c5c2f14f42275804d1af120a2346f03004ce6be384af68f73e39cbd0b9faf62f494253907d4f6606ee91b8c3c1abf6b949f27593bf41e0e3b00f',
        install_directory=install_directory)


def install_nanorc(install_directory):
    """Download and install nano syntax highlighting"""
    tar_install(
        url='http://www.nano-editor.org/dist/v2.2/nano-2.2.6.tar.gz',
        sha1='f2a628394f8dda1b9f28c7e7b89ccb9a6dbd302a',
        sha512='e1ee5d63725055290a5117b73352a8557cc3105c737643e341a95ebbb0cecb06c46f86a2363de8455e9de3940e3f920c47af92e19ef9c53862de8a605da08d8d',
        install_directory=install_directory,
        strip_components=1)
    home = os.path.expanduser('~')
    nanorc = os.path.join(home, 'nano.rc')
    if not os.path.isfile(nanorc):
        syntax_dir = os.path.join(install_directory, 'doc', 'syntax')
        LOG.info('include nanorc from {} in {}'.format(syntax_dir, nanorc))
        with open3(nanorc, 'w', newline='\n') as f:
            for filename in os.listdir(syntax_dir):
                if filename.endswith('.nanorc'):
                    path = os.path.join(syntax_dir, filename)
                    rel_path = os.path.relpath(path, home)
                    include_path = make_posix_path(os.path.join('~', rel_path))
                    f.write('include {}\n'.format(include_path))


def install_sqlite(install_directory):
    """Download and install the SQLite shell"""
    zip_install(
        url='http://sqlite.org/2015/sqlite-shell-win32-x86-3090200.zip',
        sha1='25d78bbba37d2a0d9b9f86ed897e454ccc94d7b2',
        sha512='e4eb51f674262cf65e0fe6e6d64c4ddb30301adcb295874fb1c5a6c522642f402b326ad8f46cd79d5b8db7bcac552d0cb79e114d93291c910b08eeee0a949848',
        install_directory=install_directory)


def create_nosetests_entry_point(python_scripts_directory):
    """Creates a terminal-based nosetests entry point for msysGit"""
    contents = '\n'.join([
            '#!/usr/bin/env/ python',
            'import sys',
            'import nose',
            "if __name__ == '__main__':",
            '    sys.exit(nose.core.main())',
            '',
            ])
    if not os.path.isdir(python_scripts_directory):
        os.makedirs(python_scripts_directory)
    path = os.path.join(python_scripts_directory, 'nosetests')
    LOG.info('create nosetests entrypoint {}'.format(path))
    with open(path, 'w') as f:
        f.write(contents)


def get_r_bin_directory():
    """Locate the R bin directory (if R is installed)
    """
    version_re = re.compile('^R-(\d+)[.](\d+)[.](\d+)$')
    paths = {}
    for pf in [
            os.environ.get('ProgramW6432', r'c:\Program Files'),
            os.environ.get('ProgramFiles', r'c:\Program Files'),
            os.environ.get('ProgramFiles(x86)', r'c:\Program Files(x86)'),
            ]:
        bin_glob = os.path.join(pf, 'R', 'R-[0-9]*.[0-9]*.[0-9]*[a-z]*', 'bin')
        for path in glob.glob(bin_glob):
            version_dir = os.path.basename(os.path.dirname(path))
            version_match = version_re.match(version_dir)
            if version_match and version_match.groups() not in paths:
                paths[version_match.groups()] = path
    if not paths:
        LOG.info('no R installation found under {}'.format(pf))
        return
    LOG.debug('detected R installs:\n* {}'.format('\n* '.join([
        v for k,v in sorted(paths.items())])))
    version = sorted(paths.keys())[-1]
    LOG.info('using R v{} bin directory at {}'.format(
        '.'.join(version), paths[version]))
    return paths[version]


def update_bash_profile(extra_paths=()):
    """Create or append to a .bash_profile for Software Carpentry

    Adds nano to the path, sets the default editor to nano, and adds
    additional paths for other executables.
    """
    lines = [
        '',
        '# Add paths for Software-Carpentry-installed scripts and executables',
        'export PATH=\"$PATH:{}\"'.format(':'.join(
            make_posix_path(path) for path in extra_paths),),
        '',
        '# Make nano the default editor',
        'export EDITOR=nano',
        '',
        ]
    config_path = os.path.join(os.path.expanduser('~'), '.bash_profile')
    LOG.info('update bash profile at {}'.format(config_path))
    LOG.debug('extra paths:\n* {}'.format('\n* '.join(extra_paths)))
    with open(config_path, 'a') as f:
        f.write('\n'.join(lines))


def make_posix_path(windows_path):
    """Convert a Windows path to a posix path"""
    for regex, sub in [
            (re.compile(r'\\'), '/'),
            (re.compile('^[Cc]:'), '/c'),
            ]:
        windows_path = regex.sub(sub, windows_path)
    return windows_path


def main():
    swc_dir = os.path.join(os.path.expanduser('~'), '.swc')
    bin_dir = os.path.join(swc_dir, 'bin')
    make_dir = os.path.join(swc_dir, 'opt', 'make')
    make_bin = os.path.join(make_dir, 'bin')
    nano_dir = os.path.join(swc_dir, 'opt', 'nano')
    nanorc_dir = os.path.join(swc_dir, 'share', 'nanorc')
    sqlite_dir = os.path.join(swc_dir, 'opt', 'sqlite')
    create_nosetests_entry_point(python_scripts_directory=bin_dir)
    install_make(install_directory=make_dir)
    install_nano(install_directory=nano_dir)
    install_nanorc(install_directory=nanorc_dir)
    install_sqlite(install_directory=sqlite_dir)
    paths = [make_bin, nano_dir, sqlite_dir, bin_dir]
    r_dir = get_r_bin_directory()
    if r_dir:
        paths.append(r_dir)
    update_bash_profile(extra_paths=paths)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v', '--verbose',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
        help='Verbosity (defaults to {!r})'.format(
            logging.getLevelName(LOG.level).lower()))
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    if args.verbose:
        level = getattr(logging, args.verbose.upper())
        LOG.setLevel(level)

    LOG.info('Preparing your Software Carpentry awesomeness!')
    LOG.info('installer version {}'.format(__version__))
    main()
    LOG.info('Installation complete.')
