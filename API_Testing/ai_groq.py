import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_k = os.getenv('GROQ_API_KEY')

client = Groq(
    api_key = api_k
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': 'Give me a random color.'
        }
    ],
    model = "llama-3.3-70b-versatile"
)

print(chat_completion.choices[0].message.content)

""" Example output: (Prompt is: Give me a random color.)

python ai_groq.py 

Turquoise.

"""