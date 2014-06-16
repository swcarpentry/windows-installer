Software Carpentry Windows Installer

Helps mimic a *nix environment on Windows with as little work as possible.

The script:

* Installs [nano][] and makes it accessible from [msysGit][]
* Installs [SQLite][] and makes it accessible from msysGit
* Creates a `~/nano.rc` with links to syntax highlighting configs
* Provides standard [nosetests][] behavior for msysGit
* Adds [R][]'s bin directory to the path (if we can find it)

Building
========

TODO

For folks who don't want to build their own version, the most recent
version is also [available here][compiled].

Using
=====

Just have your students download and double-click the compiled
installer.

[msysGit]: http://msysgit.github.io/
[nano]: http://www.nano-editor.org/
[SQLite]: http://www.sqlite.org/
[nosetests]: https://nose.readthedocs.org/en/latest/usage.html
[R]: http://www.r-project.org/
[compiled]: http://files.software-carpentry.org/SWCarpentryInstaller.exe
