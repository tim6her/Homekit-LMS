# An Accessory mocking a temperature sensor.
# It changes its value every few seconds.
import random

from pyhap.accessory import Accessory
# FIXME This should be available in the future
# from pyhap.const import CATEGORY_SPEAKER 
CATEGORY_SPEAKER = 26


class LMS(Accessory):

    category = CATEGORY_SPEAKER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

    @Accessory.run_at_interval(3)
    def run(self):
        self.char_temp.set_value(random.randint(18, 26))