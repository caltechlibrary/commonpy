Commonpy: useful Python functions and utilities
===============================================

This is a collection of common utility functions and classes that we at the Caltech Library have found useful in our other Python projects.

[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/commonpy.svg?style=flat-square&color=b44e88&label=Latest%20release)](https://github.com/caltechlibrary/commonpy/releases)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&color=gray&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/1677)](https://data.caltech.edu/records/1677)
[![PyPI](https://img.shields.io/pypi/v/commonpy.svg?style=flat-square&color=orange)](https://pypi.org/project/commonpy/)

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

This module provides a number of miscellaneous simple functions for some common operations on data of various kinds.

| Function           | Purpose |
|--------------------|---------|
| `unique(list)`     | Take a list and return a version without duplicates |
| `ordinal(integer)` | Return a string with the number followed by "st", "nd, "rd", or "th" |
| `slice(list, n)`   | Yield `n` number of slices from the `list` |
| `timestamp()`      | Return a string for an easily-readable form of the current time and date |
| `parse_datetime(string)` | Return a date object representing the given date string |
| `plural(word, n)`  | Simple function return a plural version of `word` if `n > 1` |
| `expand_range(string)` | Given a string of the form "X-Y", return the list of integers it represents |


### `file_utils`

This module provides a number of miscellaneous simple functions for some common operations on files and directories.

| Function           | Purpose |
|--------------------|---------|
| `readable(dest)`   | Return `True` if file or directory `dest` is accessible and readable |
| `writable(dest)`   | Return `True` if file or directory `dest` can be written |
| `nonempty(dest)`   | Return `True` if file `dest` is not empty |
| `relative(file)`   | Return a path string for `file` relative to the current directory |
| `filename_basename(file)` | Return `file` without any extensions |
| `filename_extension(file)` | Return the extension of filename `file` |
| `alt_extension(file, ext)` | Return `file` with the extension replaced by `ext` |
| `rename_existing(file)` | Rename `file` to `file.bak` |
| `delete_existing(file)` | Delete the given `file` |
| `copy_file(src, dst)` | Copy file from `src` to `dst` |
| `open_file(file)` | Open the `file` by calling the equivalent of "open" on this system |
| `open_url(url)` | Open the `url` in the user's default web browser |
| `filter_by_extensions(item_list, endings)` | |
| `files_in_directory(dir, ext, recursive)` | |


### `interrupt`

This module includes `wait(...)`, a replacement for `sleep(...)` that is interruptible and works with multiple threads.  It also provides methods to cause an interruption (including doing it by issuing a <kbd>^C</kbd> to the program), check whether an interruption occurred, and other related operations.


### `module_utils`

| Function           | Purpose |
|--------------------|---------|
| `module_path(module_name)` | Return the path to the installed module |
| `installation_path(module_name)` | Return the path to module's installation directory |
| `datadir_path(module_name)` | Return the path to the `/data` subdirectory of the module |


### `network_utils`

### `system_utils`

| Function           | Purpose |
|--------------------|---------|
| `system_profile()` | Return a string describing the system running this Python program. |


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
