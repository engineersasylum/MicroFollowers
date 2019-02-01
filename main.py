# MicroPython SH1106 OLED driver
#
# Pin Map I2C
#   - 3v - xxxxxx   - Vcc
#   - G  - xxxxxx   - Gnd
#   - D2 - GPIO 4   - SCK / SCL
#   - D1 - GPIO 5   - DIN / SDA
#   - D0 - GPIO 16  - Res (required, unless a Hardware reset circuit is connected)
#   - G  - xxxxxx     CS
#   - G  - xxxxxx     D/C
#
# Pin's for I2C can be set almost arbitrary
#
from machine import Pin, I2C
import network
import utime
import urequests
import sh1106

#configuring I2C
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

#Display initial Welcome message
display.sleep(False)
display.fill(0)
display.text('MicroFollowers', 10, 25, 1)
display.show()
utime.sleep_ms(4000)

#Configuring WIFI
station = network.WLAN(network.STA_IF)
station.active(True)

if station.isconnected() != True:
    station.connect('Xperia','blackfly21')
    utime.sleep_ms(5000)
    ip = station.ifconfig()
    display.fill(0)
    display.text(ip[0], 10, 25, 1)
    display.show()
    print(ip)

    if station.isconnected() != True:
        print("Failed to connect! Check your WIFI credentials.")

else:
    print("Already Configured\n")
    ip = station.ifconfig()
    display.fill(0)
    display.text(ip[0], 15, 25, 1)
    display.show()
    print(ip)

old_followers = 0
extra_followers = 0

#Fetching Instagram API
while True:

    insta_data = urequests.get('https://api.instagram.com/v1/users/self/?access_token=9472412125.679123c.3fb31b5968414e47b3b02c7b8101d17d')
    insta_data = insta_data.json()
    new_followers = insta_data.get('data').get('counts').get('followed_by')
    print(new_followers)

    extra_followers = int(new_followers) - old_followers
    old_followers = int(new_followers)

    display.fill(0)
    display.text(str(new_followers) + " " + str(extra_followers), 20, 25, 1)
    display.show()

    utime.sleep_ms(180000)


