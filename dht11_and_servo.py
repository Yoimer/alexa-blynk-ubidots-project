# code that prints temperature or humidity when user inputs TEMP or HUMD
# it also open or close servo when user inputs OPEN or CLOSE
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

while True:
    #reads humidity and temperature
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    # prompts user for input
    user_input = input("Please enter TEMP or HUMD or OPEN or CLOSE: ")

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
    else:
        print("Unrecognized input, enter TEMP or HUMD or OPEN or CLOSE: ")