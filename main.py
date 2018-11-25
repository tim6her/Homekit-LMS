"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal
import time

from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
import lmsquery

def connect_to_player_at_server(playername, hostname):
    """Connects to a Squeezbox player connected to a server by
    their name.

    Args:
        playername (string): name of player
        hostname (string): hostname of Squeezbox server

    Returns:
        pylms.player.Player
    """
    server = lmsquery.LMSQuery(hostname)

    players = [ply for ply in server.get_players() if
               ply['name'] == playername]
    if len(players) < 1:
        raise RuntimeError(('No player named %s connected to '
                            'server named %s') % (playername, hostname))
    return server, players[0]['playerid']

from accessories.LMS import LMS

logging.basicConfig(level=logging.INFO)


def get_bridge(driver):
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(driver, 'Bridge')
    temp_sensor = TemperatureSensor(driver, 'Sensor 2')
    temp_sensor2 = TemperatureSensor(driver, 'Sensor 1')
    bridge.add_accessory(temp_sensor)
    bridge.add_accessory(temp_sensor2)

    return bridge


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    server, player = connect_to_player_at_server('salonmaster', 'salonmaster')
    return LMS(server, player, driver, 'Salonmaster')

def homekit():
    # Start the accessory on port 51826
    driver = AccessoryDriver(port=51826)

    # Change `get_accessory` to `get_bridge` if you want to run a Bridge.
    driver.add_accessory(accessory=get_accessory(driver))

    # We want SIGTERM (kill) to be handled by the driver itself,
    # so that it can gracefully stop the accessory, server and advertising.
    signal.signal(signal.SIGTERM, driver.signal_handler)

    # Start it!
    driver.start()

   
while True:
    try:
        homekit()
    except:
        time.sleep(5)
    

