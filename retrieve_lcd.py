import network
import urequests
import time

from machine import Pin, I2C
import sys
from pico_i2c_lcd import I2cLcd

from time import sleep

# LED pins
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)
led3 = Pin(3, Pin.OUT)

# Connect to Wi-Fi
ssid = 'Wifi'
password = '123456789'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print('Connection successful')
print(wlan.ifconfig())

# Your Google Apps Script URL
url = 'https://script.google.com/macros/s/AKfycbzePDY5boHRAGWtkMe3Gm1yeOMsU6iRxL9wvGdJ9Fni_aGCfmrzqW_BSw22l2ZUTs-P/exec'

# Function to retrieve data
def retrieve_data():
    response = urequests.get(url)
    data = response.json()
    response.close()
    return data

# Initialize I2C for LCD
def initialize_lcd():
    try:
        i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
        devices = i2c.scan()
        print("I2C devices found:", devices)

        if not devices:
            raise Exception("No I2C devices found")

        I2C_ADDR = devices[0]
        lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # Assuming 2 rows and 16 columns
        return lcd
    except Exception as e:
        print("Error initializing I2C or LCD:", e)
        return None

# Function to display message on LCD
def display_message(lcd, message):
    lcd.clear()
    lcd.putstr(message)

# Function to control LEDs based on density_count
def control_leds(density_count):
    led3.value(1)
    sleep(2)

    if density_count >= 0:
        if density_count >= 1 and density_count < 3:
            led3.value(0)
            led1.value(1)
            sleep(3)
            led1.value(0)
            led2.value(1)
            sleep(1)
            led2.value(0)
        elif density_count >= 3:
            led3.value(0)
            led1.value(1)
            sleep(10)
            led1.value(0)
            led2.value(1)
            sleep(2)
            led2.value(0)
        else:
            led1.value(0)
            led2.value(0)
            led3.value(0)
    else:
        led1.value(0)
        led2.value(0)
        led3.value(0)

# Initialize LCD
lcd = initialize_lcd()

# Main loop to continuously update data
try:
    while True:
        # Retrieve data
        retrieved_data = retrieve_data()
        print("Retrieved data:", retrieved_data)

        density_count = None

        if isinstance(retrieved_data, list) and len(retrieved_data) > 0:
            latest_entry = retrieved_data[-1]
            density_count = latest_entry.get('Density')
            if density_count is not None:
                print("Latest Density count:", density_count)
                # Display on LCD
                if lcd:
                    display_message(lcd, f"Density: {density_count}")
                    sleep(5)  # Display the message for 5 seconds
                # Control LEDs
                control_leds(density_count)
            else:
                print("Error: 'Density' key not found in the retrieved data.")
        else:
            print("Error: Invalid data format retrieved or list is empty.")
        
        sleep(5)  # Wait before fetching data again

except KeyboardInterrupt:
    print("Stopped by user")
    led1.value(0)
    led2.value(0)
    led3.value(0)
    lcd.clear()
# Clean up and disconnect
wlan.disconnect()
wlan.active(False)

