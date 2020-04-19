import Adafruit_DHT
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    # prompts user for input
    user_input = input("Please enter TEMP or HUMD: ")

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
    else:
        print("Unrecognized input, enter TEMP or HUMD: ")