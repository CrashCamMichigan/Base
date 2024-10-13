import cv2
import base64
import time  # Import the time module
from pymongo import MongoClient
from datetime import datetime
import pytz  # Import pytz for time zone handling
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Atlas credentials
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
print(MONGO_PASSWORD)
username = "crash1"
password = MONGO_PASSWORD
dbname = "my_database"  # Change to your desired database name

# Create a connection string
connection_string = f"mongodb+srv://{username}:{password}@cluster1.ztedo.mongodb.net/{dbname}?retryWrites=true&w=majority&appName=Cluster1"

# Create a MongoClient to connect to MongoDB
client = MongoClient(connection_string)

# Access the database
db = client[dbname]

# Check the connection by listing the collections in the database
collections = db.list_collection_names()
print("Collections in the database:", collections)

# Access the collection where you want to insert documents
sample_collection = db['Data']  # Replace with your collection name

# Set the timezone to Eastern Time
eastern = pytz.timezone('US/Eastern')

import sys, threading, queue, serial
import serial.tools.list_ports

baudRate = 9600
arduinoQueue = queue.Queue()
localQueue = queue.Queue()

def selectArduino():
    ports = serial.tools.list_ports.comports()
    choices = []
    print('PORT\tDEVICE\t\t\tMANUFACTURER')
    for index,value in enumerate(sorted(ports)):
        if (value.hwid != 'n/a'):
            choices.append(index)
            print(index, '\t', value.name, '\t', value.manufacturer) # https://pyserial.readthedocs.io/en/latest/tools.html#serial.tools.list_ports.ListPortInfo

    choice = -1
    while choice not in choices:
        answer = input("➜ Select your port: ")
        if answer.isnumeric() and int(answer) <= int(max(choices)):
            choice = int(answer)
    print('selecting: ', ports[choice].device)
    return ports[choice].device


def listenToArduino():
    message = b''
    while True:
        incoming = arduino.read()
        if (incoming == b'\n'):
            arduinoQueue.put(message.decode('utf-8').strip().upper())
            message = b''
        else:
            if ((incoming != b'') and (incoming != b'\r')):
                 message += incoming

def listenToLocal():
    while True:
        command = sys.stdin.readline().strip().upper()
        localQueue.put(command)
'''
def configureUserInput():
    localThread = threading.Thread(target=listenToLocal, args=())
    localThread.daemon = True
    localThread.start()
'''

def configureArduino():
    global arduinoPort
    arduinoPort = selectArduino()
    global arduino
    arduino = serial.Serial(arduinoPort, baudrate=baudRate, timeout=.1)
    arduinoThread = threading.Thread(target=listenToArduino, args=())
    arduinoThread.daemon = True
    arduinoThread.start()

# ---- CALLBACKS UPON MESSAGES -----

def handleLocalMessage(aMessage):
    print("=> [" + aMessage + "]")
    arduino.write(aMessage.encode('utf-8'))
    arduino.write(bytes('\n', encoding='utf-8'))

def handleArduinoMessage(aMessage):
    now = datetime.now(eastern)
    now = now.replace(microsecond=0)  # Round to seconds

    # Prepare the document for MongoDB
    sample_document = {
        "image": int(aMessage),  # Store the encoded image
        "Time": now  # Use the current time in Eastern Time
    }

    # Insert the document into MongoDB
    insert_result = sample_collection.insert_one(sample_document)
    print(insert_result)
    print("<= [" + aMessage + "]")

# ---- MAIN CODE -----

configureArduino()                                      # will reboot AVR based Arduinos
#configureUserInput()                                    # handle stdin 

print("Waiting for Arduino")

# --- A good practice would be to wait for a know message from the Arduino
# for example at the end of the setup() the Arduino could send "OK"
while True:
    if not arduinoQueue.empty():
        if arduinoQueue.get() == "OK":
            break
print("Arduino Ready")

# --- Now you handle the commands received either from Arduino or stdin
while True:
    if not arduinoQueue.empty():
        handleArduinoMessage(arduinoQueue.get())

    if not localQueue.empty():
        handleLocalMessage(localQueue.get())
