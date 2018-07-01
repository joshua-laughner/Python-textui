.. _uielements-ref-label:

uielements
==========

.. include:: includes/std_includes.rst

.. automodule:: pytui.uielements

Usage
*****

This module contains two groups of functions: `standard interactive functions`_
and `optional input functions`_. The former is for cases where you always want
to query user input, the second is for cases where you *may* need to query user
input if a particular value is not given programmatically.

Examples
********

The standard interactive functions are generally pretty straightforward. Here is an
example using :func:`user_input_date` (lines beginning with ``$`` are the code, the
others are printed by Python)::

    $ user_date = user_input_date('Enter the first date to load data for')
    Enter the first date to load data for
    Enter in one of the formats: yyyy-mm-dd
    Entering nothing will cancel
    --> 2017-01-01

    $ user_date
    datetime.datetime(2017, 1, 1, 0, 0)


As you can see, this asks the user to input a date in a standard format and then returns
that as a :class:`datetime.datetime` object.

One possible "gotcha" is hinted at by the line "Entering nothing will cancel". For most of the
``user_input`` functions, if the user presses <Enter> without entering anything, the function
will immediately return a ``None``.  Most of them can override this with the ``emptycancel``
keyword, which will force the user to enter something. In general, these functions are written
with the idea that the encapsulating program will handle the return of ``None`` as a signal to
gracefully stop, or otherwise handle the fact that the user does not know what to enter.

Here is an example case where you might use one of the optional input functions,
in this case :func:`opt_user_input_value`::

    def read_data_from_file(filename=None):
        filename = opt_user_input_value('Enter the name of the file to open',
                                        filename,
                                        is_valid_test=os.path.isfile,
                                        invalid_msg='That is not a valid filename')
        with open(filename, 'r') a fobj:
            ...

You could imagine ``read_data_from_file`` being a function called early on in a larger
program that loads some data file so that the rest of the program can access it. In
this case, we allow the path of the file to be given in two ways:

1. As an argument to the ``read_data_from_file`` function

2. Interactively, through the ``opt_user_input_value`` function

The standard behavior of all the "opt" functions is that if the value (the second argument)
is ``None``, then it assumes that the value was not given and so should ask the user to provide
it interactively (this criteria can be overridden with the ``do_ask_test`` keyword). In this case,
we also want to ensure that, whichever way the filename is given, that it is a valid file, so
we give ``is_valid_test=os.path.isfile``. This means that either ``filename`` (if not ``None``) or
the user's input will be given to ``os.path.isfile``, which must return ``True`` for that value to
be accepted. This ensures consistent testing of both function inputs and user inputs.

For the "opt" functions that call "user_input" functions that may return ``None`` if the user doesn't
enter anything, the "opt" functions will, by default, raise a :class:`pytui.uierrors.UIOptNoneError`.
This behavior can be overridden with the ``error_on_none`` keyword.

Member functions
****************

Standard interactive functions
------------------------------

.. autofunction:: pytui.uielements.user_input_date
.. autofunction:: pytui.uielements.user_input_list
.. autofunction:: pytui.uielements.user_input_value
.. autofunction:: pytui.uielements.user_input_yn
.. autofunction:: pytui.uielements.user_onoff_list

Optional input functions
------------------------

.. autofunction:: pytui.uielements.opt_user_input_date
.. autofunction:: pytui.uielements.opt_user_input_list
.. autofunction:: pytui.uielements.opt_user_input_value
.. autofunction:: pytui.uielements.opt_user_input_yn
.. autofunction:: pytui.uielements.opt_user_onoff_list