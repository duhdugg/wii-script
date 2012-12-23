#!/usr/bin/python2

import cwiid, uinput
from time import sleep
from cfg import pointed_global, super_mario, l4d2

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

    def ir_test(self):
        self.logger('Connecting Wiimote. Sync now.')
        wm = cwiid.Wiimote()
        self.logger('Wiimote connected.')
        self.set_leds(wm)
        self.set_report(wm)
        midpoint = (0, 0)
        distance = (0, 0)
        while True:
            point_1 = None
            point_2 = None
            sleep(0.05)
            try:
                point_1 = wm.state['ir_src'][0]['pos']
            except Exception:
                pass
            try:
                point_2 = wm.state['ir_src'][1]['pos']
            except Exception:
                pass
            if (not point_1) and (not point_2):
                continue
            elif point_1 and (not point_2):
                point_2 = ( (point_1[0] + distance[0]) , (point_1[1] + distance[1]) )
            elif point_2 and (not point_1):
                point_1 = ( (point_2[0] - distance[0]) , (point_2[1] - distance[1]) )
            midpoint = ( ((point_1[0] + point_2[0]) / 2.0) , ((point_1[1] + point_2[1]) / 2.0) )
            distance = ( (point_2[0] - point_1[0]) , (point_2[1] - point_1[1]) )
            hat_x = ( (512 - midpoint[0]) / 512.0 ) * 32767
            hat_y = ( (384 - midpoint[1]) / 384.0 ) * 32767
            self.logger(distance)

if __name__ == '__main__':
    def logger(msg):
        print(msg)
    main = MainProcess(logger)
    #main.test_config(sideways_game)
    main.print_status()
    #main.ir_test()
