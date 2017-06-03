from .context import pytui
from pytui import uierrors

def time_to_warn():
    print "do_throw_both = ", uierrors.UIErrorWrapper.do_throw_both
    uierrors.UIErrorWrapper.warn("Danger will robinson")

if __name__ == "__main__":
    time_to_warn()