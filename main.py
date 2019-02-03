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

#Make the changes here
WIFI_SSID = 'xxxxxx'                     #<--------Replace with your WIFI SSID
WIFI_PASSWORD = 'xxxxxxxxxx'             #<--------Replace with your WIFI PASSWORD
INSTAGRAM_ACCESS_TOKEN = '9472xxxxxxx.2exxxx6a.00da7a4b1xxxxxxxxxxxxxx' #<-------- Get your's from Instagram
UPDATE_INTERVAL = 300000                 #<--------Update interval in ms. 300000ms/5min is optimal

#Configuring Instagram API
uri = 'https://api.instagram.com/v1/users/self/?access_token='
uri += INSTAGRAM_ACCESS_TOKEN

#configuring I2C
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

#Notification LED
notify = Pin(2, Pin.OUT)
notify.value(1)

def notification():
    notify.value(0)
    utime.sleep_ms(500)
    notify.value(1)

#Display initial Welcome message
display.sleep(False)
display.fill(0)
display.text('MicroFollowers', 10, 25, 1)
display.show()

#Configuring WIFI
station = network.WLAN(network.STA_IF)
station.active(True)

if station.isconnected() != True:
    station.connect(WIFI_SSID, WIFI_PASSWORD)
    utime.sleep_ms(8000)
    ip = station.ifconfig()
    display.fill(0)
    display.text(ip[0], 10, 25, 1)
    display.show()
    print(ip)

    if station.isconnected() != True:
        print("Failed to connect! Check your WIFI credentials.")
        display.fill(0)
        display.text("Bad WIFI.",25, 25, 1)
        display.show()

else:
    print("Already Configured\n")
    ip = station.ifconfig()
    display.fill(0)
    display.text(ip[0], 15, 25, 1)
    display.show()
    print(ip)

old_followers = urequests.get(uri)
if old_followers.status_code == 200:
    notification()
    init_followers = old_followers.json()
    old_followers = init_followers.get('data').get('counts').get('followed_by')
    username = init_followers.get('data').get('username')
    display.fill(0)
    display.text(username, 0, 25, 1)
    display.show()
    utime.sleep_ms(1000)

extra_followers = 0

#Fetching Instagram API
while True:
    new_followers = urequests.get(uri)

    if new_followers.status_code == 200:
        notification()
        new_followers = new_followers.json()
        new_followers = new_followers.get('data').get('counts').get('followed_by')
        print(new_followers)

        extra_followers = int(new_followers) - int(old_followers)
        old_followers = int(new_followers)

        if extra_followers >= 0:
            display.fill(0)
            display.text(str(new_followers) + "  " + str(extra_followers) + "+", 25, 25, 1)
            display.show()
            utime.sleep_ms(UPDATE_INTERVAL)

        else:
            display.fill(0)
            display.text(str(new_followers) + "  " + str(-1 * extra_followers) + "-", 25, 25, 1)
            display.show()
            utime.sleep_ms(UPDATE_INTERVAL)

    #The below else function does nothing since 'timeout' in urequest is not yet implemented!! If notification
    #lED is not blinking after UPDATE_INTERVAL then their is problem with your internet connection.
    else:
        display.fill(0)
        display.text("No internet", 25, 25, 1)
        display.show()
        utime.sleep_ms(60000)
        notification()
        utime.sleep_ms(500)
        notification()







