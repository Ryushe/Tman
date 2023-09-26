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

def checkIfSameUser(message, author, channel):
             return message and message.author == author and message.channel == channel

async def addRecipe(ctx, *args):
    if ',' in args:
        values = ''.join(args).split(',')
    else:
        values = ','.join(args).split(',')

    category = values[0].lower()
    recipe = values[1]
    deEncodedValue = f"<{values[2]}>"
    try:
        if category not in recipes:
            recipes[category] = {}
        if recipe not in recipes[category]:
            recipes[category][recipe] = deEncodedValue
            writeToFile()
            await ctx.channel.send("Recipe added")
        else:
            await ctx.channel.send("Recipe already exists.")
        
    except(IndexError)as e:
        await ctx.channel.send(f"Give me 3 args dumbass <category> <Recipename> <link>\nTo see categories use:\n`!cook lr`")


async def main(ctx, choice, *args, bot):
    choices = """

empty(anything thats not an option) - help

ar - add recepies <category>, <recipe>, <link> (comma seperated or whitespace seperated) CammelCase <ex: ChickenNuggets>
er - edit recepies (enters edit mode / follow prompts)
lr - list recepies <recipe name>

ac - add categories <category>
rc - remove categories <category to add> (will prompt after this is sent)
ec - edit categories <category> (will prompt after this is sent)
lc - list categories
    """

    # add recipe
    if choice == "ar": # done
        await addRecipe(ctx, *args)
       
    # remove recipe
    elif choice == "rr": # done
        recipe = args
        await delRecipies(ctx, recipe[0])

    # edit recipe
    elif choice == "er":
        await ctx.channel.send(f"Select a category\n{listAllRecepies()}")

        while True:

            userInput = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))

            recipeInList, category, recipe = await checkIfInRecipeList(userInput.content.lower())

            if recipeInList:
                await ctx.channel.send("What would you like to change (L)ink or (N)ame (E)xit")
                response = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))
                if response.content.lower() == 'n':
                    await ctx.channel.send("Enter new name:")
                    newRecipeName = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))
                    linkValue = recipes[category][recipe]
                    del recipes[category][recipe]
                    recipes[category][newRecipeName.content] = linkValue
                    await ctx.channel.send(f"{recipe}: name changed to {newRecipeName.content}")
                    
                elif response.content.lower() == 'l':
                    await ctx.channel.send("Enter new link:")
                    newLink = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))
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
                await ctx.channel.send(f"Added: {category}")
            writeToFile()
        except(IndexError) as e:
            await ctx.channel.send("remove the whitespaces")


    elif choice == "rc":
 
        while True:
            category = args[0]

            try:
                if category in recipes:
                    await ctx.channel.send(f"Are you sure? This will delete the catagory and everything inside\n(Y)es, (N)o")
                    newLink = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))
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
       
        category = args[0]
        while True:
            try:
                if category in recipes:
                    await ctx.channel.send(f"Entering edit mode:\nEnter anything other than an existing category to exit\nNew category name for{category}:")
                    newCategoryName = await bot.wait_for('message', check=lambda message: checkIfSameUser(message, ctx.author, ctx.channel))
                    if newCategoryName:
                        recipes[newCategoryName] = recipes[category] # copies to new
                        del recipes[category] # deletes old
                    writeToFile()
                    break
                else:
                    await ctx.channel.send("Exited edit mode")
                    await ctx.channel.send(f"That category doesn't exist viable options:\n{listCategories()}")   
                    break


            except() as e:
                break
    elif choice == "lc":
        categories = listCategories()
        await ctx.channel.send(f"Categories:\n{categories}")

    else:
        await ctx.channel.send(f"your choices are: {choices}")



recipe_file.close()




