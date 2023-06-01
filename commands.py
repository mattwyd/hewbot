import random
import requests
from PIL import Image
import discord
import os
import re
#discord staorage
import descriptions
import datetime
import random
import json
#mcstuff
from mcstatus import JavaServer
#plotting stuff
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from collections import Counter

last_write = ''
keyList = {}
command_list = {}
image_directory = 'images'
storage_directory = 'storage'

mc_ip = '20.104.224.62:25565' #update this to be changeable in func
server = JavaServer.lookup(mc_ip)
api_endpoint = f"https://api.mcsrvstat.us/2/{mc_ip}"

minecraft_achievements = {}


def register(command_str):
    def wrapper(func):
        command_list[command_str] = func
        return func
    return wrapper

@register('help')
async def help_command(message, args, client):
    hidden_commands = ['help', 'echo', 'write', 'tts']
    help_text = 'this is whats on the menu tonight:\n\n'
    if not args:
        for command in command_list:
            if command not in hidden_commands:
                help_text += f'{command}\n'
        await message.channel.send(help_text)
    else:
        await message.channel.send(f'so you want help with the {args[0]} command?...\n\n{descriptions.commands[args[0]]}')


@register('today')
async def today_command(message, args, client):
    today = datetime.datetime.today().date()
    await message.channel.send(f'{today}')

@register('echo')
async def echo_command(message, args, client):
    await message.channel.send(args)


@register('roll')
async def roll_command(message, args, client):
    # if specific args, roll 0-args
    if args:
        await message.channel.send(f'{message.author.nick} got a... {random.randint(0, int(args[0]))}!')
    # else, roll 0-100
    else:
        await message.channel.send(f'{message.author.nick} got a... {random.randint(0, 100)}!')


# lets user add images that can later be recalled through keyword functionality coming soon
@register('add')
async def add_command(message, args, client):
    # check if there is an attachment and if the user gave some keyword to refer to the image
   if message.attachments and args:
    # get url
    attachment = message.attachments[0]
    url = attachment.url

    if not url.endswith('jpg'):
        await message.channel.send('this is not a jpg.')
    else:
        # send a get request to the url and get the response
        response = requests.get(url)

        if response.status_code != 200:
            print(f'error {response.status_code}')
        else:
            file_name = f'{args[0]}.jpg'
            with open(os.path.join(image_directory, file_name), 'wb') as f:
                f.write(response.content)

            try:
                if args[1] == '-noresize':
                    await message.channel.send('saved to the server systems. congrats!')
            except IndexError:
                with Image.open(os.path.join(image_directory, file_name)) as original_image:
                    # resize the image
                    resized_image = original_image.resize((128, 128))
                    # save the resized image to a new file
                    resized_image.save(os.path.join(image_directory, file_name))
                    await message.channel.send('your jpg has been resized and saved on the server systems. congrats!')
            else:
                await message.channel.send('either you did not attach anything or you did not specify a keyword.')


@register('gimme')
async def gimme_command(message, args, client):
    try:
        await message.channel.send(file=discord.File(os.path.join(image_directory,str(args[0]) +'.jpg')))
    except:
        print(f'ERROR: the user has requested {str(args[0])} a file that does not exist')

@register('reply')
async def reply_command(message, args, client):
    #PROGRMA to register a command in the dictionry???? yaaaa
    
    text = message.clean_content.replace(',', '')
    
    
    if len(text.split('-')) < 3:
        await message.channel.send(f'look at .help reply')
        return
   
    text = text.split("-")
    keyList[text[1]] = str(text[2:])
    await message.channel.send(f'the reply {text[2]} has added')

    #write to text 
    with open(os.path.join(storage_directory, 'replies.json'), 'w') as file:
        json.dump(keyList, file, indent=4)


@register('rmreply')
async def rmreply_command(message, args, client):

    bruv = ' '
    try:
        del keyList[bruv.join(args)]  
        await message.channel.send(f'the keyword {bruv.join(args)} has been removed')
        with open(os.path.join(storage_directory, 'replies.json'), 'w') as file:
            json.dump(keyList, file, indent=4)
    except KeyError:
            await message.channel.send(f'doesnt exist in the library')

