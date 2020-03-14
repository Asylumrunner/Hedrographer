import discord
import requests
import json
from names import drow_names
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
        except Exception as e:
            await client.send_message(message.channel, "Floor dice don't count. (There was an exception: {})".format(e))
    if message.content.startswith('!g'):
        try:
            split_message = message.content.split(" ")
            try:
                number = int(split_message[1])
            except ValueError:
                number = 1
            
            try:
                species = split_message[2] if split_message[2] in ['Drow', 'Aelfir', 'Human'] else 'Drow'
            except Exception:
                species = 'Drow'
            
            if species == 'Drow':
                name_list = drow_names
            elif species == 'Aelfir':
                name_list = drow_names
            else:
                name_list = drow_names
            response = requests.post(maskmaker_url, json={"number": number, "names": name_list, "attributes": ["Pride", "Intellect", "Weirdness", "Strength", "Paranoia"]}).text
            response = json.loads(response)
            chat_message = "```"
            if "--just-names" in split_message:
                chat_message += "{}\n".format([character['name'] for character in response['characters']])
            else:
                for character in response['characters']:
                    chat_message += "Name: {}\n".format(character['name'])
                    chat_message += "Traits: {}\n".format(character['traits'])
                    chat_message += "Attributes: {}\n".format(character['attribute'])
            chat_message += "```"
            await client.send_message(message.channel, chat_message)
        except Exception as e:
            await client.send_message(message.channel, "Uhh... his name is.... uhhhh.... Dave. The Elf. (There was an exception: {})".format(e))
client.run(secret_dict['client_key'])
