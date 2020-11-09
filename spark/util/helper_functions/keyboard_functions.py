from __future__ import annotations
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from ...core import Core

from functools import reduce
from operator import and_
from ..decorators import *

_phys_to_typed = {
    "Backquote": ('`', '~'),
    "Digit1": ('1', '!'),
    "Digit2": ('2', '@'),
    "Digit3": ('3', '#'),
    "Digit4": ('4', '$'),
    "Digit5": ('5', '%'),
    "Digit6": ('6', '^'),
    "Digit7": ('7', '&'),
    "Digit8": ('8', '*'),
    "Digit9": ('9', '('),
    "Digit0": ('0', ')'),
    "Minus": ('-', '_'),
    "Equal": ('=', '+'),
    "BracketLeft": ('[', '{'),
    "BracketRight": (']', '}'),
    "Backslash": ('\\', '|'),
    "Semicolon": (';', ':'),
    "Quote": ('\'', '"'),
    "Comma": (',', '<'),
    "Period": ('.', '>'),
    "Slash": ('/', '?')
}


def helper_handle_kb_event(self: Core, event: Dict[str, str]):
    self.refresh_last_activity()
    key_pressed = self._methods.get("key_pressed", None)
    key_released = self._methods.get("key_released", None)
    key_repeated = self._methods.get("key_repeated", None)
    self.key = event['key']

    if event['type'] == "keydown":
        if not event['repeat']:
            self._keys_held[self.key] = True
            if key_pressed:
                key_pressed()
        else:
            if key_repeated:
                key_repeated()
    else:
        if event['code'].isalpha() and len(event['code']) == 1:
            self._keys_held[event['code'].lower()] = False
            self._keys_held[event['code'].upper()] = False
        elif event['code'] in _phys_to_typed:
            for k in _phys_to_typed[event['code']]:
                self._keys_held[k] = False
        else:
            self._keys_held[self.key] = False
        if key_released:
            key_released()


@ignite_global
def helper_keys_held(self: Core, *keys, pattern=None):
    if pattern is None:
        pattern = [True]*len(keys)
    match = [self._keys_held.get(key, False) == want for key, want in zip(keys, pattern)]
    return reduce(and_, match)
