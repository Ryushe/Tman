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
                formattedRecipes += "\n\n\n"

    return formattedRecipes

def addRecepies(category, recipe, link):
    if category not in recipes:
        recipes[category] = {}
    
    if recipe not in recipes[category]:
        recipes[category][recipe] = link

        writeToFile()
    else:
        print("Recipe already exists.")

async def checkIfRecipeExists(ctx, recipe):
        for category in list(recipes.keys()):
            recipeItems = recipes[category]
            if recipe in recipeItems:
                return category
        if recipe not in recipeItems:
            await ctx.channel.send("Recipe doesn't exist")

async def delRecipies(ctx, recipe):
    
    category = ''
         
    category = await checkIfRecipeExists(ctx, recipe)
    if category:
        del recipes[category][recipe]
        with open(recipe_path, "w") as recipe_file:
            json.dump(recipes, recipe_file, indent=4)
        
        await ctx.channel.send("Recipe deleted")


async def checkIfInRecipeList(recipe):
    for category in list(recipes.keys()):
        recipeItems = recipes[category]
        if recipe in recipeItems:
            return True, category, recipe
        else: return False, category, recipe

def writeToFile():
    with open(recipe_path, "w") as recipe_file:
        try:
            json.dump(recipes, recipe_file, indent=4)
        except Exception as e:
            print(f"Error writing JSON data: {e}")
    
    recipe_file.close()


async def main(ctx, choice, *args, bot):
    choices = """

empty(anything thats not an option) - help

ar - add recepies <category>, <recipe>, <link> (comma seperated or whitespace seperated) CammelCase <ex: ChickenNuggets>
er - edit recepies (enters edit mode / follow prompts)
lr - list recepies <recipe name>

ac - add categories
rc - remove categories
ec - edit categories
lc - list categories
    """

    # add recipe
    if choice == "ar": # done
        
        if ',' in args:
            values = ''.join(args).split(',')
        else:
            values = ','.join(args).split(',')
        
        deEncodedValue = f"<{values[2]}>"
        try:
            addRecepies(values[0].lower(), values[1], deEncodedValue) # should be (category, recipe, link)
            await ctx.channel.send("Recipe added")
        except(IndexError)as e:
            await ctx.channel.send(f"Give me 3 args dumbass <category> <Recipename> <link>\nTo see categories use:\n`!cook lr`")

    # remove recipe
    elif choice == "rr": # done
        recipe = args
        await delRecipies(ctx, recipe[0])

    # edit recipe
    elif choice == "er":
        await ctx.channel.send(f"Select a category\n{listAllRecepies()}")

        while True:
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            userInput = await bot.wait_for('message', check=check)

            recipeInList, category, recipe = await checkIfInRecipeList(userInput.content.lower())

            if recipeInList:
                await ctx.channel.send("What would you like to change (L)ink or (N)ame (E)xit")
                response = await bot.wait_for('message', check=check)
                if response.content.lower() == 'n':
                    await ctx.channel.send("Enter new name:")
                    newRecipeName = await bot.wait_for('message', check=check)
                    linkValue = recipes[category][recipe]
                    del recipes[category][recipe]
                    recipes[category][newRecipeName.content] = linkValue
                    await ctx.channel.send(f"{recipe}: name changed to {newRecipeName.content}")
                    
                elif response.content.lower() == 'l':
                    await ctx.channel.send("Enter new link:")
                    newLink = await bot.wait_for('message', check=check)
                    # Update the link for the existing recipe name (key)
                    recipes[category][recipe] = newLink.content
                    await ctx.channel.send(f"{recipes[category][newLink.content]}: Link changed")
                else:
                    await ctx.channel.send(f"Exited edit config (nothing changed)")
                    break

                writeToFile()
            break
            

        
    elif choice == "lr": # done
        category = ''.join(args)

        if args:
            recipe = listRecepies(category.lower())
        else: 
            recipe = listAllRecepies()

        await ctx.channel.send(f"Recepies are: \n{recipe}")

    elif choice == "ac":
        category = args[0]
        try:
            if category not in recipes:
                recipes[category] = {}
                await ctx.channel.send(f"Added:{category}")
            writeToFile()
        except(IndexError) as e:
            await ctx.channel.send("remove the whitespaces")


    elif choice == "rc":
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        while True:
            category = args[0]
            try:
                if category in recipes:
                    await ctx.channel.send(f"Are you sure? This will delete the catagory and everything inside\n(Y)es, (N)o")
                    newLink = await bot.wait_for('message', check=check)
                    if newLink.content.lower() == 'y':
                        del recipes[category]
                        await ctx.channel.send(f"Deleted {category}")
                        writeToFile()
                        break
                    else: 
                        await ctx.channel.send(f"Didn't delete :)")
                        break
                else:
                    await ctx.channel.send(f"{args[0]} is not a category")
                    break
            except() as e:
                await ctx.channel.send(f"Category not removed")
                break

    elif choice == "ec":
        await ctx.channel.send(f"Nigga this shit aint done yet")
    elif choice == "lc":
        categories = listCategories()
        await ctx.channel.send(f"Categories:\n{categories}")

    else:
        await ctx.channel.send(f"your choices are: {choices}")



recipe_file.close()




