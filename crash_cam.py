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

# Start the video capture (0 for the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Open a file to write the encoded frame data
with open("webcam_data.txt", "w") as file:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Write the encoded frame to the text file
        file.write(jpg_as_text + "\n")

        # Get the current time in Eastern Time and round to the nearest second
        now = datetime.now(eastern)
        now = now.replace(microsecond=0)  # Round to seconds

        # Prepare the document for MongoDB
        sample_document = {
            "image": jpg_as_text,  # Store the encoded image
            "Time": now  # Use the current time in Eastern Time
        }

        # Insert the document into MongoDB
        insert_result = sample_collection.insert_one(sample_document)
        print("Inserted document ID:", insert_result.inserted_id)

        # Display the resulting frame
        cv2.imshow('Webcam Stream', frame)

        # Wait for 1 second
        time.sleep(1)  # Delay for 1 second

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()
