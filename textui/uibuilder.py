from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
# If comparing to the int type becomes a compatibility issue, try this. Requires installing the builtins package for
# Python 2 (http://python-future.org/compatible_idioms.html)
# from builtins import int

from .uierrors import UIValueError, UITypeError, UICallbackError, UIErrorWrapper
from .uielements import user_input_date, user_input_value, user_input_list, user_input_yn, user_onoff_list

import pdb

class StopMainLoop(Exception):
    """
    Exception used by a menu to indicate that the program should stop the main loop
    """
    pass


class _MenuItem(object):
    @property
    def hide_if(self):
        return self._hide_if

    def __init__(self, name_in, callback_in, hide_if=None):
        self.name = name_in
        # This should be an instance of _CallBack
        self.callback = callback_in

        if hide_if is None:
            hide_if = lambda pgrm_data: False

        self._hide_if = hide_if


class _CallBack(object):
    def __init__(self, fxn, parent_menu, *args):
        self.return_fxn = fxn
        self.parent = parent_menu
        self.extra_fxns = args

    def execute(self, prog_data):
        for fxn in self.extra_fxns:
            fxn(prog_data)
        return self.return_fxn(prog_data)

    def get_menu_hierarchy(self):
        hierarchy = []
        #FIXME: this is supposed to trace the history of callbacks for a UICallbackError, but right now just loops infinitely
        raise NotImplementedError('get_menu_hierarchy is broken right now')

        next_menu = self.parent
        while next_menu is not None:
            hierarchy.insert(0, next_menu.name)

        return hierarchy


class Program(object):
    def __init__(self, main_menu, autostart=False, **program_data):

        self.data = program_data

        if type(main_menu) is not Menu:
            UIErrorWrapper.raise_error(UITypeError("main_menu must be an instance of Menu"))
        self.next_callback = _CallBack(main_menu.interact, None)

        if autostart:
            self.main_loop()

    def main_loop(self):
        while True:
            try:
                new_callback = self.next_callback.execute(self.data)
            except StopMainLoop:
                break

            if type(new_callback) is not _CallBack:
                UIErrorWrapper.raise_error(UICallbackError(self.next_callback))
            else:
                self.next_callback = new_callback


