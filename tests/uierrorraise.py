from .context import pytui
from pytui import uierrors

uierrors.UIErrorWrapper.do_throw_both = False
print "UIErrorRaise"

def time_to_error():
    print "do_throw_both = ", uierrors.UIErrorWrapper.do_throw_both
    uierrors.UIErrorWrapper.raise_error(ValueError("Hi"))

if __name__ == "__main__":
    time_to_error()

# To get these to work, they need to be run from the parent pytui directory with
# python -m tests.uierrorraise
# or whichever test function you wish to use.
