from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

api_key=os.getenv("GEMINI_API")
client = genai.Client(api_key = api_key )



from flask import Flask, render_template, url_for, request

app = Flask(__name__)



#list of raw materials
raw_food_items = {
    "fruits": [
        "apple", "banana", "mango", "grapes", "orange", "papaya", "pineapple", "guava",
        "watermelon", "muskmelon", "pomegranate", "strawberry", "blueberry", "blackberry",
        "pear", "peach", "plum", "cherry", "kiwi", "dragon fruit", "lychee"
    ],
    "vegetables": [
        "cabbage", "carrot", "broccoli", "spinach", "potato", "tomato", "cauliflower",
        "cucumber", "capsicum", "brinjal", "bitter gourd", "ridge gourd", "bottle gourd",
        "ladyfinger", "zucchini", "pumpkin", "radish", "turnip", "green beans", "peas"
    ],
    "leafy_greens": [
        "spinach", "lettuce", "kale", "fenugreek leaves", "coriander leaves", "mustard greens",
        "amaranth", "curry leaves", "mint", "basil"
    ],
    "grains": [
        "rice", "wheat", "oats", "quinoa", "barley", "millet", "sorghum", "corn", "buckwheat"
    ],
    "legumes_and_pulses": [
        "lentils", "chickpeas", "kidney beans", "black beans", "green gram", "split peas",
        "soybeans", "pigeon peas", "mung beans"
    ],
    "nuts_and_seeds": [
        "almonds", "cashews", "walnuts", "peanuts", "pistachios", "hazelnuts", "flaxseeds",
        "chia seeds", "pumpkin seeds", "sunflower seeds", "sesame seeds"
    ],
    "roots_and_tubers": [
        "ginger", "garlic", "beetroot", "sweet potato", "yam", "turmeric root", "taro root",
        "radish", "onion"
    ],
    "herbs": [
        "mint", "basil", "coriander", "parsley", "thyme", "oregano", "rosemary", "dill",
        "chives", "sage"
    ],
    "spices": [
        "turmeric", "cumin", "black pepper", "cardamom", "clove", "cinnamon", "nutmeg",
        "mustard seeds", "fenugreek seeds", "coriander seeds", "bay leaf", "star anise"
    ],
    "mushrooms": [
        "button mushroom", "shiitake", "oyster mushroom", "portobello", "enoki"
    ],
    "other": [
        "coconut", "tamarind", "raw jackfruit", "lemon", "lime", "green chili"
    ]
}






@app.route("/", methods=['GET', 'POST'])
def hello_world():

    chosen = request.form.getlist("ingredients")
    given_prompt = request.form.get("user_prompt") 



    #gemini
    
    behave = f"""
    You are mainly designed to say food recipies from a few given ingridients. 

    The ingridients are {chosen}. Now provide a good food recipie on this ingridients, with this request {given_prompt}
    """

    reply = ""
    for chunks in client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=behave
    ):
        reply += chunks.text or ""


    return render_template('template.html', data = raw_food_items, reply = reply)





app.run(debug=True)

