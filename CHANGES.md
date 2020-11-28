Change log for CommonPy
=======================

Version 1.1.0
-------------

This version adds a start at a module of string utilities, and introduces `antiformat(..)`: a function that will quote instances of `{` and `}` braces in a string so that the string can be passed safely to `format`.


Version 1.0.0
-------------

* Rename a few functions to follow a more consistent naming convention.
* Update `requirements.txt` file.
* Add more documentation.
* Call this a 1.0.0 release.


Version 0.0.7
-------------

* Fix bug in `filename_basename(...)`.
* Improve `plural(...)` by using `pluralize(...)` from [Boltons](https://github.com/mahmoud/boltons) package.
* Remove tests for removed module http_code.
* Miscellaneous other minor fixes and tweaks.


Version 0.0.6
-------------

* Add a new module, `network_utils`.
* Start a collection of exceptions that may be returned by this package.
* Add additional dependency requirements to `requirements.txt`.


Version 0.0.5
-------------

* Add a new module, `module_utils`.
* Add functions to the `file_utils` module.
* The package `__init__.py` file no longer imports the individual modules.  (Users are expected to use the approach `from commonpy.modulename import functionname`.)


Version 0.0.4
-------------

Changed the order of arguments to function `config_interrupt` in the `interrupt` module to be in a more convenient order for most use cases.


Version 0.0.3
-------------

This release adds the module `interrupt`.  This module includes `wait(...)`, a replacement for `sleep(...)` that is interruptible and works with multiple threads.  It also provides methods to cause an interruption (including doing it by issuing a <kbd>^C</kbd> to the program), check whether an interruption occurred, and other related operations.


Version 0.0.2
-------------

Fixed some issues with the `README.md` file and started adding some documentation about the functions.


Version 0.0.1
-------------

First release of various utilities developed for other Caltech Library projects over the last couple of years.
