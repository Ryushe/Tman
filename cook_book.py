import json
import random
import time


recipe_path = "recepies.json"

try:
    with open(recipe_path, "r") as recipe_file:
        recipes = json.load(recipe_file)
except FileNotFoundError:
    recipes = {}

# for main function if user doesn't input a choice
def getRandomCategory():                                                # doesnt work
    return random.choice(list(recipes.keys()))

def listCategories():
    word = ", ".join(recipes.keys())
    return word

def listRecepies(category):
    recipe = ", ".join(recipes[category])
    return recipe

def listAllRecepies():
    formatted_recipes = ""
    for category, recipes_in_category in recipes.items():
        formatted_recipes += f"{category.capitalize()}:\n"
        num_recipes = len(recipes_in_category)
        for i, (recipe_name, recipe_link) in enumerate(recipes_in_category.items()):
            formatted_recipes += f"  {recipe_name}: {recipe_link}"
            if i < num_recipes - 1:
                formatted_recipes += "\n" 
            if i == num_recipes - 1:
                formatted_recipes += "\n\n"

    return formatted_recipes

def addRecepies(category, recipe, link):
    if category not in recipes:
        recipes[category] = {}
    
    if recipe not in recipes[category]:
        recipes[category][recipe] = link

        with open(recipe_path, "w") as recipe_file:
            json.dump(recipes, recipe_file, indent=4)
    else:
        print("Recipe already exists.")


recipe_file.close()