#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keypad

from RPi import GPIO

KEYMAP = [
    'C#', 'D', 'D#', 'E',
    'F#', 'G', 'G#', 'A',
    'A#', 'B', 'C2', None,
    'C1', 'F', None, None
]

NOTES = {
    'C1': 16.352,
    'C#': 17.324,
    'D': 18.354,
    'D#': 19.445,
    'E': 20.602,
    'F': 21.827,
    'F#': 23.125,
    'G': 24.500,
    'G#': 25.957,
    'A': 27.500,
    'A#': 29.135,
    'B': 30.868,
    'C2': 32.703
}

def note(key, octave=4):
    return NOTES[key] * (2 ** octave)


if __name__ == '__main__':
    kbd = keypad.matrix(rows=[15, 14, 25, 7],
                        cols=[8, 23, 24, 18],
                        keymap=KEYMAP,
                        mode=GPIO.BCM)

    # Piezo buzzer on GPIO-22
    GPIO.setup(22, GPIO.OUT)
    p = GPIO.PWM(22, 262)
    p.start(0)

    def key_handler(event):
        key_presses = event.keys_pressed()

        if key_presses:
            print key_presses
            for key in key_presses:
                p.ChangeDutyCycle(50)
                p.ChangeFrequency(note(key))
        else:
            p.ChangeDutyCycle(0)

    kbd.register(key_handler)
    kbd.update()
