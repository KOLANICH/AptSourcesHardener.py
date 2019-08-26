AptSourcesHardener.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
![GitLab Build Status](https://gitlab.com/KOLANICH/AptSourcesHardener.py/badges/master/pipeline.svg)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/AptSourcesHardener.py.svg?branch=master)](https://travis-ci.org/KOLANICH/AptSourcesHardener.py)
![GitLab Coverage](https://gitlab.com/KOLANICH/AptSourcesHardener.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/AptSourcesHardener.py.svg)](https://coveralls.io/r/KOLANICH/AptSourcesHardener.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/AptSourcesHardener.py.svg)](https://libraries.io/github/KOLANICH/AptSourcesHardener.py)

This is the library to harden `sources.lists` using the recommendations from https://wiki.debian.org/DebianRepository/UseThirdParty (for all the sources).

* Binds every source to its public key.
    * If a file is present, uses the file
    * Otherwise uses key fingerprint.

Requirements
------------
* [`Python >=3.4`](https://www.python.org/downloads/). [`Python 2` is dead, stop raping its corpse.](https://python3statement.org/) Use ```2to3``` with manual postprocessing to migrate incompatible code to `3`. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their `dict` is ordered and deterministic. Python 3 is also semi-dead, 3.7 is the last minor release in 3.
* [`AptSourcesList.py`](https://gitlab.com/KOLANICH/AptSourcesList.py) ![Licence](https://img.shields.io/github/license/KOLANICH/AptSourcesList.py.svg) [![PyPi Status](https://img.shields.io/pypi/v/AptSourcesList.svg)](https://pypi.python.org/pypi/AptSourcesList) [![TravisCI Build Status](https://travis-ci.org/KOLANICH/AptSourcesList.py.svg?branch=master)](https://travis-ci.org/KOLANICH/AptSourcesList.py) [![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/AptSourcesList.py.svg)](https://libraries.io/github/KOLANICH/AptSourcesList.py)
