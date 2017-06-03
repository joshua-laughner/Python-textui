"""
This module contains the low level text UI elements for the package pytui.

This module contains the functions that actually handle user input. Each function is
configured so that the user input occurs within a while True loop. Input checking is
done on the user input and the loop will not exit if an invalid value was given.

You are welcome to use these functions directly in your programs if you do not wish
to use the menu construct classes also provided in the pytui package.


"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __builtin__ import int

import datetime as dt
from jllutils import genutils
from .uierrors import UIErrorWrapper, UITypeError, UIValueError

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
     If false, the list of options will be represented if no answer given.
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
        userans = raw_input("Enter 1-{0}: ".format(len(options)))
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


def user_input_date(prompt, currentvalue=None, emptycancel=True):
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
    :return: A datetime.datetime instance, or None.
    """
    # TODO: use datetime strftime method
    # Prompts the user for a date in yyyy-mm-dd or yyyy-mm-dd HH:MM:SS format. Only input is a prompt describing
    # what the date is. Returns a datetime object. The currentvalue keyword can be used to display the current
    # setting, but it must be a datetime object as well. Returns none if user ever enters an empty string.
    if currentvalue is not None and type(currentvalue) is not dt.datetime and type(currentvalue) is not dt.date:
        UIErrorWrapper.raise_error(UITypeError("If given, currentvalue must be a datetime.date or datetime.datetime instance"))
    elif type(currentvalue) is dt.date:
        currentvalue = dt.datetime(currentvalue.year, currentvalue.month, currentvalue.day)
    if type(emptycancel) is not bool:
        UIErrorWrapper.raise_error(UITypeError("If given, emptycancel must be a bool"))

    print(prompt)
    print("Enter in the format yyyy-mm-dd or yyyy-dd-mm HH:MM:SS")
    print("i.e. both 2016-04-01 and 2016-04-01 00:00:00 represent midnight on April 1st, 2016")
    if emptycancel:
        print("Entering nothing will cancel")

    if currentvalue is not None:
        print("Current value is {0}".format(currentvalue))

    while True:
        userdate = raw_input("--> ")
        userdate = userdate.strip()
        if len(userdate) == 0:
            if emptycancel:
                return None
            else:
                print("You must enter a value")
                continue

        date_and_time = userdate.split(" ")
        date_and_time = [s.strip() for s in date_and_time]
        if len(date_and_time) == 1:
            # No time passed, set to midnight
            hour = 0
            min = 0
            sec = 0
        else:
            time = date_and_time[1].split(':')
            if len(time) != 3:
                print('Time component must be of form HH:MM:SS (three 2-digit numbers separated by colons')
                continue

            try:
                hour = int(time[0])
                min = int(time[1])
                sec = int(time[2])
            except ValueError:
                print("Error parsing time. Be sure only numbers 0-9 are used to define HH, MM, and SS")
                continue

        date = date_and_time[0].split("-")
        if len(date) != 3:
            print("Date component must be of form yyyy-mm-dd (4-, 2-, and 2- digits separated by dashed")
            continue

        try:
            yr = int(date[0])
            mn = int(date[1])
            dy = int(date[2])
        except ValueError:
            print("Error parsing date. Be sure only numbers 0-9 are used to define yyyy, mm, and dd.")
            continue

        # Take advantage of datetime's built in checking to be sure we have a valid date
        try:
            dateout = dt.datetime(yr,mn,dy,hour,min,sec)
        except ValueError, e:
            print("Problem with date/time entered: {0}".format(str(e)))
            continue

        # If we get here, nothing went wrong
        return dateout


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
            userans = raw_input("T/F: ").lower().strip()
            if userans == "t":
                return True
            elif userans == "f":
                return False
            elif len(userans) == 0:
                return None
            else:
                print("Option is a boolean. Must enter T or F.")
        else:
            userans = raw_input("--> ").strip()
            if len(userans) == 0 and emptycancel:
                return None
            elif len(userans) == 0 and not emptycancel:
                print("Cannot enter an empty value.")
            else:
                try:
                    userans = returntype(userans)
                except ValueError:
                    print("Could not convert your input to {0}, try again".format(genutils.typestr(returntype)))
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
        userans = raw_input(prompt + defstr + ": ")

        if userans == "":
            return defaultans
        elif userans.lower() == "y":
            return True
        elif userans.lower() == "n":
            return False
        else:
            print("Enter y or n only. ", end="")
