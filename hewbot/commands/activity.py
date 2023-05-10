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

last_write = 'last black history month'
keyList = {}
command_list = {}
image_directory = 'images'
storage_directory = 'storage'

mc_ip = '20.104.224.62:25565' #update this to be changeable in func
server = JavaServer.lookup(mc_ip)
api_endpoint = f"https://api.mcsrvstat.us/2/{mc_ip}"

minecraft_achievements = {}


@register('activity')
async def motd_command(message, args, client):
    if len(message.content) < 30:
        print(message.content[10:])
        await client.change_presence(activity=discord.Streaming(name=message.content[10:], url='https://www.youtube.com/watch?v=MRW0i5rxRvU&t=188s&ab_channel=stevenokpysh'))
