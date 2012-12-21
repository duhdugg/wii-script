#!/usr/bin/python2

import cwiid
import uinput

class Config:
    def __init__(self, event_list, position, active_process):
        self.event_list = event_list
        self.position = position
        self.active_process = active_process

    @property
    def event_list(self):
        return self.__event_list

    @event_list.setter
    def event_list(self, value):
        self.__event_list = value

    @event_list.deleter
    def event_list(self):
        del self.__event_list

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @position.deleter
    def position(self):
        del self.__position

    @property
    def active_process(self):
        return self.__active_process

    @active_process.setter
    def active_process(self, value):
        self.__active_process = value

    @active_process.deleter
    def active_process(self):
        del self.__active_process


class Button:
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        button_state = '0'*16 + bin(wiimote_state['buttons']).replace('0b', '')
        if button_state[-1*len(self.wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, 1)
        else:
            uinput_device.emit(self.uinput_event, 0)

class DPad:
    def __init__(self, wiimote_button, opposite_wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.opposite_wiimote_button = bin(opposite_wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        button_state = '0'*16 + bin(wiimote_state['buttons']).replace('0b', '')
        if button_state[-1*len(self.wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, 32767)
        elif button_state[-1*len(self.opposite_wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, -32767)
        else:
            uinput_device.emit(self.uinput_event, 0)

class ShakeButton:
    def __init__(self, uinput_event):
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        natural_state = 120
        shake = False
        for x in wiimote_state['acc']:
            delta = -1 * (natural_state - x)
            if delta > 40:
                shake = True
        if shake:
            uinput_device.emit(self.uinput_event, 1)
        else:
            uinput_device.emit(self.uinput_event, 0)

class MouseAccel:
    def __init__(self, index, uinput_event, rate, sensitivity):
        self.index = index
        self.uinput_event = uinput_event
        self.rate = rate
        self.sensitivity = sensitivity
    def __call__(self, wiimote_state, uinput_device):
        natural_state = 120
        acc_state = wiimote_state['acc']
        r = self.rate
        s = self.sensitivity
        change = (-1*r) * ((natural_state - acc_state[self.index]) / s)
        uinput_device.emit(self.uinput_event, change)

sideways_game = Config(
                     [
                      Button(cwiid.BTN_1, uinput.BTN_1),
                      Button(cwiid.BTN_2, uinput.BTN_2),
                      Button(cwiid.BTN_A, uinput.BTN_A),
                      Button(cwiid.BTN_B, uinput.BTN_B),
                      DPad(cwiid.BTN_LEFT, cwiid.BTN_RIGHT, uinput.ABS_HAT0Y),
                      DPad(cwiid.BTN_DOWN, cwiid.BTN_UP, uinput.ABS_HAT0X),
                      Button(cwiid.BTN_PLUS, uinput.BTN_GEAR_UP),
                      Button(cwiid.BTN_MINUS, uinput.BTN_GEAR_DOWN),
                      Button(cwiid.BTN_HOME, uinput.BTN_0),
                      ShakeButton(uinput.BTN_3),
                     ],
                     'sideways',
                     'game',
                     )

pointed_global = Config(
                    [
                     MouseAccel(0, uinput.REL_X, 2, 5),
                     MouseAccel(1, uinput.REL_Y, 2, 5),
                     Button(cwiid.BTN_A, uinput.BTN_LEFT),
                     Button(cwiid.BTN_B, uinput.BTN_RIGHT),
                    ],
                    'pointed',
                    'global',
                    )
