from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __builtin__ import int

from .uierrors import UIValueError, UITypeError, UICallbackError, UIErrorWrapper
from .uielements import user_input_date, user_input_value, user_input_list, user_input_yn, user_onoff_list

class _MenuItem(object):
    def __init__(self, name_in, callback_in):
        self.name = name_in
        # This should be an instance of _CallBack
        self.callback = callback_in

class _CallBack(object):
    def __init__(self, fxn, parent_menu):
        self.fxn = fxn
        self.parent = parent_menu

    def get_menu_hierarchy(self):
        hierarchy = []
        next_menu = self.parent
        while next_menu is not None:
            hierarchy.insert(0, next_menu.name)

        return hierarchy


class Program(object):
    def __init__(self, main_menu):
        if type(main_menu) is not Menu:
            UIErrorWrapper.raise_error(UITypeError("main_menu must be an instance of Menu"))
        self.next_callback = _CallBack("top", main_menu.interact)
        self.main_loop()

    def main_loop(self):
        while True:
            new_callback = self.next_callback.fxn()
            if type(new_callback) is not _CallBack:
                UIErrorWrapper.raise_error(UICallbackError(self.next_callback))
            else:
                self.next_callback = new_callback


class Menu(object):
    def __init__(self, menu_name, parent_in=None):
        self.name = menu_name
        self.parent = parent_in

        # If we are the child of another menu, then the final option
        # in the menu should be to go up one level. If we are the
        # top menu, then it should be to quit.
        self.menu_items = []
        if self.parent is None:
            self.add_item("Quit", self.quit_program())
        else:
            self.add_item("Up one level", self.up_one_level())

    def interact(self):
        ind = user_input_list("=== {0} ===".format(self.name),
                              self.__item_names(),
                              returntype="index")
        return self.menu_items[ind]

    def add_item(self, name, callback):
        if type(name) is not str:
            UIErrorWrapper.raise_error(UITypeError("name must be a string"))
        if not isinstance(callback, lambda : 0):
            UIErrorWrapper.raise_error(UITypeError("callback must be a function"))
        callback_inst = _CallBack(callback, self)
        item = _MenuItem(name, callback_inst)
        # The new item will be next to last (quit or go up one level is always last)
        self.menu_items.insert(-1, item)

    def __item_names(self):
        return [item.name for item in self.menu_items]

    def up_one_level(self):
        pass

    def quit_program(self):
        exit(0)