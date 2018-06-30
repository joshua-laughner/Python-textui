"""
This module contains the low level text UI elements for the package pytui.

This module contains the functions that actually handle user input. Each function is
configured so that the user input occurs within a while True loop. Input checking is
done on the user input and the loop will not exit if an invalid value was given.

You are welcome to use these functions directly in your programs if you do not wish
to use the menu construct classes also provided in the pytui package.


"""
from __future__ import print_function, division, absolute_import
# If comparing to the int type becomes a compatibility issue, try this. Requires installing the builtins package for
# Python 2 (http://python-future.org/compatible_idioms.html)
# from builtins import int

from collections import OrderedDict
import datetime as dt
import copy
import re
import sys

import pdb

from .uierrors import UIErrorWrapper, UITypeError, UIValueError


if sys.version_info.major == 2:
    text_input = raw_input
elif sys.version_info.major == 3:
    text_input = input
else:
    raise NotImplementedError('No text input function defined for Python version {}'.format(sys.version_info.major))


def user_input_list(prompt, options, returntype="value", currentvalue=None, emptycancel=True):
    """
    This function provides the user a list of choices to choose from, the user selects one by its number

    :param prompt: The text prompt to display for the user (type = str)
    :param options: The list of options to present (type = list or tuple)
    :param returntype: optional, can be "value" or "index", "value" is default.
    If set to "value", the return value will be the value of the option chosen. If
    set to "index", the return value will be the index of the list chosen.
    :param currentvalue: optional, defaults to None. Sets what the current value of
    this option is. If one is given, it will be marked with a * in the list.
    :param emptycancel: optional (type = bool), defaults to True. If true, then this
     function will return None if no answer is chosen (but not if an invalid selection
     is chosen). A message indicating that an empty answer will cancel is added to the prompt.
     If false, the list of options will be re-presented if no answer given.
    :return: either the value or index of the user choice (see returntype) or the type None.
    """

    # Input checking
    if type(prompt) is not str:
        UIErrorWrapper.raise_error(UITypeError("prompt must be a string"))
    if type(options) is not list and type(options) is not tuple:
        UIErrorWrapper.raise_error(UITypeError("options must be a list or tuple"))
    if type(returntype) is not str or returntype.lower() not in ["value", "index"]:
        UIErrorWrapper.raise_error(UITypeError("returntype must be one of the strings 'value' or 'index'"))
    if type(emptycancel) is not bool:
        UIErrorWrapper.raise_error(UITypeError("emptycancel must be a bool"))

    print(prompt)
    if emptycancel:
        print("A empty answer will cancel.")
    if currentvalue is not None:
        print("The current value is marked with a *")
    for i in range(1, len(options)+1):
        if currentvalue is not None and options[i-1] == currentvalue:
            currstr = "*"
        else:
            currstr = " "
        print("  {2}{0}: {1}".format(i, options[i-1], currstr))

    while True:
        userans = text_input("Enter 1-{0}: ".format(len(options)))
        if len(userans) == 0:
            if emptycancel:
                return None
            else:
                continue

        try:
            userans = int(userans)
        except ValueError:
            print("Input invalid")
        else:
            if userans > 0 and userans <= len(options):
                break

    if returntype.lower() == "value":
        return options[userans-1]
    elif returntype.lower() == "index":
        return userans - 1
    else:
        UIErrorWrapper.raise_error(UIValueError("Value '{0}' for keyword 'returntype' is not recognized".format(returntype)))


