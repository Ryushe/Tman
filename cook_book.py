import json

try:
    with open(recepies.json, "r") as file:
        recipes = json.load(file)
except FileNotFoundError:
    recipes = {}

recepies = {
    "Beef": {
        "Beef and Rice"
    }
}

    


