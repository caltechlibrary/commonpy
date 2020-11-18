Change log for Commonpy
=======================

Version 0.0.3
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
