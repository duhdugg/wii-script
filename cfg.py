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
        """
        A list of uinput events that will be used by the configuration.
        Too see a full list of uinput events in a python shell:
            import uinput
            help(uinput.ev)
        You can also reference /usr/include/linux/input.h
        """
        return self.__event_list

    @event_list.setter
    def event_list(self, value):
        self.__event_list = value

    @event_list.deleter
    def event_list(self):
        del self.__event_list

    @property
    def position(self):
        """
        For future use, to automatically load configs based on controller position.
        """
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @position.deleter
    def position(self):
        del self.__position

    @property
    def active_process(self):
        """
        For future use, to automatically load configs based on running applications.
        """
        return self.__active_process

    @active_process.setter
    def active_process(self, value):
        self.__active_process = value

    @active_process.deleter
    def active_process(self):
        del self.__active_process


class Button:
    """
    Maps a Wiimote button to a joystick button or keypress event.
    """
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        button_state = '0'*16 + bin(wiimote_state['buttons']).replace('0b', '')
        if button_state[-1*len(self.wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, 1)
        else:
            uinput_device.emit(self.uinput_event, 0)

class NunButton:
    """
    Maps a nunchuk button to a joystick button or keypress event.
    """
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        if not 'nunchuk' in wiimote_state.keys():
            return 0
        else:
            button_state = '0'*16 + bin(wiimote_state['nunchuk']['buttons']).replace('0b', '')
            if button_state[-1*len(self.wiimote_button)] == '1':
                uinput_device.emit(self.uinput_event, 1)
            else:
                uinput_device.emit(self.uinput_event, 0)

class DPad:
    """
    Maps opposite points on a Wiimote DPad to represent an axis on a joystick.
    """
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
    """
    Maps shaking the Wiimote (in any direction) to a joystick button or keypress event.
    """
    def __init__(self, uinput_event, sensitivity):
        self.uinput_event = uinput_event
        self.sensitivity = sensitivity
        self.natural_state = 120
    def __call__(self, wiimote_state, uinput_device):
        shake = False
        for x in wiimote_state['acc']:
            delta = -1 * (self.natural_state - x)
            if delta > self.sensitivity:
                shake = True
        if shake:
            uinput_device.emit(self.uinput_event, 1)
        else:
            uinput_device.emit(self.uinput_event, 0)

class NunShakeButton:
    """
    Maps shaking the nunchuk (in any direction) to a joystick button or keypress event.
    """
    def __init__(self, uinput_event, sensitivity):
        self.uinput_event = uinput_event
        self.sensitivity = sensitivity
        self.natural_state = 140
    def __call__(self, wiimote_state, uinput_device):
        if not 'nunchuk' in wiimote_state.keys():
            return 0
        else:
            shake = False
            for x in wiimote_state['nunchuk']['acc']:
                delta = -1 * (self.natural_state - x)
                if delta > self.sensitivity:
                    shake = True
            if shake:
                uinput_device.emit(self.uinput_event, 1)
            else:
                uinput_device.emit(self.uinput_event, 0)

class ButtonAxis:
    """
    By pressing a Wiimote button, emulate a fully-pressed axis (ideally, gas or brake).
    """
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        button_state = '0'*16 + bin(wiimote_state['buttons']).replace('0b', '')
        if button_state[-1*len(self.wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, 32767)
        else:
            uinput_device.emit(self.uinput_event, 0)

class NunButtonAxis:
    """
    By pressing a nunchuk button, emulate a fully-pressed axis (ideally, gas or brake).
    """
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        if not 'nunchuk' in wiimote_state.keys():
            return 0
        else:
            button_state = '0'*16 + bin(wiimote_state['nunchuk']['buttons']).replace('0b', '')
            if button_state[-1*len(self.wiimote_button)] == '1':
                uinput_device.emit(self.uinput_event, 32767)
            else:
                uinput_device.emit(self.uinput_event, 0)



class MouseAccel:
    """
    Map the Wiimote accelerometer/gyroscope to the mouse.
    """
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

class IRJoystick:
    """
    Map the Wiimote infrared sensor to an absolute value on a joystick axis.
    """
    def __init__(self, index, mult, maxval, uinput_event):
        self.index = index
        self.mult = mult
        self.maxval = maxval
        self.uinput_event = uinput_event
        self.mid = 0
        self.dist = 0
    def __call__(self, wiimote_state, uinput_device):
        self.point = [None, None]
        try:
            self.point[0] = wiimote_state['ir_src'][0]['pos'][self.index]
        except Exception, e:
            pass
        try:
            self.point[1] = wiimote_state['ir_src'][1]['pos'][self.index]
        except Exception, e:
            pass
        if (self.point[0] == None) and (self.point[1] == None):
            return 0
        elif (self.point[0] != None) and (self.point[1] == None):
            self.point[1] = self.point[0] + self.dist
        elif (self.point[0] == None) and (self.point[1] != None):
            self.point[0] = self.point[1] - self.dist
        self.mid = (self.point[0] + self.point[1]) / 2.0
        self.dist = self.point[1] - self.point[0]
        hatval = int(( (self.maxval - self.mid) / self.maxval) * 32767 * self.mult)
        uinput_device.emit(self.uinput_event, hatval)

class NunStick:
    """
    Map the nunchuk control stick to a joystick axis.
    """
    def __init__(self, index, mult, uinput_event):
        self.index = index
        self.mult = mult
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        if not 'nunchuk' in wiimote_state.keys():
            return 0
        else:
            stickval = wiimote_state['nunchuk']['stick'][self.index]
            hatval = int( ((stickval - 127) / 100.0) * 32767 * self.mult)
            uinput_device.emit(self.uinput_event, hatval)

class ResetHat:
    """
    Map a Wiimote button to override the value of a hat to zero.
    Useful when IR goes wacky.
    """
    def __init__(self, wiimote_button, uinput_event):
        self.wiimote_button = bin(wiimote_button).replace('0b', '')
        self.uinput_event = uinput_event
    def __call__(self, wiimote_state, uinput_device):
        button_state = '0'*16 + bin(wiimote_state['buttons']).replace('0b', '')
        if button_state[-1*len(self.wiimote_button)] == '1':
            uinput_device.emit(self.uinput_event, 0)
        else:
            return 0

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

super_mario = Config(
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
                      ShakeButton(uinput.BTN_3, 40),
                     ],
                     'sideways',
                     'zsnes',
                     )
l4d2 = Config(
                [
                 IRJoystick(0, 1, 512.0, uinput.ABS_RX), # aim
                 IRJoystick(1, -1, 384.0, uinput.ABS_RY), # aim
                 Button(cwiid.BTN_2, uinput.BTN_1), # toggle scores
                 Button(cwiid.BTN_A, uinput.BTN_A), # use/menuAccept
                 Button(cwiid.BTN_B, uinput.BTN_B), # attack
                 DPad(cwiid.BTN_DOWN, cwiid.BTN_UP, uinput.ABS_HAT0Y), # spin, flash
                 DPad(cwiid.BTN_RIGHT, cwiid.BTN_LEFT, uinput.ABS_HAT0X), # weapons
                 Button(cwiid.BTN_MINUS, uinput.BTN_THUMBL), # vocalize
                 Button(cwiid.BTN_PLUS, uinput.BTN_THUMBR), # scoped zoom
                 Button(cwiid.BTN_HOME, uinput.BTN_START), # pause
                 ShakeButton(uinput.BTN_Y, 100), # reload
                 NunStick(0, 1, uinput.ABS_X), # strafe
                 NunStick(1, -1, uinput.ABS_Y), # walk
                 NunShakeButton(uinput.BTN_X, 110), # melee
                 NunButton(cwiid.NUNCHUK_BTN_Z, uinput.BTN_Z), # crouch
                 NunButton(cwiid.NUNCHUK_BTN_C, uinput.BTN_C), # jump
                 ResetHat(cwiid.BTN_1, uinput.ABS_RX), # reset IR joystick X axis
                 ResetHat(cwiid.BTN_1, uinput.ABS_RY), # reset IR joystick Y axis
                ],
                'pointed',
                'Left4Dead2',
                )