def user_input_date(prompt, currentvalue=None, emptycancel=True, req_time_part='day', smallest_allowed_time_part=None):
    """
    Request that the user input a date.

    :param prompt: A string printed as the prompt; it should describe what date is
    being requested.
    :param currentvalue: optional, datetime.date or datetime.datetime instance. If
    given, will print out the current value given. Useful when setting an option so
    that the user knows what the current value is.
    :param emptycancel: optional, defaults to True. A boolean determining whether an
    empty answer will cause this function to return None. If false, the user must enter
    a valid date to exit (not recommended for most cases).
    :param req_time_part: optional, defaults to 'day'. A string describing the largest
    required time part, must be one of: 'year', 'month', 'day', 'hour', 'minute', 'second'.
    If this is set to 'minute' for example, then the user must input at least year, month,
    day, hour, and minute, or it will be rejected.
    :param smallest_allowed_time_part: optional, defaults to None. A string describing
    the smallest piece of time the user is allowed to specify. Must be one of the same strings
    as allowed for req_time_part, and must be the same or smaller piece of time than req_time_part.
    For example, if this is set to 'minute', then the user may not include seconds in their
    answer. If left as None, then it will be automatically set to the same as req_time_part,
    effectively giving the user only one choice for how specific to make their time.
    :return: A datetime.datetime instance, or None.
    """

    # Prompts the user for a date in yyyy-mm-dd or yyyy-mm-dd HH:MM:SS format. Only input is a prompt describing
    # what the date is. Returns a datetime object. The currentvalue keyword can be used to display the current
    # setting, but it must be a datetime object as well. Returns none if user ever enters an empty string.
    if currentvalue is not None and type(currentvalue) is not dt.datetime and type(currentvalue) is not dt.date:
        UIErrorWrapper.raise_error(UITypeError("If given, currentvalue must be a datetime.date or datetime.datetime instance"))
    elif type(currentvalue) is dt.date:
        currentvalue = dt.datetime(currentvalue.year, currentvalue.month, currentvalue.day)

    if type(emptycancel) is not bool:
        UIErrorWrapper.raise_error(UITypeError("If given, emptycancel must be a bool"))

    # Must give the time formats as a list of tuples (instead of keyword-value pairs) to preserve order because
    # at least in Python 2 **kwargs becomes a regular dict() and so loses order before OrderedDict even sees it.
    time_formats = OrderedDict([('year', '%Y'), ('month', '%Y-%m'), ('day', '%Y-%m-%d'),
                                ('hour', '%Y-%m-%d %H'), ('minute', '%Y-%m-%d %H:%M'), ('second', '%Y-%m-%d %H:%M:%S')])
    if req_time_part not in time_formats:
        UIErrorWrapper.raise_error(UITypeError('req_time_part must be one of: {}'.format(', '.join(time_formats.keys()))))
    elif smallest_allowed_time_part not in time_formats and smallest_allowed_time_part is not None:
        UIErrorWrapper.raise_error(UITypeError('smallest_allowed_time_part must be one of: {}'.format(', '.join(time_formats.keys()))))
    else:
        key_ind = time_formats.keys().index(req_time_part)
        if smallest_allowed_time_part is None:
            smallest_ind = key_ind + 1
        else:
            smallest_ind = time_formats.keys().index(smallest_allowed_time_part)+1

        if smallest_ind <= key_ind:
            UIErrorWrapper.raise_error(UIValueError('req_time_part must be a larger piece of time than smallest_allowed_time_part'))
        allowed_time_fmts = time_formats.values()[key_ind:smallest_ind]
        allowed_fmts_str = ', '.join([_human_readable_time_format(fmt) for fmt in allowed_time_fmts])

    print(prompt)
    print("Enter in one of the formats: {}".format(allowed_fmts_str))
    print("Any omitted parts will be set to 0 or 1, as appropriate")
    if emptycancel:
        print("Entering nothing will cancel")

    if currentvalue is not None:
        print("Current value is {0}".format(currentvalue))

    while True:
        userdate = text_input("--> ")
        userdate = userdate.strip()
        if len(userdate) == 0:
            if emptycancel:
                return None
            else:
                print("You must enter a value")
                continue

        matching_fmt = None
        for fmt in allowed_time_fmts:
            if len(userdate) == len(_human_readable_time_format(fmt)):
                matching_fmt = fmt
                break

        if matching_fmt is None:
            print('Wrong number of characters. Allowed formats are: {}'.format(allowed_fmts_str))
            continue

        try:
            dateout = dt.datetime.strptime(userdate, matching_fmt)
        except ValueError:
            print('Cannot understand "{}" as "{}"'.format(userdate, matching_fmt))

        # If we get here, nothing went wrong
        return dateout


