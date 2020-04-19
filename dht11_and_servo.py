# code that prints temperature or humidity when user inputs TEMP or HUMD
# it also open or close servo when user inputs OPEN or CLOSE, activates relays depending on inputs such as STARTFAN STOPFAN
# this is has to be used entering the command: su root
# password: raspberry

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

# set pin 5 as output
GPIO.setup(5,GPIO.OUT)

while True:
    #reads humidity and temperature
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    user_input = input("Please enter any of the following commands: \n TEMP \n HUMD \n OPEN \n CLOSE \n STARTFAN \n STOPFAN: ")

    # if input is HUMD, prints humidity
    if(user_input == "HUMD"):
        if humidity is not None:
            print("Humidity = {} %".format(humidity))
        else:
            print("Sensor failure. Check wiring.")

    # if input is TEMP, prints temperature
    elif(user_input == "TEMP"):
        if temperature is not None:
            print("Temperature = {} °C".format(temperature))
        else:
            print("Sensor failure. Check wiring.")

    # if input is OPEN
    elif(user_input == "OPEN"):
        print("Opening...")
        for pulse in range(100, 220, 1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(delay_period)

    # if input is CLOSE
    elif(user_input == "CLOSE"):
        print("Closing...")
        for pulse in range(220, 100, -1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(delay_period)

    # if input is STARTFAN, turns on fan
    elif(user_input == "STARTFAN"):
        print("Starting Fan")
        GPIO.output(5,GPIO.HIGH)

    # if input is STOPFAN, turns off fan
    elif(user_input == "STOPFAN"):
        print("Stopping Fan")
        GPIO.output(5,GPIO.LOW)

    else:
        print("Unrecognized input")
        time.sleep(1)