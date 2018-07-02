Introduction to textui
======================

.. include:: includes/std_includes.rst

``textui`` is a package intended to provide a simple to use but flexible
text-based menu system that is widely compatible with many different system.
A large part of my motivation for creating this package is that, as a scientist,
I'm often working via SSH or other terminal-based remote access to a computing
cluster, where a full-fledged GUI module like :mod:`tkinter` is not always
easy to use, and for applications where taking the time to write something
with :mod:`curses` is not worth it.

This package is divided into two parts:

:ref:`uielements-ref-label`: individual functions that prompt for and accept
user input.

:ref:`uibuilder-ref-label`: a collection of classes that can be used to build
a multi-level interlinked menu system.

All elements of ``textui`` work by printing directly to the terminal, so programs
using it do not require any kind of X11 forwarding to work across an SSH connection.