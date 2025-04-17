# Functional; uses AI to communicate messages
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
            'content': 'What ingredients might be in butter chicken?'
        }
    ],
    model = "llama-3.3-70b-versatile"
)

print(chat_completion.choices[0].message.content)

""" Example output: (Prompt is: Give me a random color.)

python ai_groq.py 

Turquoise.

"""

"""
Prompt: What ingredients might be in butter chicken?s
Butter chicken, also known as murgh makhani, is a popular Indian dish that often contains a combination of the following ingredients:

1. Chicken: Boneless, skinless chicken breast or thighs, typically marinated in spices and yogurt.
2. Tomato puree or crushed tomatoes: Fresh or canned, these add a rich, tangy flavor to the dish.
3. Onion: Sautéed or caramelized onions add a sweet, depth of flavor.
4. Garlic and ginger: Minced or grated, these aromatics add warmth and depth to the dish.
5. Spices: A blend of spices such as garam masala, cumin, coriander, cayenne pepper, and turmeric.
6. Butter or ghee: Unsalted butter or ghee (clarified butter) is used to add richness and creaminess to the sauce.
7. Heavy cream or yogurt: These dairy products help to balance the heat and acidity of the tomatoes, creating a smooth, creamy sauce.
8. Fenugreek leaves (kasoori methi): Dried or fresh, these leaves add a distinct, slightly bitter flavor.
9. Lemon juice or vinegar: A squeeze of fresh lemon juice or a splash of vinegar helps to balance the flavors.
10. Salt and sugar: To balance the flavors and add depth to the dish.
11. Optional ingredients: Some recipes may include additional ingredients such as cilantro, cardamom, cinnamon, or green chilies to add extra flavor and aroma.

These ingredients come together to create a rich, creamy, and aromatic sauce that coats the marinated chicken, making butter chicken a beloved dish around the world.
"""