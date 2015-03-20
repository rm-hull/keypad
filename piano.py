#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keypad

KEYMAP = [
    'C#', 'D', 'D#', 'E',
    'F#', 'G', 'G#', 'A',
    'A#', 'B', 'C2', None,
    'C1', 'F', None, None
]

def key_handler(event):
    print event.keys_pressed()


if __name__ == '__main__':
    kbd = keypad.matrix(rows=[15, 14, 25, 7],
                        cols=[8, 23, 24, 18],
                        keymap=KEYMAP)

    kbd.register(key_handler)
    kbd.update()
