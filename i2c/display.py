from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
import time

import psutil
import subprocess
import re

from PIL import ImageFont
from animated_gif import play_for

console_font = ImageFont.truetype("font/prospero.ttf", 16)
# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

interface = psutil.net_if_addrs()['wlan0'][0]
last = []
last_ip = None

def get_w_ip(output):
    matches = re.findall(r'(?:\d{1,3}.){3}\d{1,3}', output)
    return matches

def show(stats, vspace=12, spacing=12, pad_top=0):
    with canvas(device) as draw:
        for i, key in enumerate(stats):
            value = stats[key]
            draw.text((0,i*vspace+pad_top), key, fill='white')
            draw.text((spacing, i*vspace+pad_top), ': '+str(stats[key]), fill='white')

if __name__ == '__main__':
    play_for(gif='columbia.gif', no_loop=True, scale=50)
    while True:
        ip_addr = interface.address
        # ssh_connections = re.findall(r'\((.*)\)', subprocess.check_output(['who']).decode())
        ssh_connections = get_w_ip(subprocess.check_output(['w','-h']).decode())
        new = list(set(ssh_connections).difference(set(last)))
        if last_ip is None:
            last_ip = ssh_connections[-1] if len(ssh_connections) else 'NIL'
        else:
            last_ip = new[-1] if len(new)>0 else last_ip
        
        if len(new):
            play_for(gif='dokkaebi.gif', time=5, scale=-200)
        last = ssh_connections[:]
        stats = {"IP":ip_addr, "SESSIONS":len(ssh_connections), "LAST":last_ip}
        show(stats, spacing=55, pad_top=10)

        time.sleep(1)
