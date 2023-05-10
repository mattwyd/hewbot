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