'''
interrupt.py: provide an interruptible wait(...) and related utilities.

This module includes wait(...), a replacement for sleep(...) that is
interruptible and works with multiple threads.  It also provides methods to
cause an interruption (including doing it by issuing a ^C to the program),
check whether an interruption occurred, and other related operations.

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020-2022 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   deprecation import deprecated
import signal
import sys
import threading

if sys.platform == "win32":
    import win32api

if __debug__:
    from sidetrack import log

# This is needed to get the __version__ property.
import commonpy


# Global variables.
# .............................................................................

__waiter = threading.Event()
'''Internal state variable used to communicate that an interrupt occurred.'''

__exception = KeyboardInterrupt
'''Exception that will be raised when an interrupt signal is received.'''


# Main functions.
# .............................................................................

def config_interrupt(callback = None, raise_exception = KeyboardInterrupt,
                     on_signal = signal.SIGINT):
    '''Configure handling of interruptions.

    This function can be used to attach a signal handler that will do the
    following upon receipt of a designated signal:

      1. call interrupt(), defined elsewhere in this module
      2. optionally call the function "callback" given as argument
      3. raise the given "exception" (default: KeyboardInterrupt)

    Parameter "callback" assigns a function to be called after calling
    interrupt() when the signal is received.  If no value is given for
    "callback", no callback function is called.

    Parameter "raise_exception" determines the exception that is raised after
    calling the callback function.

    Parameter "signal" determines the signal to which the handler is bound.
    By default, signal.SIGINT is used, which is ^C on Unix-like systems.
    Note that changing this to something *other* than SIGINT means that ^C
    will then trigger the normal Python keyboard interrupt signal handling
    instead of invoking this signal handler.
    '''

    global __exception
    __exception = raise_exception

    def interrupt_handler(signum, frame = None):
        if __debug__: log('interrupt_handler invoked')
        interrupt()
        if callback:
            if __debug__: log(f'invoking callback {callback}')
            callback()
        if sys.platform == "win32":
            # Don't chain to next handler.
            return 1
        else:
            raise __exception

    if __debug__: log(f'setting handler on {on_signal}, exception {__exception}')
    if sys.platform == "win32":
        win32api.SetConsoleCtrlHandler(interrupt_handler, True)
    else:
        signal.signal(on_signal, interrupt_handler)


def wait(duration):
    '''Wait for "duration" seconds, in a way that can be interrupted.

    This is a replacement for sleep(duration).  If interrupted, this function
    raises the exception configured by a prior call to config_interrupt(...).

    This function calls reset() before it begins waiting.
    '''
    if interrupted():
        # It doesn't make sense to exit right away if we're called, so assume
        # a preexisting interrupt was left unreset accidentally.
        reset_interrupts()
    if __debug__: log(f'waiting for {duration} s')
    __waiter.wait(duration)
    if interrupted():
        if __debug__: log(f'raising {__exception}')
        raise __exception


def interrupt():
    '''Interrupt any waits and internally record an interrupt has occurred.'''
    if __debug__: log(f'interrupting wait')
    __waiter.set()


def interrupted():
    '''Return True if interrupt() has been called and not cleared.'''
    return __waiter.is_set()


def raise_for_interrupts():
    '''Check whether an interrupt occurred; if so, raise an exception.'''
    if interrupted():
        if __debug__: log(f'raising {__exception}')
        raise __exception


def reset_interrupts():
    '''Clear the internal marker that an interrupt occurred.'''
    if __debug__: log(f'clearing interrupt state')
    __waiter.clear()


@deprecated(deprecated_in = '1.7.0', removed_in = '2.0.0',
            current_version = commonpy.__version__,
            details = 'Use reset_interrupts() instead of reset()')
def reset():
    reset_interrupts()
