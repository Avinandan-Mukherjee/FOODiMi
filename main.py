import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_API")
genai.configure(api_key=api_key)

from flask import Flask, render_template, url_for, request
from markupsafe import Markup
import markdown2

app = Flask(__name__)

# List of raw materials
raw_food_items = {
    "Fruits": [
        "Apple", "Banana", "Mango", "Grapes", "Orange", "Papaya", "Pineapple", "Guava",
        "Watermelon", "Muskmelon", "Pomegranate", "Strawberry", "Blueberry", "Blackberry",
        "Pear", "Peach", "Plum", "Cherry", "Kiwi", "Dragon Fruit", "Lychee"
    ],
    "Vegetables": [
        "Cabbage", "Carrot", "Broccoli", "Spinach", "Potato", "Tomato", "Cauliflower",
        "Cucumber", "Capsicum", "Brinjal", "Bitter Gourd", "Ridge Gourd", "Bottle Gourd",
        "Ladyfinger", "Zucchini", "Pumpkin", "Radish", "Turnip", "Green Beans", "Peas"
    ],
    "Leafy Greens": [
        "Spinach", "Lettuce", "Kale", "Fenugreek Leaves", "Coriander Leaves", "Mustard Greens",
        "Amaranth", "Curry Leaves", "Mint", "Basil"
    ],
    "Grains": [
        "Rice", "Wheat", "Oats", "Quinoa", "Barley", "Millet", "Sorghum", "Corn", "Buckwheat"
    ],
    "Legumes And Pulses": [
        "Lentils", "Chickpeas", "Kidney Beans", "Black Beans", "Green Gram", "Split Peas",
        "Soybeans", "Pigeon Peas", "Mung Beans"
    ],
    "Nuts And Seeds": [
        "Almonds", "Cashews", "Walnuts", "Peanuts", "Pistachios", "Hazelnuts", "Flaxseeds",
        "Chia Seeds", "Pumpkin Seeds", "Sunflower Seeds", "Sesame Seeds"
    ],
    "Roots And Tubers": [
        "Ginger", "Garlic", "Beetroot", "Sweet Potato", "Yam", "Turmeric Root", "Taro Root",
        "Radish", "Onion"
    ],
    "Herbs": [
        "Mint", "Basil", "Coriander", "Parsley", "Thyme", "Oregano", "Rosemary", "Dill",
        "Chives", "Sage"
    ],
    "Spices": [
        "Turmeric", "Cumin", "Black Pepper", "Cardamom", "Clove", "Cinnamon", "Nutmeg",
        "Mustard Seeds", "Fenugreek Seeds", "Coriander Seeds", "Bay Leaf", "Star Anise"
    ],
    "Fish": [
        "Rohu", "Katla", "Hilsa", "Pomfret", "Salmon", "Mackerel", "Tuna", "Prawns",
        "Bhetki", "Sardine", "Anchovy"
    ],
    "Meat": [
        "Chicken", "Goat", "Mutton", "Beef", "Pork", "Duck", "Turkey", "Quail", "Rabbit"
    ],
    "Animal Products": [
        "Egg", "Milk", "Cheese", "Butter", "Paneer", "Curd", "Cream"
    ],
    "Mushrooms": [
        "Button Mushroom", "Shiitake", "Oyster Mushroom", "Portobello", "Enoki"
    ],
    "Other": [
        "Coconut", "Tamarind", "Raw Jackfruit", "Lemon", "Lime", "Green Chili"
    ]
}


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    chosen = request.form.getlist("ingredients")
    given_prompt = request.form.get("user_prompt") 

    # Gemini
    behave = f"""
    You are mainly designed to say food recipes from a few given ingredients. 

    The ingredients are {chosen}. Now provide a good food recipe using these ingredients, with this request: {given_prompt}
    """

    reply = ""
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(behave)
        reply = response.text
    except Exception as e:
        reply = f"Error generating recipe: {str(e)}"

    html_reply = Markup(markdown2.markdown(reply))

    return render_template('template.html', data=raw_food_items, reply=html_reply)

if __name__ == "__main__":
    app.run(debug=True)