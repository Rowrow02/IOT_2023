# IOT_2023

To use this code a my_AIO file is required which has all of your personal information.

Copy/paste and change the following and drop in a file called 'my_AIO.py'
# my_AIO
``` python
import ubinascii
import machine
WIFI_SSID = "YOUR WIFI NAME"
WIFI_PASS = "YOUR PASSWORD" 

#Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883 
AIO_USER = "ACCOUNT NAME"
AIO_KEY = "ACCOUNT KEY"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  
AIO_LIGHTS_FEED = "FEED NAME LED LIGHT" 
AIO_RANDOMS_FEED = "FEED NAME TEMPERATURE"
```