class Menu(object):
    @property
    def _last_item(self):
        if self.parent is None:
            label = 'Quit' if self._last_item_name_override is None else self._last_item_name_override
            return _MenuItem(label, _CallBack(self._quit_program, self))
        else:
            label = 'Back' if self._last_item_name_override is None else self._last_item_name_override
            return _MenuItem(label, _CallBack(self._up_one_level, self))

    @property
    def item_names(self):
        return [item.name for item in self.menu_items]

    @property
    def menu_items(self):
        # Add the last item on the fly so that if this menu gains a parent after instantiation the last menu item will
        # be correct - this is important if a menu is created first then attached to another menu
        return self._menu_items + [self._last_item]

    @property
    def children(self):
        return {c.name: c for c in self.menu_items[:-1]}

    def __init__(self, menu_name, parent=None, hard_quit=False, enter_hook=None, exit_hook=None, auto_exit=False,
                 last_item_name_override=None):
        """
        A multiple choice menu that links to other menus in a hierarchy.

        The Menu class is the core of the UIBuilder. It presents the user with a list of options, each of which is
        linked to an action. That may be another menu or a custom action.

        :param menu_name: The name of the menu, it will be displayed at the top of the list of options.
        :type menu_name: str

        :param parent: the parent menu instance, i.e. the menu that we should go back to when we're done with this menu.
         Optional; if not given, this menu is assumed to be the main menu, so instead of "return to previous menu", the
         last option will be "quit". This can be set later by assigning to the ``parent`` attribute.
        :type parent: `Menu`

        :param hard_quit: optional, controls what happens if this menu is the main menu and the user selects "quit". If
         this is False (default) then the program's main loop will just be exited, but Python will continue running.
         If this is True, then ``exit(0)`` will be called to quit Python completely.
        :type hard_quit: bool

        :param enter_hook: optional, a function that accepts one input (the program data, see `Program`) and optionally
         returns a boolean. This will be called before the menu is displayed, so it can be used to set up elements of
         the program data needed by the menu, check the program data, etc. If this function explicitly returns False,
         then the program will automatically return to the parent menu (or quit, if this was the main menu). Note:
         returning None in this case is the same as returning True, and this menu will display normally.
        :type enter_hook: function (1 argument)

        :param exit_hook: optional, a function that accepts one input (the program data, see `Program`) and, like
         ``enter_hook`` optionally returns a boolean. This is called after the user chooses to exit this menu. Similarly
         to ``enter_hook``, if this returns True or None, the menu exits normally, but if it returns False, we stay in
         this menu.
        :type exit_hook: function (1 argument)

        :param auto_exit: causes this menu to automatically return to the previous menu (or exit the program, if it is
         the main menu) after the user selects an option and returns to this menu - this usually only makes sense if
         none of the options are further sub menus.
        :type auto_exit: bool
        """
        self.name = menu_name
        self.parent = parent
        self._hard_quit = hard_quit
        self._auto_exit = auto_exit  # should this menu automatically exit after a choice is made once?
        self._trigger_auto_exit = False  # used to trigger auto exit when we return here
        self._last_item_name_override = last_item_name_override

        if enter_hook is None:
            enter_hook = lambda x: True
        if exit_hook is None:
            exit_hook = lambda x: True

        self._enter_hook = enter_hook
        self._exit_hook = exit_hook

        # If we are the child of another menu, then the final option
        # in the menu should be to go up one level. If we are the
        # top menu, then it should be to quit.
        self._menu_items = []

    def visible_menu_items(self, pgrm_data):
        """
        Get the list of menu items that are currently visible

        :param pgrm_data: the program data dictionary
        :type pgrm_data: dict

        :return: list of menu items
        :rtype: list of `_MenuItem`s
        """
        return [item for item in self.menu_items if not item.hide_if(pgrm_data)]

    def visible_item_names(self, pgrm_data):
        """
        Get the names of menu items currently visible

        :param pgrm_data: the program data dictionary
        :type pgrm_data: dict

        :return: list of menu item names
        :rtype: list of str
        """
        return [item.name for item in self.visible_menu_items(pgrm_data)]

    def interact(self, pgrm_data):
        """
        Main method to interact with the menu

        :param pgrm_data: the program data dictionary
        :type pgrm_data: dict

        :return: the next callback to execute
        """
        def call_hook(hook):
            result = hook(pgrm_data)
            if result is None:
                result = True
            return result

        # Auto-exit assumes that all the options in this menu automatically return to this menu - i.e. none of them are
        # sub menus themselves. We need the callback of the choice to execute, return us here, at which point we should
        # automatically go back up one level. We set the trigger when we return the choice callback, then it gets used
        # here to actually do the automatic exit.
        if self._trigger_auto_exit:
            self._trigger_auto_exit = False
            post_result = call_hook(self._exit_hook)
            if post_result:
                return self._last_item.callback

        pre_result = call_hook(self._enter_hook)
        if not pre_result:
            # TODO: should this trigger when coming from a child menu?
            return self._last_item.callback

        ind = user_input_list("\n=== {0} ===".format(self.name), self.visible_item_names(pgrm_data), returntype="index",
                              emptycancel=False)

        if ind == (len(self.visible_menu_items(pgrm_data)) - 1):
            # Only trigger the exit hook if we are going back to the previous menu or quitting
            post_result = call_hook(self._exit_hook)
            if post_result is None:
                post_result = True
        else:
            post_result = True

        if post_result:
            if self._auto_exit and ind < (len(self.visible_menu_items(pgrm_data)) - 1):
                self._trigger_auto_exit = True
            return self.visible_menu_items(pgrm_data)[ind].callback
        else:
            return _CallBack(self.interact, self)

    def _add_item(self, name, callback, hide_if=None):
        """
        _add_item is the internal method call used to add a menu item to this Menu.
        Using this in typical menu building is not recommended because it REQUIRES that
        your callback function return an instance of _Callback when it completes. This
        can add some flexibility (if you want to have a function go somewhere else than the
        calling Menu when it finishes) but requires you to take responsibility for that.

        :param name: the name of the menu item, as a string

        :param callback: a function which returns an instance of _Callback

        :param hide_if: optional, if given, must be a function that accepts one argument (the
         program data dict, see `Program`) and returns ``True`` if this submenu should be hidden,
         False otherwise.
        :return: none
        """
        if type(name) is not str:
            UIErrorWrapper.raise_error(UITypeError("name must be a string"))
        if not callable(callback) and not isinstance(callback, _CallBack):
            UIErrorWrapper.raise_error(UITypeError("callback must be a function or an instance of textui.uibuilder.Callback"))

        if isinstance(callback, _CallBack):
            callback_inst = callback
        else:
            callback_inst = _CallBack(callback, self)
        item = _MenuItem(name, callback_inst, hide_if=hide_if)

        self._menu_items.append(item)

    def add_submenu(self, submenu_title, menu_item_name=None, hide_if=None, **submenu_kwargs):
        """
        add_submenu creates a new instance of Menu with this Menu as the parent,
        adds it as the next-to-last option in this Menu, and returns the new instance of Menu.

        :param submenu_title: The title of the submenu, passed as the first argument to Menu()

        :param menu_item_name: optional, if given, will be used as the item name in the current
        menu, if not given, the submenu_title is used both as the menu title and the item name

        :param hide_if: optional, if given, must be a function that accepts one argument (the
         program data dict, see `Program`) and returns ``True`` if this submenu should be hidden,
         False otherwise.

        :return: instance of Menu
        """
        if not isinstance(submenu_title, str):
            UIErrorWrapper.raise_error(UITypeError("submenu_title must be a string"))

        if menu_item_name is None:
            menu_item_name = submenu_title
        elif not isinstance(menu_item_name, str):
            UIErrorWrapper.raise_error(UITypeError("menu_item_name must be a string, if given"))

        smenu = Menu(submenu_title, parent=self, **submenu_kwargs)
        self._add_item(menu_item_name, smenu.interact, hide_if=hide_if)
        return smenu

    def attach_submenu(self, submenu, menu_item_name=None, hide_if=None):
        """
        attach_submenu takes an existing instance of Menu and binds it as an option in this Menu.

        :param submenu: the Menu to attach to the current menu

        :param menu_item_name: if given, overrides the name used in the options list of this menu.
        If not given, the menu item is given the value of submenu.name

        :param hide_if: optional, if given, must be a function that accepts one argument (the
         program data dict, see `Program`) and returns ``True`` if this submenu should be hidden,
         False otherwise.

        :return: none
        """

        if not isinstance(submenu, Menu):
            UIErrorWrapper.raise_error(TypeError('submenu must be an instance of textui.uibuilder.Menu'))
        if menu_item_name is None:
            menu_item_name = submenu.name
        elif not isinstance(menu_item_name, str):
            UIErrorWrapper.raise_error(TypeError('menu_item_name must be a string'))

        if submenu.parent is not None:
            UIErrorWrapper.warn('While attaching menu "{0}" to "{1}": {0} already has a parent which will be overwritten'
                                .format(submenu.name, self.name))
        submenu.parent = self
        self._add_item(menu_item_name, submenu.interact, hide_if=hide_if)

    def add_setting_menu(self, submenu_title, setting_callback, setting_default=None, menu_item_name=None):
        raise NotImplementedError('Setting menus not implemented; may never be')

    def attach_custom_fxn(self, menu_item_name, callback_fxn, hide_if=None):
        """
        attach_custom_fxn is the usual way to add functions that actually DO SOMETHING to a menu,
        rather than adding a submenu.

        :param menu_item_name: the name that the item should have in the Menu, as a string

        :param callback_fxn: the function that should execute when this menu item is selected,
         it must accept one argument and return nothing.

        :param hide_if: optional, if given, must be a function that accepts one argument (the
         program data dict, see `Program`) and returns ``True`` if this submenu should be hidden,
         False otherwise.

        :return: none
        """
        if not isinstance(menu_item_name, str):
            UIErrorWrapper.raise_error(TypeError('menu_item_name must be a string'))
        if not callable(callback_fxn):
            UIErrorWrapper.raise_error(TypeError('callback_fxn must be a function'))

        self._add_item(menu_item_name, _CallBack(self.interact, self, callback_fxn), hide_if=hide_if)

    def _up_one_level(self, _):
        return _CallBack(self.parent.interact, self)

    def _quit_program(self, _):
        if self._hard_quit:
            exit(0)
        else:
            raise StopMainLoop('{name} says to stop the main program loop'.format(name=self.name))
