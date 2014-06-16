Software Carpentry Windows Installer

Helps mimic a *nix environment on Windows with as little work as possible.

The script:

* Installs [nano][] and makes it accessible from [msysGit][]
* Installs [SQLite][] and makes it accessible from msysGit
* Creates a `~/nano.rc` with links to syntax highlighting configs
* Provides standard [nosetests][] behavior for msysGit
* Adds [R][]'s bin directory to the path (if we can find it)

To use:

1. Install [Python][], [IPython][], and [Nose][nose].  An easy way to
   do this is with the [Anaconda CE][Anaconda-CE] Python distribution.
2. [Install msysGit][msysgit-install]
3. Run `swc-windows-installer.py`.  You should be able to simply
   double click the file in Windows.

[msysGit]: http://msysgit.github.io/
[msysgit-install]: https://github.com/msysgit/msysgit/releases
[nano]: http://www.nano-editor.org/
[SQLite]: http://www.sqlite.org/
[Python]: https://www.python.org/
[IPython]: http://ipython.org/
[Nose]: https://nose.readthedocs.org/en/latest/
[nosetests]: https://nose.readthedocs.org/en/latest/usage.html
[R]: http://www.r-project.org/
[Anaconda-CE]: http://continuum.io/anacondace.html