def _human_readable_time_format(fmt):
    translation_dict = {'%Y': 'yyyy', '%m': 'mm', '%d': 'dd', '%H': 'HH', '%M': 'MM', '%S': 'SS'}
    for k, v in translation_dict.items():
        fmt = fmt.replace(k, v)
    return fmt


def user_input_value(prompt, testfxn=None, testmsg=None, currval=None,
                     returntype=str, emptycancel=True):
    """
    Ask the user to input a value.

    :param prompt: The prompt to give the user as a string
    :param testfxn: optional, if given, should be a function that returns a boolean value.
    Used to test if the value the user gave is valid. This can be a pre-defined function
    or one created using the lambda syntax.
    :param testmsg: optional, if given, should be a message that describes the conditions
    required by testfxn
    :param currval: optional, the current value of the option. If given, the value will
    be printed after the prompt
    :param returntype: optional, must be a type which can be used as a function to convert
    a string to that type, e.g. int, bool, float, list. If the type is bool, this function
    will require the user to enter T or F (or nothing if emptycancel is True). If not given,
    the user input will be returned as a string.
    :param emptycancel: optional, must be a boolean, defaults to True. If True, then the user
    can enter an empty string, which will make this function return None.
    :return: The user input value as the type specified by returntype, or None is emptycancel
    is True and the user does not enter a value.
    """

    if type(prompt) is not str:
        UIErrorWrapper.raise_error(UITypeError("prompt must be a string"))
    if testfxn is not None and not isinstance(testfxn, type(lambda: 0)):
        # There does not seem to be a "function" type like there is an int or float type
        # so we'll just compare vs a simple lambda function. This should return true for
        # a lambda function or a defined function.
        UIErrorWrapper.raise_error(UITypeError("testfxn must be a function"))
    if testmsg is not None and type(testmsg) is not str:
        UIErrorWrapper.raise_error(UITypeError("testmsg must be a string"))
    if testmsg is None and testfxn is not None:
        UIErrorWrapper.warn("If you specify a testfxn but no testmsg it will not be clear to the user what is wrong")
    if type(emptycancel) is not bool:
        UIErrorWrapper.raise_error(UITypeError("If given, emptycancel must be a bool"))

    print(prompt)
    if currval is not None:
        print("The current value is {0}".format(currval))

    while True:
        if returntype is bool:
            userans = text_input("T/F: ").lower().strip()
            if userans == "t":
                return True
            elif userans == "f":
                return False
            elif len(userans) == 0:
                return None
            else:
                print("Option is a boolean. Must enter T or F.")
        else:
            userans = text_input("--> ").strip()
            if len(userans) == 0 and emptycancel:
                return None
            elif len(userans) == 0 and not emptycancel:
                print("Cannot enter an empty value.")
            else:
                try:
                    userans = returntype(userans)
                except ValueError:
                    print("Could not convert your input to {0}, try again".format(returntype.__name__))
                else:
                    return userans


def user_input_yn(prompt, default="y"):
    """
    Prompts the user with a yes/no question, returns True if answer is yes, False if answer is no.

    This is similar to user_input_value with a bool
    return type, but handles it differently if the user does not enter a
    value; this function will return the default value rather than a None type
    or forcing the user to enter something
    :param prompt: The prompt string that the user should be shown
    :param default: optional, must be either the string "y" or "n". Sets the
    default answer.
    :return: bool
    """

    if type(prompt) is not str:
        UIErrorWrapper.raise_error(UITypeError("prompt must be a string"))
    if type(default) is not str or default not in "YyNn":
        UIErrorWrapper.raise_error(UITypeError("default must be the string 'y' or 'n'"))

    while True:
        if default in "Yy":
            defstr = " [y]/n"
            defaultans = True
        else:
            defstr = " y/[n]"
            defaultans = False
        userans = text_input(prompt + defstr + ": ")

        if userans == "":
            return defaultans
        elif userans.lower() == "y":
            return True
        elif userans.lower() == "n":
            return False
        else:
            print("Enter y or n only. ", end="")


