import json
import random
import time


recipe_path = "recepies.json"

try:
    with open(recipe_path, "r") as recipe_file:
        recipes = json.load(recipe_file)
except FileNotFoundError:
    with open(recipe_path, "w") as recipe_file:
        recipes = {}

# for main function if user doesn't input a choice
def getRandomCategory():                                                # doesnt work
    return random.choice(list(recipes.keys()))

def listCategories():
    word = ", ".join([recipe.capitalize() for recipe in recipes.keys()])
    return word

def listRecepies(category): # lists only that category
    formattedRecipes = ""
    
    if category in recipes:
        recipesInCategory = recipes[category]
        formattedRecipes += f"{category.capitalize()}:\n"
        numRecipes = len(recipesInCategory)
        
        for i, (recipeName, recipeLink) in enumerate(recipesInCategory.items()):
            formattedRecipes += f"    {recipeName}: {recipeLink}"
            if i < numRecipes - 1:
                formattedRecipes += "\n" 
            if i == numRecipes - 1:
                formattedRecipes += "\n\n"
    return formattedRecipes
    

def listAllRecepies():
    formattedRecipes = ""
    for category, recipesInCategory in recipes.items():
        formattedRecipes += f"{category.capitalize()}:\n"
        numRecipes = len(recipesInCategory)
        for i, (recipeName, recipeLink) in enumerate(recipesInCategory.items()):
            formattedRecipes += f"  {recipeName}: {recipeLink}"
            if i < numRecipes - 1:
                formattedRecipes += "\n" 
            if i == numRecipes - 1:
                formattedRecipes += "\n\n\n\n"

    return formattedRecipes

def addRecepies(category, recipe, link):
    if category not in recipes:
        recipes[category] = {}
    
    if recipe not in recipes[category]:
        recipes[category][recipe] = link

        with open(recipe_path, "w") as recipe_file:
            json.dump(recipes, recipe_file, indent=4)
    else:
        print("Recipe already exists.")

# def delRecipies(category, recipe):
#     if category in recipes:
#         if recipe in recipes[category]:
#             del recipes[category][recipe]
            


async def delRecipies(ctx, bot, recipe):
    

    category = ''
    async def checkIfRecipeExists():
        for category in list(recipes.keys()):
            recipeItems = recipes[category]
            print(recipeItems)
            if recipe in recipeItems:
                return category
            
    category = await checkIfRecipeExists()
    if category:
        del recipes[category][recipe]
        with open(recipe_path, "w") as recipe_file:
            json.dump(recipes, recipe_file, indent=4)
        
        await ctx.channel.send("Recipe deleted")

recipe_file.close()