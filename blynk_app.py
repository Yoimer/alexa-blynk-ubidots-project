import blynklib
# import blynklib_mp as blynklib # micropython import

BLYNK_AUTH = 'jHyhGi70lQWdU37_u0Xu96oY3aQYqXSn' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

# Servo Control
import time
import wiringpi
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
delay_period = 0.01

# DHT11
import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27

# gpio libraries
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set pin 5 as output (FAN)
GPIO.setup(5,GPIO.OUT)

# set pin 6 as output (OUTDOOR LIGHT)
GPIO.setup(6,GPIO.OUT)

# set pin 13 as output (LIVING ROOM LIGHT)
GPIO.setup(13,GPIO.OUT)

# set pin 19 as output (BED ROOM LIGHT)
GPIO.setup(19,GPIO.OUT)

# set pin 26 as output (KITCHEN LIGHT)
GPIO.setup(26,GPIO.OUT)

# set pin 12 as output (AC)
GPIO.setup(12,GPIO.OUT)

# set pin 16 as output (KETTEL)
GPIO.setup(16,GPIO.OUT)

# register handler for Virtual Pin V0 reading by Blynk App.
# when a widget in Blynk App asks Virtual Pin data from server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about read virtual pin event to hardware
# this notification captured by current handler 

# shows temperature in app
# 2 seconds in app
@blynk.handle_event('read V0')
def read_temperature(pin):
    # reads temperature and humidity
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
        temperature = str(temperature)
        print("Temperature = {} °C".format(temperature))
        # Example: get sensor value, perform calculations, etc
        # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, temperature)

# shows humidity in app
# 1 second in app
@blynk.handle_event('read V1')
def read_humidity(pin):
    # reads temperature and humidity
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None:
        humidity = str(humidity)
        print("Humidity = {} %".format(humidity))
        # Example: get sensor value, perform calculations, etc
        # send value to Virtual Pin and store it in Blynk Cloud 
        blynk.virtual_write(pin, humidity)

# control FAN relay (pin 5)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V2 write event
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Stopping Fan")
        GPIO.output(5,GPIO.LOW)
    elif value == ['1']:
        print("Starting Fan")
        GPIO.output(5,GPIO.HIGH)

# contrl OUTDOOR LIGHT (pin 6)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V3 write event
@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning Outdoor Light ON")
        GPIO.output(6,GPIO.LOW)
    elif value == ['1']:
        print("Turning Outdoor Light ON")
        GPIO.output(6,GPIO.HIGH)

# control LIVING ROOM LIGHT (pin 13)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V4 write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning Living Room Light OFF")
        GPIO.output(13,GPIO.LOW)
    elif value == ['1']:
        print("Turning Living Room Light ON")
        GPIO.output(13,GPIO.HIGH)

# control BED ROOM LIGHT (pin 19)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V5 write event
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning Bed Room Light OFF")
        GPIO.output(19,GPIO.LOW)
    elif value == ['1']:
        print("Turning Bed Room Light ON")
        GPIO.output(19,GPIO.HIGH)

# control KITCHEN LIGHT (pin 26)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V6 write event
@blynk.handle_event('write V6')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning Kitchen Light OFF")
        GPIO.output(26,GPIO.LOW)
    elif value == ['1']:
        print("Turning Kitchen Light ON")
        GPIO.output(26,GPIO.HIGH)

# control AC (pin 12)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V6 write event
@blynk.handle_event('write V7')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning AC OFF")
        GPIO.output(12,GPIO.LOW)
    elif value == ['1']:
        print("Turning AC ON")
        GPIO.output(12,GPIO.HIGH)

# control KETTEL (pin 16)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V6 write event
@blynk.handle_event('write V8')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Turning Kettel OFF")
        GPIO.output(16,GPIO.LOW)
    elif value == ['1']:
        print("Turning Kettel ON")
        GPIO.output(16,GPIO.HIGH)

# control servo - open - close (pin 18)
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
# register handler for virtual pin V9 write event
@blynk.handle_event('write V9')
def write_virtual_pin_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == ['0']:
        print("Closing Servo...")
        for pulse in range(220, 100, -1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(delay_period)
    elif value == ['1']:
        print("Opening Servo...")
        for pulse in range(100, 220, 1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(delay_period)

# main loop that starts program and handles registered events
while True:
    blynk.run()