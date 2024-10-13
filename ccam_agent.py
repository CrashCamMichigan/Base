from uagents import Agent, Context, Model
from pydantic import BaseModel
import requests
import json
import os
from datetime import datetime, timedelta
from ccam_helpers import create_video_from_base64
import base64

import pymongo
MONGO_USER = os.environ.get("MONGO_USER", "YOUR_MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASS", "YOUR_MONGO_PASSWORD")
url = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster1.ztedo.mongodb.net/?retryWrites=true&w=majority"
mongo_client = pymongo.MongoClient(url)
collection = mongo_client.get_database('my_database')['Data']

from openai import OpenAI
openai_client = OpenAI()

class ModelOutputFormat(BaseModel):
    is_crash: bool

def get_mongo_data(last_n_seconds: int = 20):
    # specific_time = datetime.now() 
    specific_time = datetime.strptime("2024-10-13T06:18:18.772+00:00", "%Y-%m-%dT%H:%M:%S.%f%z")
    start_time = specific_time - timedelta(seconds=15)

    query = {
        'Time': {
            '$gte': start_time,
            '$lte': specific_time
        }
    }

    results = collection.find(query)
    vibrations = []
    images = []
    for i, document in enumerate(results):
        if 'vibration' in document.keys():
            vibrations.append(document['vibration'])
        if 'image' in document.keys():
            images.append(document['image'])
    return vibrations, images


def get_completion(context, vibrations=[9,10,11,11,9,9,9], images=[], max_tokens=256):
    system_description = """Respond to incoming data about a car crash. Respond with True or False witha varible is_crash. Input contains vibration data and an image. Rely
    on the vibration data to determine if a crash has occurred. There should be a massive spike in the vibration data if a crash has occurred. Also, the data should rocket up to value of at least a few 100. Also use the image as supporting evidence.
    Image could include a toy car or a real car. Treat seeing nothig as a crash.
    """
    images_params = [{
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image}"
        }
    } for image in images]

    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_description},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "Vibrations: " + str(vibrations),
                }
            ] + images_params
            },
        ],
        response_format=ModelOutputFormat,
        max_tokens=max_tokens,
        temperature=0.0,
    )

    model_output = json.loads(completion.choices[0].message.content)
    is_crash = model_output["is_crash"]
    return is_crash

agent = Agent()

@agent.on_interval(period=5.0)
async def handle_request(ctx: Context):
    vibrations, images = get_mongo_data()
    is_crash = get_completion(ctx, vibrations, images)
    print(len(images))
    print(is_crash)
    if is_crash:
        video = create_video_from_base64(images)
        temp_collec = mongo_client.get_database('my_database')['VideoData']
        with open(video, "rb") as video_file:
            video_binary = video_file.read()
            video_base64 = base64.b64encode(video_binary).decode('utf-8')
        # temp_collec.insert_one({'video': video_base64})
        temp_collec.replace_one({}, {'video_data': video_base64}, upsert=True)
        exit()

if __name__ == "__main__":
    agent.run()
    