# Tman - the bot about mo

Discord bot that contains many different functionalities:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Recipe book  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Update about anime episode drops  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Image scraper (sends image to user specified)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and much much more

## Installing (as admin prompt)

note: install bat only installs python3, pip and discord.py microsoft c++ build tools needs seperate install
Microsoft C++ build tools: https://visualstudio.microsoft.com/downloads/?q=build+tools

```
git clone https://github.com/LilPeenieWeenie/Tman.git && cd Tman
```

```
echo "DISCORD_TOKEN=<put your bot token here>" > .env
```
optional (if not ran, manual installs for the dependencies found at bottom of page)
```
./install.bat
```

```
chmod +x ./Tman.bat
```

```
./Tman.bat
```

## Usage

Main commands:  
* !cook <option>
    * empty(anything thats not an option) - help
    * ar - add recepies <category>, <recipe>, <link> (comma seperated or whitespace seperated) CammelCase <ex: ChickenNuggets>
    * er - edit recepies (enters edit mode / follow prompts)
    * lr - list recepies <recipe name>
    * ac - add categories <category>
    * rc - remove categories <category to add> (will prompt after this is sent)
    * ec - edit categories <category> (will prompt after this is sent)
    * lc - list categories
* !search <option> #will search a recipe for the !cook command
* !botherTemo @<user> <ImageToSearch> #spams user with specified image
* !spam <word> #will send to current channel in (only works for servers)
* !update #sends recent anime list to current channel
* !sendate @<user> #sends list to user specified
* !hello # say hi to the bot
* !commands #list the commands available


```
## Dependencies

* Microsoft C++ build tools
* Python3
* pip
* Discord.py
* python - requests
* python - dotenv
* python - bs4

## Built With

* [BS4](https://beautiful-soup-4.readthedocs.io/en/latest/) - Web Scraping Framework Used

## Authors

* **LilPeenieWeenie** - (https://github.com/LilPeenieWeenie)