@register('write')
async def write_command(message, args, client):
    server_id = message.guild.id
    server = client.get_guild(server_id)
    print(server)
    # Get a list of channels in the server
    channels = server.text_channels
    # Print the names of all channels in the server

    await message.channel.send(f'this might take a second')
    messages = []
    for channel in channels:
        print(channel.name)
        async for message in channel.history(limit=None):
            if message.author != client.user and message.content != '' and message.content[:3] != 'htt' and message.content[0] not in '-\<>$./!,' and len(message.content) > 1 and not message.author.bot:
                messages.append({
                    "created_at": str(message.created_at)[:19],
                    "author_name": message.author.name,
                    "content": message.clean_content
                })
    print("Done fetching messages.")

    
    messages = sorted(messages, key=lambda x: x['created_at'])

    print("Done sorting messages.")

    # Write messages to file in JSON format
    with open(os.path.join(storage_directory, "backup.json"), "w") as file:
        json.dump(messages, file, indent=4)
    print("Done writing messages to file.")
    last_write = datetime.datetime.today()

@register('activity')
async def motd_command(message, args, client):
    if len(message.content) < 30:
        print(message.content[10:])
        await client.change_presence(activity=discord.Streaming(name=message.content[10:], url='https://www.youtube.com/watch?v=MRW0i5rxRvU&t=188s&ab_channel=stevenokpysh'))

@register('adv')
async def adv_command(message, args, client):
    await message.channel.send('coming soon')
    #write to text 
    with open(os.path.join(storage_directory, 'adv.json'), 'r') as file:
        minecraft_achievemnts = json.load(file)

    # Read the contents of the file into a string
    with open(os.path.join(storage_directory, 'message.txt'), 'r') as f:
        for line in file:
            if not re.match(r'<.*>', line):
                continue  # skip lines containing user messages in angle brackets
            match = re.search(r'^\[[\w\s:]+\]: (\S+) has completed the challenge \[(.+)\]', line)
            if match:
                username = match.group(1) # get the username
                achievement = match.group(2) # get the achievement
                print(username + ' has got ' + achievement)

    with open(os.path.join(storage_directory, 'adv.json'), 'w') as file:
        json.dump(minecraft_achievemnts, file, indent=4)

@register('motd')
async def motd_command(message, args, client):
     
    today = datetime.datetime.today()
    # Use the day of the month as the index for selecting an item
    date_obj = datetime.date(datetime.date.today().year, today.month, today.day)
    #we mod this to avoid index out of bounds
    day_of_year = date_obj.timetuple().tm_yday % len(descriptions.jokes)
    # Get the item at the selected index
    selected_item = descriptions.jokes[day_of_year]
    print(day_of_year)
    print(selected_item)
    await message.channel.send(selected_item)

@register('mc')
async def mc_command(message, args, client):
    status = server.status()
    # Print the number of players online
    try:
        response = requests.get(api_endpoint)
        data = response.json()
        #print(data)
        if "players" in data:
            players = data["players"]["list"]
            if players != []:
                await message.channel.send("The server has the following players online: {0}".format(", ".join(players)))
            else:
                await message.channel.send("The server has the no players online and replied in {latency} ms".format(", ".join(players)))

        else:
            await message.channel.send("No players found on the server.")
    except Exception as e:
        await message.channel.send(f"No players found on the server")
    guess = random.randint(0,100)
    print(guess)
    if guess > 95 :
        await message.channel.send(f"Server has various reports of admin abuse and admin hacking. Proceed with caution.")



@register('word')
async def word_command(message, args, client):
    await message.channel.send(f'querying the chatlogs last updated {last_write} this might take a second...')

    def contains_word_with_typos(string, word):
        for s in string.split():
            if fuzz.ratio(s.lower(), word.lower()) > 75:
                return True
        return False

    if len(args) == 2:
       
        # load json file
        with open(os.path.join(storage_directory,'backup.json')) as f:
            msgs = json.load(f)

        word_counts = {}
        # Specify word and user to filter for
        search_word = args[1]
        username = args[0]
        i = 0
        for msg in msgs:
            if msg["author_name"] == username:
                date = datetime.datetime.strptime(msg["created_at"][:10], '%Y-%m-%d') 
                word_counts[i] = date
                if contains_word_with_typos(msg["content"], search_word):
                    i = i + 1

        print(word_counts.values())
        print(word_counts.keys())
        # Plot word count over time
        plt.plot(list(word_counts.values()), list(word_counts.keys()))
        plt.xlabel('Date')
        plt.ylabel('Word Count')
        plt.xticks(rotation=90)
        plt.title(f' "{search_word}" Count Over Time by {username}')
        plt.savefig('word_count_over_time.jpg', format='jpg')
        plt.clf()

        await message.channel.send(file=discord.File('word_count_over_time.jpg'))

        os.remove("word_count_over_time.jpg")
    else:
        await message.channel.send(f"usage is .word username word ")
