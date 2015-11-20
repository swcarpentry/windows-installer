Software Carpentry Windows Installer

Helps mimic a *nix environment on Windows with as little work as possible.

The script:

* Installs [GNU Make][make] and makes it accessible from [msysGit][]
* Installs [nano][] and makes it accessible from msysGit
* Installs [SQLite][] and makes it accessible from msysGit
* Creates a `~/nano.rc` with links to syntax highlighting configs
* Provides standard [nosetests][] behavior for msysGit
* Adds [R][]'s bin directory to the path (if we can find it)

Building
========

Building the Windows installer requires a Windows machine with [Python][],
[py2exe][] and [Inno Setup][inno]. `py2exe` can be installed using `pip` and
Inno Setup can be installed using the self-installing package from
[the download page][inno-download].

```
python setup.py install
python setup.py py2exe
ISCC.exe swc-installer.iss
```

For folks who don't want to build their own version, the most recent
version is also [available here][compiled].

Using
=====

Just have your students download and double-click the compiled
installer.  If you're using [R][], you'll have to [install
R][R-install] before running this installer (because this installer
searches likely paths to find R's `bin` directory).  Otherwise, you
can run it whenever you like (e.g. either before or after installing
[Python][]).

[make]: https://www.gnu.org/software/make/
[msysGit]: http://msysgit.github.io/
[nano]: http://www.nano-editor.org/
[SQLite]: http://www.sqlite.org/
[nosetests]: https://nose.readthedocs.org/en/latest/usage.html
[R]: http://www.r-project.org/
[R-install]: http://cran.r-project.org/bin/windows/base/rw-FAQ.html#Installation-and-Usage
[Python]: https://www.python.org/
[py2exe]: http://py2exe.org/
[inno]: http://www.jrsoftware.org/isinfo.php
[inno-download]: http://www.jrsoftware.org/isdl.php
[compiled]: https://github.com/swcarpentry/windows-installer/releases/latest
