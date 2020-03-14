import discord
import requests
import json
from random import randrange
from secrets import secret_dict, maskmaker_url

client = discord.Client()

@client.event
async def on_ready():
    print("The Hedrographer is present.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!r'):
        try:
            dice_to_roll = int(message.content[2])
            rolls = [randrange(1, 11) for die in range(dice_to_roll)]
            best_roll = max(rolls)
            
            result = ""
            if best_roll == 1:
                result = "Critical Failure (take double stress)"
            elif best_roll > 1 and best_roll < 6:
                result = "Failure (take stress)"
            elif best_roll > 5 and best_roll < 8:
                result = "Success at a Cost (take stress)"
            elif best_roll > 7 and best_roll < 10:
                result = "Success (take no stress)"
            elif best_roll == 10:
                result = "Critical Success (inflict {} stress)".format(rolls.count(10))

            chat_message = "```Rolled {} dice, results: {}\n".format(dice_to_roll, rolls)
            chat_message += "Result: {}\n".format(best_roll)
            chat_message += "{}\n```".format(result)

            await client.send_message(message.channel, chat_message)
        except Exception:
            await client.send_message(message.channel, "Floor dice don't count")
    if message.content.startswith('!g'):
        #try:
        split_message = message.content.split(" ")
        response = requests.post(maskmaker_url, json={"number": 1, "attributes": ["Pride", "Intellect", "Weirdness", "Strength", "Paranoia"]}).text
        response = json.loads(response)
        chat_message = "```"
        for character in response['characters']:
            chat_message += "Name: {}\n".format(character['name'])
            chat_message += "Traits: {}\n".format(character['traits'])
            chat_message += "Attributes: {}\n".format(character['attribute'])
        chat_message += "```"
        await client.send_message(message.channel, chat_message)
        #except Exception:
        #    await client.send_message(message.channel, "Uhh... his name is.... uhhhh.... Dave. The Elf.")
client.run(secret_dict['client_key'])
