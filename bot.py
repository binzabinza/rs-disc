import discord
from DiscordManager import DiscordManager


client = discord.Client()
dm = DiscordManager()

@client.event #this is some fancy syntactic sugar saying on_ready = client.event()
async def on_ready(): #async def makes this function a coroutine
    for guild in client.guilds:
        print("Starting up...")
        if (guild.name == "GUILD"):
            break

        print(f"{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n")
        members = "\n - ".join([member.name for member in guild.members])
        print(f"Guild Members:\n - {members}")

@client.event
async def on_message(message):
    #ignore itself
    if (message.author == client.user):
        return

    #meme testing bullshit
    if (message.content.startswith('$hello there')):
        await message.channel.send('General Kenobi!')
    elif (message.content.startswith('$pray')):
        await message.channel.send('We pray to our Lord and Saviors: Jerome Powell, Dr. Fauci, and the Flying Carrots to save our portfolios and avoid hyperinflation. AMEN')
    
    #RSBOT functionality
    elif (message.content.startswith('$')):
        command, args = parse(message.content)
        response = dm.execute(command, args)
        await message.channel.send(response)

def parse(string):
    command = string.split()[0]
    args = string.split()[1:]
    return command, args
#############
client.run('')
