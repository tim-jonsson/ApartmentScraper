import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
import re
import json

with open('./settings.json', 'r') as file:
    settings_dict = json.load(file)

    options = FirefoxOptions()
    options.add_argument("--headless")
    url = settings_dict["url"]

    token = settings_dict["token"]

    def getSoup():
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(10) # Wait until the JS has loaded.
        return BeautifulSoup(driver.page_source, features="lxml")

    def getAparmentNumbers():
        pre_processed = getSoup().find_all("span", class_="pl-2 object-preview-description-cc")[1].text
        temp = re.findall(r'\d+', pre_processed)
        return list(map(int, temp))[0]

    intents = discord.Intents().all()

    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.listen()
    async def on_ready():
        task_loop.start()

    @tasks.loop(minutes=1)
    async def task_loop():
        channel = bot.get_channel(settings_dict["channel"])
        number_of_apartments = getAparmentNumbers()
        if(number_of_apartments != 0):
            await channel.send(f"<@{settings_dict["user"]}> There are new apartments available ({number_of_apartments})!")

    bot.run(token)







