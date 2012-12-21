#!/usr/bin/python2

import cwiid, uinput
from time import sleep
from cfg import pointed_global, sideways_game

class MainProcess:
    def __init__(self, logger):
        self.logger = logger

    def set_leds(self, wm):
        wm.led = 15
        wm.rumble = 1
        sleep(0.1)
        wm.rumble = 0

    def set_report(self, wm):
        wm.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN | cwiid.RPT_EXT | cwiid.RPT_IR | cwiid.RPT_STATUS

    def test_config(self, config):
        self.logger('Connecting Wiimote. Sync now.')
        wm = cwiid.Wiimote()
        self.logger('Wiimote connected.')
        self.set_leds(wm)
        self.set_report(wm)
        inputs = []
        for event in config.event_list:
            inputs.append(event.uinput_event)
        js = uinput.Device(inputs)
        while True:
            sleep(0.01)
            for event in config.event_list:
                event(wm.state, js)
        wm.close()
        return None

    def print_status(self):
        self.logger('Connecting Wiimote. Sync now.')
        wm = cwiid.Wiimote()
        self.logger('Wiimote connected.')
        self.set_leds(wm)
        self.set_report(wm)
        while True:
            sleep(0.1)
            self.logger(wm.state)

if __name__ == '__main__':
    def logger(msg):
        print(msg)
    main = MainProcess(logger)
    #main.test_config(sideways_game)
    main.print_status()