def user_onoff_list(prompt, options, currentstate=None, feedback_level=2):
    """
    Provides a list of toggleable options to the user
    Will print the prompt followed by the list of options provided. The user
    can interactively toggle each option on or off.
    :param prompt: A string prompting the user what to do. Will be followed
    by further instructions on what user inputs are valid.
    :param options: A list or tuple of strings of the option names
    :param currentstate: optional, a list of bools that describe the current
     state of the options (on or off). If not given, all default to False.
     Must be the same length as options. Is shallow copied internally so it
     will not change the values in the calling function.
    :param feedback_level: optional, an integer describing how much feedback
    to give the user. Defaults to 2, meaning that this function will print
    out what user input it could not parse. Set to 0 to turn this off (1
    reserved against future intermediate levels of feedback).
    :return: a list of bools with the new states of the options, or None if
    the user cancels.
    """
    if type(prompt) is not str:
        UIErrorWrapper.raise_error(UITypeError("prompt must be a string"))
    if type(options) is not list and type(options) is not tuple:
        UIErrorWrapper.raise_error(UITypeError("options must be a list or tuple"))
    elif not all([type(x) is str for x in options]):
        UIErrorWrapper.raise_error(UITypeError("options must be a list or tuple of strings"))
    if currentstate is None:
        currentstate = [False]*len(options)
    elif type(currentstate) is not list or not all([type(x) is bool for x in currentstate]):
        UIErrorWrapper.raise_error(UITypeError("currentstate must be a list of bools, if given"))
    elif len(currentstate) != len(options):
        UIErrorWrapper.raise_error(UIValueError("currentstate must be the same length as options, if given"))
    else:
        # Do not allow this function to modify the state in the calling workspace
        currentstate = copy.copy(currentstate)

    prompt += "\nEnter the number or multiple numbers separated by a space to toggle,\n" \
        "'all' to toggle all, 'on' to set all on, 'off' to set all off,\n" \
        "'a' to accept, or 'c' to cancel.\n" \
        "Active options are marked with a *:"

    print(prompt)
    while True:
        for i in range(len(options)):
            if currentstate[i]:
                state_str = "[*]"
            else:
                state_str = "[ ]"
            print("{0}: {1} {2}".format(i+1, options[i], state_str))

        user_ans = text_input("(Type 'm' to see initial message again) --> ")
        opt_inds = []
        bad_opts = []
        if user_ans.lower() == "m":
            print("")
            print(prompt)
            continue
        elif user_ans.lower() == "a":
            return currentstate
        elif user_ans.lower() == "c":
            return None
        elif user_ans.lower() == "all":
            # Python3 range compatible
            opt_inds = range(len(options))
        elif user_ans.lower() == "on":
            opt_inds = [i for i in range(len(options)) if not currentstate[i]]
        elif user_ans.lower() == "off":
            opt_inds = [i for i in range(len(options)) if currentstate[i]]
        else:
            user_ans = re.split("\s+", user_ans)
            for u in user_ans:
                try:
                    opt = int(u)-1
                except ValueError as err:
                    # If the input cannot be parsed as an int, move on
                    bad_opts.append(u)
                else:
                    if opt >= 0 and opt < len(options):
                        opt_inds.append(opt)
                    else:
                        bad_opts.append(u)

        if feedback_level > 1 and len(bad_opts) > 0:
            print("Could not parse {0},\n"
                  "out of range or not a number".format(", ".join(bad_opts)))

        for i in opt_inds:
            currentstate[i] = not currentstate[i]
