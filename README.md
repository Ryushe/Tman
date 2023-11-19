# Tman - the bot about mo

Discord bot that contains many different functionalities:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Recipe book  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Update about anime episode drops  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Image scraper (sends image to user specified)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and much much more

## Installing

```
git clone https://github.com/LilPeenieWeenie/Tman.git && cd Tman
```

```
echo "DISCORD_TOKEN=<put your bot token here>" > .env
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

## Built With

* [BS4](https://beautiful-soup-4.readthedocs.io/en/latest/) - Web Scraping Framework Used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Authors

* **LilPeenieWeenie** - (https://github.com/LilPeenieWeenie)
