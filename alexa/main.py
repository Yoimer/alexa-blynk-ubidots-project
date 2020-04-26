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

# list where livingroom_light_state  will be saved
save_livingroom_light_state = []
# first index equal 0
save_livingroom_light_state.append(0)

# list where save_bedroom_light_state  will be saved
save_bedroom_light_state = []
# first index equal 0
save_bedroom_light_state.append(0)

# list where save_kitchen_light_state will be saved
save_kitchen_light_state = []
# first index equal 0
save_kitchen_light_state.append(0)

# list where save_ac_statee will be saved
save_ac_state = []
# first index equal 0
save_ac_state.append(0)

# list where save_kettel_state will be saved
save_kettel_state = []
# first index equal 0
save_kettel_state.append(0)

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

@ask.intent("TurnOnOutDoorLightIntent")
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

@ask.intent("TurnOffOutDoorLightIntent")
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

@ask.intent("TurnOnLivingRoomLightIntent")
# turns Living Room Light on
def livingroomlighton():
    if(save_livingroom_light_state[0] == 1):
        print("Living Room Light is already ON. Not action taken.")
        return statement("Living Room Light is already ON. Not action taken.")
    else:
        save_livingroom_light_state[0] = 1
        print("Turning Living Room Light ON")
        GPIO.output(13,GPIO.HIGH)
        return statement("Turning Living Room Light ON")

@ask.intent("TurnOffLivingRoomLightIntent")
# turns Living Room Light off
def livingroomlightoff():
    if(save_livingroom_light_state[0] == 0):
        print("Living Room Light is already OFF. Not action taken.")
        return statement("Living Room Light is already OFF. Not action taken.")
    else:
        save_livingroom_light_state[0] = 0
        print("Turning Living Room Light OFF")
        GPIO.output(13,GPIO.LOW)
        return statement("Turning LivingRoom Light off")

@ask.intent("TurnOnBedRoomLightIntent")
# turns Bed Room Light on
def bedroomlighton():
    if(save_bedroom_light_state[0] == 1):
        print("Bed Room Light is already ON. Not action taken.")
        return statement("Bed Room Light is already ON. Not action taken.")
    else:
        save_bedroom_light_state[0] = 1
        print("Turning Bed Room Light ON")
        GPIO.output(19,GPIO.HIGH)
        return statement("Turning Bed Room Light ON")

@ask.intent("TurnOffBedRoomLightIntent")
# turns Bed Room Light off
def bedroomlightoff():
    if(save_bedroom_light_state[0] == 0):
        print("Turning Bed Room Light OFF")
        return statement("Bed Room Light is already OFF. Not action taken.")
    else:
        save_bedroom_light_state[0] = 0
        print("Stopping BedRoom Light")
        GPIO.output(19,GPIO.LOW)
        return statement("Turning BedRoom Light off")

@ask.intent("TurnOnKitchenLightIntent")
# turns Kitchen Light on
def kitchenlighton():
    if(save_kitchen_light_state[0] == 1):
        print("Kitchen Light is already ON. Not action taken.")
        return statement("Kitchen Light is already ON. Not action taken.")
    else:
        save_kitchen_light_state[0] = 1
        print("Turning Kitchen Light ON")
        GPIO.output(26,GPIO.HIGH)
        return statement("Turning Kitchen Light ON")

@ask.intent("TurnOffKitchenLightIntent")
# turns Kitchen Light off
def kitchenlightoff():
    if(save_kitchen_light_state[0] == 0):
        print("Turning Kitchen Light OFF")
        return statement("Kitchen Light is already OFF. Not action taken.")
    else:
        save_kitchen_light_state[0] = 0
        print("Stopping Kitchen Light")
        GPIO.output(26,GPIO.LOW)
        return statement("Turning Kitchen Light off")

# @ask.intent("TurnOnAcIntent")
# # turns AC on
# def acon():
#     if(save_ac_state[0] == 1):
#         print("AC is already ON. Not action taken.")
#         return statement("AC is already ON. Not action taken.")
#     else:
#         save_ac_state[0] = 1
#         print("Turning AC ON")
#         GPIO.output(12,GPIO.HIGH)
#         return statement("Turning AC ON")

# @ask.intent("TurnOffAcIntent")
# # turns AC off
# def acoff():
#     if(save_ac_state[0] == 0):
#         print("Turning AC OFF")
#         return statement("AC is already OFF. Not action taken.")
#     else:
#         save_ac_state[0] = 0
#         print("Stopping AC")
#         GPIO.output(12,GPIO.LOW)
#         return statement("Turning AC off")


@ask.intent("TurnOnKettelIntent")
# turns Kettel on
def kettelon():
    if(save_kettel_state[0] == 1):
        print("Kettel is already ON. Not action taken.")
        return statement("Kettel is already ON. Not action taken.")
    else:
        save_kettel_state[0] = 1
        print("Turning Kettel ON")
        GPIO.output(16,GPIO.HIGH)
        return statement("Turning Kettel ON")

@ask.intent("TurnOffKettelIntent")
# turns Kettel off
def ketteloff():
    if(save_kettel_state[0] == 0):
        print("Kettel is already OFF. Not action taken.")
        return statement("Kettel is already OFF. Not action taken.")
    else:
        save_kettel_state[0] = 0
        print("Stopping Kettel")
        GPIO.output(16,GPIO.LOW)
        return statement("Turning Kettel off")

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