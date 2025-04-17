# Functional; analyzes an image to classify its contents
# Useful for identifying food
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://cdn7.localdatacdn.com/dc/washington/6111766/original/Kcfkhyhihn.jpg"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)

""" Example output:
ChatCompletionMessage(content='
The image depicts two donuts on a plate, 
with one prominently displayed in the 
foreground and the other partially 
visible behind it. The donut in the foreground 
features a chocolate glaze and is adorned with 
multicolored sprinkles, while the second donut 
appears to have a similar chocolate glaze but without 
sprinkles. The background of the image consists of a 
plain white plate.', role='assistant', 
executed_tools=None, function_call=None, 
reasoning=None, tool_calls=None)

"""