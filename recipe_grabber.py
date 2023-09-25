from bs4 import BeautifulSoup
import requests
import re
import string

searchItem = input("What tingles your sack today?\n")

url = f"http://rule34.paheal.net/post/list/{searchItem}/1"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.findAll('div', {'class': 'shm-thumb thumb'})


filePath = input(
    "Where would you like to save it my child:\n") or "/home/lilpeenieweenie/wkfolder/myCode"
names = []
srcs = []

def main():
    
    downloadWebContent()


def createFile():

    try: 
        outFile = open(filePath+f'/{searchItem}.txt', 'x')
    except IOError:
        outFile = open(filePath+f'/{searchItem}.txt', 'a')
    return outFile

def splitNumbers(names): #shortens name of file 

    text = ""
    characters = []
    num = ""

    for name in names: 
        for i in name: 
            if(i.isalpha()):
                text += i
            else: num += i

        characters.append(text)
        charlen = len(characters)
        final = characters[charlen-1]
    return(final)

def downloadWebContent():
    for t in tbody:
        srcs =  t.br.next_sibling['href']
        names = t.img['title']
        filteredNames = splitNumbers(names)
        r = requests.get(srcs, allow_redirects=True)

        open(filePath+"/"+filteredNames 
        +checkFileType(names), 'wb').write(r.content)



def checkFileType(filteredNames):
    for name in filteredNames:
        if(name.__contains__('jpg')):
            return('.jpg')
        elif(name.__contains__('png')):
            return('.png')
        else: return '.jpg'

main()



# want to use .__contains__('string') to see if pdf, jpg etc and then make the file