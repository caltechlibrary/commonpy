Commonpy: useful Python functions and utilities
===============================================

This is a collection of common utility functions and classes that we at the Caltech Library have found useful in our other Python projects.

[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/handprint.svg?style=flat-square&color=b44e88&label=Latest%20release)](https://github.com/caltechlibrary/handprint/releases)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

This repository does not constitute a single program; instead, it contains a collection of modules with utility functions and classes that we have found ourselves using repeatedly in other Python projects.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `commonpy` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `commonpy` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install commonpy
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `commonpy` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/commonpy.git
```


Usage
-----

The basic approach to using this package is to import the modules and functions you need.  For example:

```python
from commonpy.file_utils import readable

if readable('/path/to/some/file'):
    # do something
```

The following subsections describe the different modules available.

### `data_utils`

### `file_utils`

### `http_code`

### `system_utils`



Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/sidetrack/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Commonpy!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2020, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

Mike Hucka started this collection of utilities sometime in 2018.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/commonpy/main/.graphics/caltech-round.png">
  </a>
</div>
