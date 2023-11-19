from bs4 import BeautifulSoup
import requests
import json
import asyncio
import cook_book

aOptions = f"""\n
What category would you like to add it to?
{cook_book.listCategories()}
Enter new category to create it
"""

file = "recipe_grabber.json"

try:
    with open(file, "r") as url_file:
        url = json.load(url_file)
except FileNotFoundError:
    with open(file, "w") as url_file:
        url = {}

headers = {
    "User-Agent": "recipe_grabber/2.7 (Contact: itslilpeenieweenie@gmail.com)"
}


def writeToRecipes():
    file = "recepies.json"
    try:
        with open(file, "w") as recipeFile:
            recipes = json.load(recipeFile)
    except () as e:
        print("error writing")
    
    recipeFile.close()


def getResponse(searchUrl):
    response = requests.get(searchUrl, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Request failed with status code: {response.status_code}")


def removeWhitespaces(recipe):
    return recipe.replace(" ", "_")


def sanitizeRecipeName(recipeName):
    sanitizedRecipeName = recipeName
    
    for char in recipeName:
        if char.isspace():
            sanitizedRecipeName = removeWhitespaces(recipeName).lower()
    return sanitizedRecipeName
        

async def addRecipe(recipeName, recipeLink, ctx, bot):
    for char in recipeName:
        if char.isspace():
            sanitizedRecipeName = removeWhitespaces(recipeName).lower()
            break
        else: sanitizedRecipeName = recipeName

    await ctx.channel.send(aOptions) # var at top page
    category = await bot.wait_for('message', check=lambda message: cook_book.checkIfSameUser(message, ctx.author, ctx.channel))

    try: await cook_book.addRecipe(ctx, category.content.lower(), sanitizedRecipeName, recipeLink)
    except: await ctx.channel.send(f"Recipe couldn't be added")


def combineArgs(*args):
    return ' '.join(args)


async def main(ctx, *args, bot):
    site = "sites"
    userChoice = url["userchoice"]

    args = combineArgs(*args)

    if args.lower() == 's':
        await ctx.channel.send(f"Searching on {userChoice}")
    else:
        if args:
            searchUrl = url[site][userChoice] + args
        else:
            searchUrl = url[site][userChoice]
        
        soup = getResponse(searchUrl)
        

        searchItem = args
        await ctx.channel.send(f"Searching for {searchItem}")

        if userChoice == "cookpad":
            searchTag = {"name": "a", "class_": "block-link__main"}
            try:
                nameAtag = soup.find("a", class_="block-link__main") 
                recipeName = nameAtag.get_text(strip=True)
                siteLink = "https://cookpad.com"
                recipeLink = siteLink + nameAtag.get('href')
                


            except(AttributeError) as e:
                await ctx.channel.send(f"Nothing found for {args}")


        while True:
            recipeName = sanitizeRecipeName(recipeName) #sanitize recipe name

            await ctx.channel.send(f"Recipe found: {recipeName}") 
            await ctx.channel.send("(A)dd recipe to !cook, (N)ext recipe,(V)iew, (S)ite using, (E)xit")
            userInput = await bot.wait_for('message', check=lambda message: cook_book.checkIfSameUser(message, ctx.author, ctx.channel))

            if userInput.content.lower() == 'a':
                await addRecipe(recipeName, recipeLink, ctx, bot)
                break
                
            elif userInput.content.lower() == "n": # broken
                try:
                    nameAtag = nameAtag.find_next(**searchTag)
                    recipeName = nameAtag.get_text(strip=True)
                    recipeLink = siteLink + nameAtag.get('href')
                except():
                    await ctx.channel.send(f"No more recipes")
                    break
                continue
            elif userInput.content.lower() == "v":
                await ctx.channel.send(f"Link: {recipeLink}")
                continue

            else:
                await ctx.channel.send("Exiting")
                break

            
        else:
            await ctx.channel.send(f"""
Options:
ss - site selected
sf - search for <Item to search for>
any other input - help page
""")
