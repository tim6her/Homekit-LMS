# An Accessory mocking a temperature sensor.
# It changes its value every few seconds.
import random

from pyhap.accessory import Accessory
# FIXME This should be available in the future
# from pyhap.const import CATEGORY_SPEAKER 
CATEGORY_SPEAKER = 26

class LMS(Accessory):

    category = CATEGORY_SPEAKER

    def __init__(self, server, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        serv_pp = self.add_preload_service('Switch')
        self.char_pp = serv_pp.configure_char('On',
                                              setter_callback=self.set_mode)
        self.server = server
        self.player = player
        self.set_info_service(firmware_revision=None,
                              manufacturer='Myself',
                              model='Raspberry Pi 3, running Slimlibrary',
                              serial_number=None)

    @Accessory.run_at_interval(3)
    def run(self):
        self.char_pp.value = self._player_mode() == 'play'
        self.char_pp.notify()
    
    def set_mode(self, on):
        if on:
            self.server.query(self.player, 'play')
        else:
            self.server.pause(self.player)
    
    def _player_mode(self):
        return self.server.query(self.player, 'status')['mode']
        