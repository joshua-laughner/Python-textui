from . import uierrorraise
from .context import pytui
from pytui import uierrors

uierrors.UIErrorWrapper.do_throw_both = True
uierrors.UIErrorWrapper.do_soft_exit = False
print "UIErrorNest"

def nested_error():
    uierrorraise.time_to_error()
    print ""
    print "Exiting normally"

nested_error()