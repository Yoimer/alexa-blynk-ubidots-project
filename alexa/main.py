import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from flask import Flask
import json
import requests

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# DHT11
import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27

# list where fan states will be saved
save_fan_state = []
# first index equal 0
save_fan_state.append(0)

# list where outdoor_light states will be saved
save_outdoor_light_state = []
# first index equal
save_outdoor_light_state.append(0)

# gpio libraries
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set pin 5 as output (FAN)
GPIO.setup(5,GPIO.OUT)

# set pin 6 as output (OUTDOOR LIGHT)
GPIO.setup(6,GPIO.OUT)

######################################
# Skill name: derby uni project
# Invocation Name : derby uni project

##########launch skill##########
# voice commands are:
#Alexa, start derby uni project
#Alexa, open derby uni project
#Alexa, begin derby uni project
#Alexa, derby uni project
#Alexa, load derby uni project
#Alexa, run derby uni project
#Alexa, use derby uni project
#Alexa, tell derby uni project (This one makes no sense for the context of this skill. It works
                            # if invoking though)

##########launch skill##########
@ask.launch
# read welcome message from template.yaml file
def launch_app():
    welcome_msg = render_template('welcome')
    prompt = 'Which option do you prefer man?'
    return question(welcome_msg).reprompt(prompt).simple_card('Welcome to derby uni project', welcome_msg)

@ask.intent("TemperatureIntent")
# get temperature from sensor
def temperature():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
        print("Temperature = {} °C".format(temperature))
        return statement("Temperature value is {} Celsius degrees".format(temperature))
    else:
        print("Sensor failure. Check wiring.")
        return statement("Sensor failure. Please check wiring.")

@ask.intent("HumidityIntent")
# get humidity from sensor
def humidity():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None:
        print("Humidity = {} %".format(humidity))
        return statement("Humidity value is {} Percentage".format(humidity))
    else:
        print("Sensor failure. Check wiring.")
        return statement("Sensor failure. Please check wiring.")

@ask.intent("StartFanIntent")
# turns fan on
def turnsfanon():
    if(save_fan_state[0] == 1):
        print("Fan is already ON. Not action taken.")
        return statement("Fan is already ON. Not action taken.")
    else:
        save_fan_state[0] = 1
        print("Starting Fan")
        GPIO.output(5,GPIO.HIGH)
        return statement("Turning fan on")

@ask.intent("StopFanIntent")
# turns fan off
def turnsfanoff():
    if(save_fan_state[0] == 0):
        print("Fan is already OFF. Not action taken.")
        return statement("Fan is already OFF. Not action taken.")
    else:
        save_fan_state[0] = 0
        print("Stopping Fan")
        GPIO.output(5,GPIO.LOW)
        return statement("Turning fan off")


@ask.intent("StartOutDoorLightIntent")
# turns Outdoor Light on
def outdoorlighton():
    if(save_outdoor_light_state[0] == 1):
        print("Outdoor Light is already ON. Not action taken.")
        return statement("Outdoor Light is already ON. Not action taken.")
    else:
        save_outdoor_light_state[0] = 1
        print("Turning Outdoor Light ON")
        GPIO.output(6,GPIO.HIGH)
        return statement("Turning Outdoor Light ON")

@ask.intent("StopOutDoorLightIntent")
# turns Outdoor Light off
def outdoorlightoff():
    if(save_outdoor_light_state[0] == 0):
        print("Turning Outdoor Light OFF")
        return statement("Outdoor Light is already OFF. Not action taken.")
    else:
        save_outdoor_light_state[0] = 0
        print("Stopping Outdoor Light")
        GPIO.output(6,GPIO.LOW)
        return statement("Turning Outdoor Light off")

# stop
@ask.intent("AMAZON.StopIntent")
# stops the skill
def stop():
    return statement("Stopping the skill")

# if user does not match any intent, system goes here
@ask.intent("AMAZON.FallbackIntent")
def fallback():
    fallback_msg = 'I can not help you with that, try any of the options available for this app'
    return statement(fallback_msg)

# ask for help when welcoming or anytime
@ask.intent("AMAZON.HelpIntent")
def help():
    help_msg = "Ok, I am going to help you... I can tell you the temperature value or turn on the fan. Which option do you prefer?"
    reprompt_msg  = 'Please, tell me do you want me to give the temperature value of want to turn on fan?'
    #return statement(help_msg)
    return question(help_msg).reprompt(reprompt_msg)

# cancel intent
@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement("Cancelling the skill. Thanks for using")

# session ending
@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')