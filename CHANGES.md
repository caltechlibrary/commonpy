# Change log for CommonPy

## Version 1.8.2

This version merely changes a version dependency in `requirements.txt`. No other changes.


## Version 1.8.1

Changes in this release:

* At some point between versions 0.18 and 0.21.1 (current version), the `httpx` package changed the keyword argument named `allow_redirects` to `follow_redirects`, and our `network_utils` module functions broke as a result. This release updates `network_utils` to account for the change.
* The `requirements.txt` file now pins most dependencies to a specific version, to avoid situations where getting a newer version of a package might break existing code.
* The copyright year has been updated in various files.


## Version 1.8.0

This version introduces the `data_structures` module, and a new class, `CaseFoldDict`.


## Version 1.7.3

Changes in this release:

* Fixed a missing f-string in an exception message, plus guarded a few more exception message strings with `antiformat`.
* Added `CITATION.cff` file.
* Updated the `Makefile`.


## Version 1.7.2

Improve `flattened` to handle lists of dict keys.


## Version 1.7.1

Add missing `deprecation` package to `requirements.txt`.


## Version 1.7.0

Changes in this release:

* Beginning with this release, the function `reset()` is deprecated in favor of the function `reset_interrupts()`. 
* The function `wait()` resets the interrupt state before it begins waiting.


## Version 1.6.3

This release fixes some unexpected failures in `flattened(...)`.


## Version 1.6.2

This release expands `flattened(...)` to deal with iterators and generators.


## Version 1.6.1

This release fixes a bug in version 1.6.0.


## Version 1.6.0

This release adds the new function `flattened(...)`


## Version 1.5.0

This release adds the new function `print_boxed(...)`.


## Version 1.4.0

Changes in this version:
* In `net(...)`, in case of a connection error, don't do exponential back-off and retry. Retry only once and then give up, because connection errors often mean the server is not available and long waits are unhelpful to callers.
* Change `net(...)` to not test if a network is available if the given destination address is on the local host. This prevents incorrectly returning `NetworkFailure` when the current host is detached from the network and the failure is actually a `ServiceFailure` (for example, if nothing is listening on the destination port on the local host).
* Add new function `on_localhost(...)`, for testing whether a given network location indicates the local host.

Note: the previous release, 1.3.10, should not have added new functions in a patch release &ndash; API changes should result in changing the minor release number, not merely the patch number. The previous release number was a mistake; it should have been 1.4.0, but since it wasn't, this release is 1.4.0.


## Version 1.3.10

* Add new functions `download(...)` and `download_file(...)`.


## Version 1.3.9

* Don't import packages `dateparser` and `validator_collection` until actually necessary, to reduce application startup times.


## Version 1.3.8

* Fix problems on Windows involving the interrupt handler configured by `config_interrupt(...)`. First, the internal function used did not have a signature that was correct for `win32api.SetConsoleCtrlHandler` on Windows. Second, the proper usage is to return a value, not raise an exception.


## Version 1.3.7

* Make `relative(...)` from `file_utils` more robust against a problem on Windows, in which Python's `os.path.relpath` generates an error when you try to use it on a network-mapped drive.


## Version 1.3.6

* Fix missing `requirements.txt` entry for `pywin32` on Windows.


## Version 1.3.5

* Fix reference to missing function called by `relative(...)`.


## Version 1.3.4

* Fix undefined exceptions in network_utils due to a missing import.


## Version 1.3.3

* Fix broken references to os.path functions.


## Version 1.3.2

* Add a check for a common mistake in parameters to `net(...)`.


## Version 1.3.1

* Remove reference to HTTPX exception `RequestBodyUnavailable`, which no longer seems to exist in current versions of the HTTPX package.
* Remove use of exception `UserCancelled` in `network_utils.py`, because its definition no longer existed elsewhere and on review it seemed unecessary in the context where it was used.


## Version 1.3.0

* Fixed issue #2: httpx Timeout needs a default value.
* Bump the required version of [httpx](https://www.python-httpx.org) to 0.16.
* Changed name `filter_by_extension(...)` to `filtered_by_extension(...)` to follow the style of other functions that return values.
* Made trivial changes to the Makefile


## Version 1.2.0

* Added new function `config_path(...)`
* Added more unit tests


## Version 1.1.1

This version makes `antiformat(...)` more robust against values that are not strings, by applying `str(...)` to the incoming value.


## Version 1.1.0

This version adds a start at a module of string utilities, and introduces `antiformat(..)`: a function that will quote instances of `{` and `}` braces in a string so that the string can be passed safely to `format`.


## Version 1.0.0

* Rename a few functions to follow a more consistent naming convention.
* Update `requirements.txt` file.
* Add more documentation.
* Call this a 1.0.0 release.


## Version 0.0.7

* Fix bug in `filename_basename(...)`.
* Improve `plural(...)` by using `pluralize(...)` from [Boltons](https://github.com/mahmoud/boltons) package.
* Remove tests for removed module http_code.
* Miscellaneous other minor fixes and tweaks.


## Version 0.0.6

* Add a new module, `network_utils`.
* Start a collection of exceptions that may be returned by this package.
* Add additional dependency requirements to `requirements.txt`.


## Version 0.0.5

* Add a new module, `module_utils`.
* Add functions to the `file_utils` module.
* The package `__init__.py` file no longer imports the individual modules.  (Users are expected to use the approach `from commonpy.modulename import functionname`.)


## Version 0.0.4

Changed the order of arguments to function `config_interrupt` in the `interrupt` module to be in a more convenient order for most use cases.


## Version 0.0.3

This release adds the module `interrupt`.  This module includes `wait(...)`, a replacement for `sleep(...)` that is interruptible and works with multiple threads.  It also provides methods to cause an interruption (including doing it by issuing a <kbd>^C</kbd> to the program), check whether an interruption occurred, and other related operations.


## Version 0.0.2

Fixed some issues with the `README.md` file and started adding some documentation about the functions.


## Version 0.0.1

First release of various utilities developed for other Caltech Library projects over the last couple of years.
