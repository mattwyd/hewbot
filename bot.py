import discord
from discord.ext import tasks  # Import the tasks module from discord.ext
import commands  # Import the commands module that contains custom command functions
import json
import datetime
import os

# Set up the Discord client and enable intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
# Define the on_ready event handler
@client.event
async def on_ready():
    # Load the replies JSON file into the keyList dictionary
    try:
        with open(os.path.join(commands.storage_directory, 'replies.json'), 'r') as file:
            commands.keyList = json.load(file)
    except json.decoder.JSONDecodeError as e:
        print(f'no replies stored, hopefully this is your first time set-up')
    print(f'We have logged in as {client.user}')  # Print a message to indicate that the daily loop has run
    daily_loop.start()  # Start the daily loop task

# Define the daily_loop task that runs every 24 hours
@tasks.loop(hours=16)
async def daily_loop():
    # Update the message of the day
    await motd_update()
    
    #await commands.write_command()
# Define the motd_update function that updates the Discord bot's presence with the message of the day
async def motd_update():
    today = datetime.datetime.today()
    # Use the day of the year as the index for selecting a joke
    day_of_year = today.timetuple().tm_yday % len(commands.descriptions.jokes)
    selected_item = commands.descriptions.jokes[day_of_year]  # Get the joke at the selected index
    # Update the Discord bot's presence with the selected joke
    await client.change_presence(activity=discord.Streaming(name=selected_item, url='https://www.youtube.com/watch?v=MRW0i5rxRvU&t=188s&ab_channel=stevenokpysh'))
    channel = discord.utils.get(client.get_all_channels(), name='dabbot-spam')
    await channel.send(selected_item)
    print(f'it is day number {day_of_year} of the year')  # Print a message indicating the day of the year
    print(f'motd : {selected_item}')  # Print a message indicating the updated message of the day

# Define the on_message event handler
@client.event
async def on_message(message):
    
    # Ignore empty messages and messages sent by the bot itself
    if not message.content or message.author == client.user:
        return
    print(f'{message.channel} {message.author}: {message.content}')  # Print the author and content of the received message

    content = message.content.replace(',', '')  # Remove commas from the message content

    if content in commands.keyList:
        # Retrieve the response associated with the message content key from the keyList dictionary
        response = commands.keyList[content].replace('[', '').replace(']', '').replace("'", '').split(',')
        # Check the length of the response to determine how to handle it
        echo = commands.command_list['echo']
        gimme = commands.command_list['gimme']
        if len(response) == 2:
            # If the response contains two elements, send the first element as a text message and the second element as an image
            await echo(message, response[0], client)
            response[1] = response[1].replace('@', '').strip()
            if response[1] != '':
                await gimme(message, [response[1], ''], client)
        else:
            if '@' in response[0]:
                #send response from resopnse[0] for image
                response[0] = response[0].replace('@', '')
                await gimme(message, [response[0], ''], client)

            else:
            #send response from resopnse[0] for text
                await echo(message, response[0], client)

    elif content.startswith('.'):
        parts = content.split(' ')
        command = parts[0][1:]
        args = parts[1:]
        if commands.command_list.get(command):
            func = commands.command_list[command]
            await func(message, args, client)
    else:
        return

client.run('NTY2NjQyNTQ3NjYxOTk2MDcz.GE4So_.aFb0eMoHO9rEyKCYkz5heuc5PhHn5E-SSWVmFg')
