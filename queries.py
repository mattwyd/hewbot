import os
import json
from fuzzywuzzy import fuzz


storage_directory = 'storage'

keyList = {}
try:
    with open(os.path.join(storage_directory, 'backup.json'), 'r') as file:
        keyList = json.load(file)
except json.decoder.JSONDecodeError as e:
    print(f'no replies stored, hopefully this is your first time set-up')

def contains_word_with_typos(string, word):
    for s in string.split():
        if fuzz.ratio(s.lower(), word.lower()) > 75:
            return True
    return False

print(contains_word_with_typos('', ''))

counts = {}
for data in keyList:
    if contains_word_with_typos(data['content'], 'apple') or contains_word_with_typos(data['content'], 'apples'):
        print(data['content'])
        author_name = data['author_name']
        if author_name in counts:
            counts[author_name] += 1
        else:
            counts[author_name] = 1

for author_name, count in counts.items():
    print(f"{author_name}: {count}")
