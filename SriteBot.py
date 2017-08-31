import discord
import asyncio

import random
import re

client = discord.Client()

commandFlag = "s:"

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='dank memes'))

@client.event
async def on_message(message):
    if message.content.startswith(commandFlag):
        command = message.content[len(commandFlag):]
        print(commandFlag,"|",command)
        if command == "hello":
            print("Message Sender:",message.author,dir(message.author))
            await client.send_message(message.channel, "Hi "+str(message.author.nick))
        if command.startswith("rand "):
            flags = command[5:].split(" ")
            print(flags)
            if len(flags) == 3:
                if flags[0].isnumeric() and flags[1] == "to" and flags[2].isnumeric():
                    number = random.randint(int(flags[0]),int(flags[2]))
                    await client.send_message(message.channel, "Result: "+str(number))
                
    elif message.content.startswith(";;play "):
        songName = message.content[7:]
        print(songName)
        print(message.server.get_member("184405311681986560").nick)
        await client.change_nickname(message.server.get_member("184405311681986560"),"unmute for "+songName)
        await client.send_message(message.channel, "Recieved")
    
client.run("MzQ4NjUzNjAwMzQ1NDIzODcz.DIc3IQ.Ln473Gh-nANS0zidcJIKiNzKCSY")
