import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId  # Import ObjectId for MongoDB ID handling

# Load MongoDB credentials from .env
load_dotenv()

MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
username = "crash1"
dbname = "my_database"  # Your database name
collection_name = "VideoData"  # Your collection name

# Create a connection string
connection_string = f"mongodb+srv://{username}:{MONGO_PASSWORD}@cluster1.ztedo.mongodb.net/{dbname}?retryWrites=true&w=majority"

def get_latest_video_base64():
    # Connect to MongoDB
    client = MongoClient(connection_string)
    db = client[dbname]
    collection = db[collection_name]

    try:
        # Retrieve the latest video document (sort by _id)
        latest_video_document = collection.find_one(sort=[("_id", -1)])  # Get the most recent entry

        # Check if the document exists
        if latest_video_document:
            # Extract the Base64-encoded video data and the ObjectId
            video_data = latest_video_document.get("video_data")
            video_id = latest_video_document.get("_id")  # Retrieve ObjectId
            print(f"Retrieved video ID: {video_id}")
            return video_data  # Return the Base64-encoded video data
        else:
            print("No video found in the database.")
            return None
    except Exception as e:
        print(f"Error retrieving video data: {e}")
        return None
    finally:
        # Close the MongoDB connection
        client.close()

# # Example usage:
# if __name__ == "__main__":
#     video_base64 = get_latest_video_base64()
#     if video_base64:
#         print("Retrieved Base64 video data:", video_base64)
