from lcus_relay import Relay

import logging

_LOGGER = logging.getLogger(__name__)

class Buzzer:
    def __init__(self, serial_port):
        self._relay = Relay(serial_port)

    def press(self):
        self._relay.turn_on()

    def release(self):
        self._relay.turn_off()
