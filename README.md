# DiscordTrophiesWidget
A way to actively and automatically see the amout of trophies you have in the current game your playing, and displaying them onto a custom widget on discord with the slide bar. You'll have the picture of the game, the name, the slider saying how much trohpies you have/Amout of trophies maximum and a little text saying your in game.

**Exept for steam you need this run on the computer you're playing for it the work** **Tuto made on and for Windows so for linux users only Steam should work sorry**

For now I only have Steam and GOG enabled but I'm working on getting other platforms done.

I'm also working on a fix for the images which in my opinions aren't always good as we don't always have the games icons.



First, you need to follow this page https://chloecinders.com/blog/discord-widgets#how-to-make-discord-widgets to make the widget.

And you can follow this youtube video to make it easier for you https://www.youtube.com/watch?v=gYv7D83u7yQ and don't forget to press publish on top of your screen so people can actually see it.

Please do not share your discord token or any personal code to anyone as you could lose your account.


After following these tutorials, you should understand how to do it and for this project, we'll only focus on the bottom widget

Because we're doing a progress bar so in the design part of the bottom widget choose "progress" 

For the content part (which is gonna be the important part) you're gonna need for both objective and progress to have everything set to User Data

<img width="182" height="488" alt="Image" src="https://github.com/user-attachments/assets/919be098-7d26-445c-b315-eedef1931a7a" /> <img width="187" height="250" alt="Image" src="https://github.com/user-attachments/assets/70302e2e-130a-4d93-9281-f66735947e8f" /> <img width="347" height="160" alt="Image" src="https://github.com/user-attachments/assets/3f19afc0-a0ca-4aa1-b321-2c36edd56028" />

As you can see in these I enabled description and max value, description isn't required but max value is if you want to have the trophies you have / max trophies so if you don't enable them you'll just have to tweak the code a bit. Having a fallback isn't necessary but I recomment you put one just in case it resets.

To not have to change anything about the files name every Data field as I did, and when you'll click on 'Sample Data' you should have the same thing as me, the names are important but the value of each Data field isn't as we're going do change it using my script.

After that, at the top of the page click save and publish if you didn't. And install my project and python. Then go inside the folder WidgetDiscordGit and open this folder in a terminal. Then do the command **pip install -r requirements.txt** or **py -m pip install -r requirements.txt** depending on your version. 

Now open the file config.py and put the informations needed in it. So your **steam api key**, your **steam ID**, your **discord app ID**, your **discord user ID** and the **token of your bot**. You can also change de def update_idle(): in discordManage.py and change the value that will be displayed when no game is on so when it's in Idle mode.

Now using a terminal opened in the folder WidgetDiscordGit, do **py .\main.py** or **python .\main.py** depending on your version. Everything should work fine and the Idle mode should be displayed instead of the the temporary one you had, so just launch a game and enjoy your trophies being displayed!
