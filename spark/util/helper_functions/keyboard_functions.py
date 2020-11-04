from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...core import Core

from functools import reduce
from operator import and_
from ..decorators import *


def helper_handle_kb_event(self: Core, event):
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
        self._keys_held[self.key] = False
        if key_released:
            key_released()


@ignite_global
def helper_keys_held(self: Core, *keys, pattern=None):
    if pattern is None:
        pattern = [True]*len(keys)
    match = [self._keys_held.get(key, False) == want for key, want in zip(keys, pattern)]
    return reduce(and_, match)
