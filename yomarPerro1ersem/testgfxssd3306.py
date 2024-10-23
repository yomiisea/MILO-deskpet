# Complete project details at https://RandomNerdTutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

from machine import Pin, I2C
import ssd1306
from time import sleep
import gfx

# ESP32 Pin assignment
i2c = I2C(-1,scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

graphics = gfx.GFX(oled_width, oled_height, oled.pixel)



while True:

  oled.text("Texto prueba 1", 0, 0)
  oled.text("Texto prueba 2", 0, 16)
  oled.text("Texto prueba 3", 0, 32)
  oled.text("Texto prueba 4", 0, 48)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.line(0, 0, 127, 64, 1)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.rect(10, 16, 50, 30, 1)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.fill_rect(10, 16, 50, 30, 1)
  oled.show()
  sleep(1)
  oled.fill(0)


  graphics.circle(64, 32, 10, 1)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.fill_circle(64, 32, 10, 1)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.triangle(10,10,55,20,5,40,1)
  oled.show()
  sleep(1)
  oled.fill(0)

  graphics.fill_triangle(10,10,55,20,5,40,1)
  oled.show()
  sleep(1)
  oled.fill(0)
  