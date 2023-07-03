
import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Conversions between binary data and various encodings
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import random                 # Random number generator
from machine import Pin       # Define pin
import dht

#apin = machine.ADC(27)
#sf = 3.3/65535 
tempsensor = dht.DHT11(Pin(27))
#volt_per_adc = 3.3/4095

# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000    # milliseconds
last_random_sent_ticks = 0  # milliseconds
led = Pin("LED", Pin.OUT)   # led pin initialization for Raspberry Pi Pico W
 
# Wireless network
WIFI_SSID = "Folksam fiendservice"
WIFI_PASS = "Villejhahjelp" # No this is not our regular password. :)

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883 
AIO_USER = "roro02"
AIO_KEY = "aio_AaZz56KLQlAvLIptS0wDm7F3g2sA"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = "roro02/feeds/lights"
AIO_RANDOMS_FEED = "roro02/feeds/random"

# END SETTINGS



# FUNCTIONS

# Function to connect Pico to the WiFi
def do_connect():
    import network
    from time import sleep
    import machine
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode

    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(WIFI_SSID, WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip 



# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        led.on()                 # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        led.off()                # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.

# Function to generate a random number between 0 and the upper_bound
def random_integer(upper_bound):
    return random.getrandbits(32) % upper_bound

def measure_temp():
    tempsensor.measure()
    
    #adcVal = apin.read_u16()
    #millivolts = adcVal * sf
    
    temp = tempsensor.temperature()
    hum = tempsensor.humidity()
    #temp = millivolts/(10/1000)
    print( temp, hum)

    return temp
    
 
def send_temp():
    global last_random_sent_ticks
    global RANDOMS_INTERVAL
    if ((time.ticks_ms() - last_random_sent_ticks) < RANDOMS_INTERVAL):
        return; # Too soon since last one sent.
    temp = measure_temp()

    print("Publishing: {0} to {1} ... ".format(temp, AIO_RANDOMS_FEED), end='')
    try:
        client.publish(topic=AIO_RANDOMS_FEED, msg=str(temp))
        print("DONE")
    except Exception as e:
        print("FAILED")
    finally:
        last_random_sent_ticks = time.ticks_ms()
     


# Try Wi0Fi Connection
try:
    ip = do_connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_LIGHTS_FEED))



try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever
        client.check_msg()# Action a message if one is received. Non-blocking.
        send_temp()     # Send a random number to Adafruit IO if it's time.
        
        
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    print("Disconnected from Adafruit IO.")

print("done")

#while True:
#for i in range(10):
 # millivolts = apin.read_u16()
#  adc_12b = millivolts*sf
#  volt = adc_12b * volt_per_adc
#
#  dx = abs(50-0)
#  dy = abs(0-0.5)
#  shift = volt - 0.5
#  temp = shift / (dy/dx)
  
#  print(temp)
  
#  time.sleep(1)

