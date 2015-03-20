#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import time

from RPi import GPIO


class observable(object):

    def __init__(self):
        self._listeners = []

    def register(self, listener):
        self._listeners.append(listener)

    def deregister(self, listener):
        self._listeners.remove(listener)

    def _broadcast(self, event):
        for listener in self._listeners:
            listener(event)


class matrix(observable):

    def __init__(self, rows, cols, keymap, mode=GPIO.BCM):

        num_keys = len(rows) * len(cols)
        assert len(keymap) == num_keys

        super(matrix, self).__init__()

        self._num_cols = len(cols)
        self._num_rows = len(rows)

        self._in_channels = rows
        self._out_channels = cols

        self._keymap = keymap
        self._keystate = [False] * num_keys
        self._pressed = [False] * num_keys
        self._released = [False] * num_keys

        self._sleep_millis = 10
        self.stop = False

        GPIO.setmode(mode)
        GPIO.setup(self._in_channels, GPIO.IN)
        GPIO.setup(self._out_channels, GPIO.OUT)
        atexit.register(GPIO.cleanup)

    def update(self):

        self.stop = False

        while not self.stop:

            # Activate all columns
            GPIO.output(self._out_channels, GPIO.LOW)

            # Check if some buttons have been pressed
            if any(GPIO.input(chan) for chan in self._in_channels):

                # Deactivate all columns
                GPIO.output(self._out_channels, GPIO.HIGH)

                index = 0

                # Update state of buttons
                for j in self._out_channels:

                    # Activate a specific column
                    GPIO.output(j, GPIO.LOW)

                    for i in self._in_channels:

                        state = not GPIO.input(i)

                        self._pressed[index] = not self._keystate[index] and state
                        self._released[index] = self._keystate[index] and not state
                        self._keystate[index] = state

                        index += 1

                    # Deactivate the specific column
                    GPIO.output(j, GPIO.HIGH)

                # Notify event listeners
                if any(self._keystate):
                    self._broadcast(self)

            else:
                time.sleep(self._sleep_millis / 1000.0)

    def keys_pressed(self):
        """
        Returns a list of keys currently pressed
        """
        return [self._keymap[idx]
                for idx, value in enumerate(self._keystate)
                if value and self._keymap[idx]]
