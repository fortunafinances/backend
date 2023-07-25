import asyncio
import requests

async def getGPTData(topic, modelType):
    # pass in token to headers for authentication 
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySW5mbyI6eyJpZCI6MjE0MDksInJvbGVzIjpbImRlZmF1bHQiXSwicGF0aWQiOiI0NjBkMzRkZS0xNjlkLTRlZTItYWE4Ni0yMzcxMWIxNTY5NDIifSwiaWF0IjoxNjkwMzA3MzgwLCJleHAiOjE2OTI4OTkzODB9.fa7Mf3g6MoeOO6SfYQ79b8ORB9vAlwv9lUVjj-ZCZ4M",
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

# Usage example:
async def main():
    topic = "my_topic"
    modelType = "gpt35turbo"
    result = await getGPTData(topic, modelType)
    print(result)


# Run the event loop
asyncio.run(main())