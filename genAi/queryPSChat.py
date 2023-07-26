import requests
from dotenv import load_dotenv
import os
import sys

load_dotenv()
pschat_token = os.environ.get('PSCHAT_TOKEN')


def getGPTData(input):
    topic = "my_topic"
    modelType = "gpt35turbo"

    # pass in token to headers for authentication 
    headers = {
        "Authorization": f"Bearer " + pschat_token,
        "Content-Type": "application/json",
    }
    data = {
        # promt to send to the chat box
        "message": """
                  tell me a joke!
                  """,
        # model of PS chat we want to use
        "options": {
            "model": modelType
        }
    }

    # try-except block sends POST request to the chatbot API using requests, with the prompt and headers
    # as param. Then the response is parsed as JSON
    try:
        url = "https://api.psnext.info/api/chat"

        # request response from chatbot
        response = requests.post(url, json=data, headers=headers)

        response_data = response.json()
        return response_data["data"]["messages"][2]["content"]
    
    # catch error if there's any
    except Exception as error:
        print("FAILED PROMPT")
        print(error)