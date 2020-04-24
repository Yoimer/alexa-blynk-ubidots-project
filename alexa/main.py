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

######################################
# Skill name: blynk app
# Invocation Name : blynk app

##########launch skill##########
# voice commands are:
#Alexa, start blynk app
#Alexa, open blynk app
#Alexa, begin blynk app
#Alexa, blynk app
#Alexa, load blynk app
#Alexa, run blynk app
#Alexa, use blynk app
#Alexa, tell blynk app (This one makes no sense for the context of this skill. It works
                            # if invoking though)

##########launch skill##########
@ask.launch
# read welcome message from template.yaml file
def launch_app():
    welcome_msg = render_template('welcome')
    prompt = 'Which option do you prefer man?'
    return question(welcome_msg).reprompt(prompt).simple_card('Welcome to blynk app', welcome_msg)

@ask.intent("TemperatureIntent")
# get humidity from sensor
def temperature():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
        print("Temperature = {} °C".format(temperature))
        return statement("Temperature value is {} Celsius degrees".format(temperature))
    else:
        print("Sensor failure. Check wiring.")
        return statement("Sensor failure. Please check wiring.")

# does not match any country in LIST_OF_COUNTRIES
@ask.intent("AMAZON.FallbackIntent")
def fallback():
    fallback_msg = 'I can not help you with that, try any of the options available for this app'
    return statement(fallback_msg)

# ask for help when welcoming or anytime
@ask.intent("AMAZON.HelpIntent")
def help():
    help_msg = "Ok, I am going to help you... Please, tell me which country or currency would you like me to calculate the exchange?"
    reprompt_msg  = 'Please, tell me which country or currency would you like me to calculate the exchange?'
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