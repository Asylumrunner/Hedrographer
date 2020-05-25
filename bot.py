import discord
import requests
import json
from names import drow_names, aelfir_nouns, connectors
from random import randrange, choice
from secrets import secret_dict, maskmaker_url, disc_id

client = discord.Client()
client.hedro_lock = False

@client.event
async def on_ready():
    print("The Hedrographer is present.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.hedro_lock and str(message.author.id) != str(disc_id):
        return
    if message.content.startswith("!lock"):
        client.hedro_lock = True
        await message.channel.send("```The Hedral Lock Is Sealed```")
    elif message.content.startswith("!unlock"):
        client.hedro_lock = False
        await message.channel.send("```The Hedral Lock Slips Open```")
    if message.content.startswith("!d"):
        try:
            split_message = message.content.split(" ")
            dice_notation = split_message[1].split('d')
            num_dice = int(dice_notation[0])
            if num_dice > 20:
                raise ValueError("No, max 20 dice please")
            type_dice = int(dice_notation[1])
            if type_dice > 10000:
                raise ValueError("Max dice size is 10,000. What the hell do you need dice this big for")
            rolls = [randrange(1, type_dice) for die in range(num_dice)]
            chat_message = "```Rolled {}, result: {}\n".format(split_message[1], sum(rolls))
            chat_message += "Rolls: {}\n```".format(rolls)
            await message.channel.send(chat_message)
        except Exception as e:
            await message.channel.send("Floor dice don't count. (There was an exception: {})".format(e))
    if message.content.startswith('!r'):
        try:
            dice_to_roll = int("".join(message.content[2:]))
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

            await message.channel.send(chat_message)
        except Exception as e:
            await message.channel.send("Floor dice don't count. (There was an exception: {})".format(e))
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
                name_list = [choice(aelfir_nouns) + " " + choice(connectors) + " " + choice(aelfir_nouns) for x in range(20+number)]
                if "--obnoxious" in split_message:
                    name_list = [name + " " + choice(connectors) + " " + choice(aelfir_nouns) for name in name_list]
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
            await message.channel.send(chat_message)
        except Exception as e:
            await message.channel.send("Uhh... his name is.... uhhhh.... Dave. The Elf. (There was an exception: {})".format(e))
client.run(secret_dict['client_key'])
