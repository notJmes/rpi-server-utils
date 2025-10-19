from luma.core.interface.serial import i2c, spi, pcf8574
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010


serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
