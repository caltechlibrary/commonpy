CommonPy<img width="12%" align="right" src="https://github.com/caltechlibrary/commonpy/raw/main/.graphics/commonpy-icon.png">
===============================================

This is a collection of common utility functions and classes that we at the Caltech Library have found useful in our other Python projects.

[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/commonpy.svg?style=flat-square&color=b44e88&label=Latest%20release)](https://github.com/caltechlibrary/commonpy/releases)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&color=lightgray&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/20056)](https://data.caltech.edu/records/20056)
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


### Data structures

The `data_structures` module provides miscellaneous data classes.

| Function              | Purpose |
|-----------------------|---------|
| `CaseInsensitiveDict` | A version of `dict` that compares keys in a case-insensitive manner |


### Data utilities

The `data_utils` module provides a number of miscellaneous simple functions for some common operations on data of various kinds.

| Function           | Purpose |
|--------------------|---------|
| `flattened(thing)` | Takes a list or dictionary and returns a recursively flattened version |
| `unique(list)`     | Takes a list and return a version without duplicates |
| `ordinal(integer)` | Returns a string with the number followed by "st", "nd, "rd", or "th" |
| `slice(list, n)`   | Yields `n` number of slices from the `list` |
| `timestamp()`      | Returns a string for an easily-readable form of the current time and date |
| `parsed_datetime(string)` | Returns a date object representing the given date string |
| `pluralized(word, n, include_num)`  | Returns a plural version of `word` if `n > 1` |
| `expanded_range(string)` | Given a string of the form "X-Y", returns the list of integers it represents |


### File utilities

The `file_utils` module provides a number of miscellaneous simple functions for some common operations on files and directories.

| Function           | Purpose |
|--------------------|---------|
| `readable(dest)`   | Returns `True` if file or directory `dest` is accessible and readable |
| `writable(dest)`   | Returns `True` if file or directory `dest` can be written |
| `nonempty(file)`   | Returns `True` if file `file` is not empty |
| `relative(file)`   | Returns a path string for `file` relative to the current directory |
| `filename_basename(file)` | Returns `file` without any extensions |
| `filename_extension(file)` | Returns the extension of filename `file` |
| `alt_extension(file, ext)` | Returns `file` with the extension replaced by `ext` |
| `rename_existing(file)` | Renames `file` to `file.bak` |
| `delete_existing(file)` | Deletes the given `file` |
| `copy_file(src, dst)` | Copies file from `src` to `dst` |
| `open_file(file)` | Opens the `file` by calling the equivalent of "open" on this system |
| `open_url(url)` | Opens the `url` in the user's default web browser |
| `filtered_by_extensions(list, endings)` | |
| `files_in_directory(dir, ext, recursive)` | |


### Interruptible wait and interruption handling utilities

The `interrupt` module includes `wait(...)`, a replacement for `sleep(...)` that is interruptible and works with multiple threads.  It also provides methods to cause an interruption (including doing it by issuing a <kbd>^C</kbd> to the program), check whether an interruption occurred, and other related operations.

| Function                 | Purpose |
|--------------------------|---------|
| `config_interrupt(callback, raise_ex, signal)` | Sets up a callback function |
| `wait(duration)`         | Waits for `duration` in an interruptible fashion |
| `interrupt()`            | Interrupts any `wait` in progress |
| `interrupted() `         | Returns `True` if an interruption has been called |
| `raise_for_interrupts()` | Raises an exception if `interrupt()` has been invoked |
| `reset_interrupts()`     | Resets the interruption flag |


### Module utilities

The `module_utils` collection of functions is useful for working with paths related to a running module, for example to find internal data files that might be needed for normal operation.

| Function           | Purpose |
|--------------------|---------|
| `desktop_path()`   | Returns the path to the user's Desktop directory on this system |
| `module_path(module_name)` | Returns the path to the installed module |
| `installation_path(module_name)` | Returns the path to module's installation directory |
| `datadir_path(module_name)` | Returns the path to the `/data` subdirectory of the module |
| `config_path(module_name)` | Returns the path to local config data directory for the module |

Function `config_path(...)` is useful to use in conjunction with Python's [`configparser`](https://docs.python.org/3/library/configparser.html) module.  It returns `~/.config/modulename/` on Unix-like systems.


### Network utilities

The `network_utils` module provides several functions that are useful when performing network operations.

| Function                         | Purpose                                                             |
| -------------------------------- | ------------------------------------------------------------------- |
| `download(url, local_dest)`      | Download a file                                                     |
| `download_file(url, local_dest)` | Download a file without raising exceptions                          |
| `hostname(url)`                  | Returns the hostname portion of a URL                               |
| `net(...)`                       | See below                                                           |
| `netlock(url)`                   | Returns the hostname, port number (if any), and login info (if any) |
| `network_available()`            | Returns `True` if external hosts are reacheable over the network    |
| `scheme(url)`                    | Returns the protocol portion of the url; e.g., "https"              |
| `on_localhost(url)`              | Returns `True` if the address of `url` points to the local host     |


#### _`net`_

The `net` function in the `network_utils` module implements a fairly high-level network operation interface that internally handles timeouts, rate limits, polling, HTTP/2, and more. The function signature is:

```python
net(method, url, client = None, handle_rate = True, polling = False, recursing = 0, **kwargs)
```

The `method` parameter should have a value such as `'get'`, `'post'`, `'head'`, or similar.  The function returns a tuple of (response, exception), where the first element is the response from the get or post HTTP call, and the second element is an exception object if an exception occurred.  If no exception occurred, the second element will be `None`.  This allows the caller to inspect the response even in cases where exceptions are raised.

If keyword `client` is not `None`, it's assumed to be a [Python HTTPX Client](https://www.python-httpx.org) object to use for the network call.  Settings such as timeouts should be done by the caller creating appropriately-configured [Client](https://www.python-httpx.org/api/#client) objects.

If keyword `handle_rate` is `True`, this function will automatically pause and retry if it receives an HTTP code 429 ("too many requests") from the server.  If `False`, it will return the exception `CommonPy.RateLimitExceeded` instead.

If keyword `polling` is `True`, certain statuses like 404 are ignored and the response is returned; otherwise, they are considered errors.  The behavior when `True` is useful in situations where a URL does not exist until something is ready at the server, and the caller is repeatedly checking the URL.  It is up to the caller to implement the polling schedule and call this function (with `polling = True`) as needed.

This method always passes the argument `allow_redirects = True` to the underlying Python HTTPX library network calls.


#### _`download` and `download_file`_

The functions `download(url, local_destination)` and `download_file(url, local_destination)` download a file at the given `url`, writing it to the file specified by the parameter `local_destination`. The former version of the function will raise exceptions in case of problems; the latter version simply return `True` or `False` depending on the success of the download.


### String utilities

| Function           | Purpose |
|--------------------|---------|
| `antiformat(s)`    | Quote instances of `{` and `}` in `s` so it can be passed to format. |
| `print_boxed(msg)` | Print a message with a box around it using pure ASCII characters. |


### System utilities

| Function           | Purpose |
|--------------------|---------|
| `system_profile()` | Returns a string describing the system running this Python program. |


### Exceptions

The CommonPy module defines a number of exceptions that it may return.  (Most of the exceptions are potentially thrown by `net`, discussed above.)

| Exception                | Meaning |
|--------------------------|---------|
| `CommonPyException`      | Base class for CommonPy exceptions |
| | |
| `ArgumentError`          | The function call was given invalid or unexpected arguments |
| `AuthenticationFailure`  | Problem obtaining or using authentication credentials |
| `InternalError`          | Unrecoverable problem involving CommonPy itself |
| `Interrupted`            | The user elected to cancel/quit the program |
| `NetworkFailure`         | Unrecoverable problem involving net | 
| `NoContent`              | No content found at the given location |
| `RateLimitExceeded`      | The service flagged reports that its rate limits have been exceeded |
| `ServiceFailure`         | Unrecoverable problem involving a remote service |


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/commonpy/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing CommonPy!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2020-2022, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

Mike Hucka started this collection of utilities sometime in 2018.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/toolbox/3030990/) of a toolbox, used as the icon for this repository, was created by [priyanka](https://thenounproject.com/term/toolbox/3030990) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

CommonPy makes use of numerous open-source packages, without which it would have been effectively impossible to develop CommonPy with the resources we had.  I want to acknowledge this debt.  In alphabetical order, the packages are:

* [boltons](https://github.com/mahmoud/boltons/) &ndash; package of miscellaneous Python utilities
* [dateparser](https://pypi.org/project/dateparser/) &ndash; parse dates in almost any string format
* [h2](https://pypi.org/project/h2) &ndash; HTTP/2 support library used by [HTTPX](https://www.python-httpx.org)
* [httpx](https://www.python-httpx.org) &ndash; Python HTTP client library that supports HTTP/2
* [humanize](https://github.com/jmoiron/humanize) &ndash; make numbers more easily readable by humans
* [ipdb](https://github.com/gotcha/ipdb) &ndash; the IPython debugger
* [pytest](https://docs.pytest.org/en/stable/) &ndash; testing framework for Python
* [python_dateutil](https://pypi.org/project/python-dateutil) &ndash; date utilities
* [PyYAML](https://pyyaml.org) &ndash; Python YAML parser
* [pywin32](https://github.com/mhammond/pywin32) &ndash; Windows APIs for Python
* [sidetrack](https://github.com/caltechlibrary/sidetrack) &ndash; simple debug logging/tracing package
* [tldextract](https://github.com/john-kurkowski/tldextract) &ndash; module to parse domains from URLs

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/commonpy/main/.graphics/caltech-round.png">
  </a>
</div>
