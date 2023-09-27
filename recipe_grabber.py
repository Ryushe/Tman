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

def addRecipe():
    return 0

async def main(ctx, *args, bot):
    site = "sites"
    userChoice = url["userchoice"]

    if args[0].lower() == 's':
        await ctx.channel.send(f"Searching on {userChoice}")
    else:
        if args[0]:
            searchUrl = url[site][userChoice] + args[0]
        else:
            searchUrl = url[site][userChoice]
        
        soup = getResponse(searchUrl)
        

        searchItem = args[0]
        await ctx.channel.send(f"Searching for {searchItem}")

        if userChoice == "cookpad":
            # Find the <a> tag
            try:
                
                nameAtag = soup.find("a", class_="block-link__main")
                recipeName = nameAtag.get_text(strip=True)
                recipeLink = "https://cookpad.com" + nameAtag.get('href')
                
                while True:
                    for char in recipeName:
                        if char.isspace():
                            sanitizedRecipeName = removeWhitespaces(recipeName).lower()
                            break
                        else: sanitizedRecipeName = recipeName
                        

                    await ctx.channel.send(f"Recipe found: {recipeName}")
                    await ctx.channel.send("(A)dd recipe to !cook, (N)ext recipe,(V)iew, (S)ite using, (E)xit")
                    userInput = await bot.wait_for('message', check=lambda message: cook_book.checkIfSameUser(message, ctx.author, ctx.channel))

                    if userInput.content.lower() == 'a':

                        await ctx.channel.send(aOptions) # var at top page
                        category = await bot.wait_for('message', check=lambda message: cook_book.checkIfSameUser(message, ctx.author, ctx.channel))

                        try: await cook_book.addRecipe(ctx, category.content.lower(), sanitizedRecipeName, recipeLink)
                        except: await ctx.channel.send(f"Recipe couldn't be added")
                        break

                    elif userInput.content.lower() == "n": # broken
                        try:
                            nameAtag = nameAtag.find_next("a", class_="block-link__main")
                            recipeName = nameAtag.get_text(strip=True)
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

            except(AttributeError) as e:
                await ctx.channel.send(f"Nothing found for {args[1]}")
        else:
            await ctx.channel.send(f"""
Options:
ss - site selected
sf - search for <Item to search for>
any other input - help page
""")
    
    # filePath = input(
    #     "Where would you like to save it my child:\n") or "/home/lilpeenieweenie/wkfolder/myCode"
    # names = []
    # srcs = []

    # def main():
        
    #     downloadWebContent()


    # def createFile():

    #     try: 
    #         outFile = open(filePath+f'/{searchItem}.txt', 'x')
    #     except IOError:
    #         outFile = open(filePath+f'/{searchItem}.txt', 'a')
    #     return outFile

    # def splitNumbers(names): #shortens name of file 

    #     text = ""
    #     characters = []
    #     num = ""

    #     for name in names: 
    #         for i in name: 
    #             if(i.isalpha()):
    #                 text += i
    #             else: num += i

    #         characters.append(text)
    #         charlen = len(characters)
    #         final = characters[charlen-1]
    #     return(final)

    # def downloadWebContent():
    #     for t in tbody:
    #         srcs =  t.br.next_sibling['href']
    #         names = t.img['title']
    #         filteredNames = splitNumbers(names)
    #         r = requests.get(srcs, allow_redirects=True)

    #         open(filePath+"/"+filteredNames 
    #         +checkFileType(names), 'wb').write(r.content)



    # def checkFileType(filteredNames):
    #     for name in filteredNames:
    #         if(name.__contains__('jpg')):
    #             return('.jpg')
    #         elif(name.__contains__('png')):
    #             return('.png')
    #         else: return '.jpg'




    # want to use .__contains__('string') to see if pdf, jpg etc and then make the file