import requests
import magic

from collections import Counter
from pathlib import Path
import time
import re
import os

from config import RESOLUTION
from config import SUB

home = str(Path.home())

SUBDIR = f'{home}/Pictures/wallpapers/reddit/'
MOBILE_SUBDIR = f'{home}/Pictures/wallpapers/mobile'

request_url = 'https://www.reddit.com/r/{}/top.json'
headers = {'User-agent':'ted-test'}

mime = magic.Magic(mime=True)


def main(subreddits=SUB):

        accept  = Counter() 
        decline = Counter()

        for sub in subreddits:

                print(sub)

                url = request_url.format(sub)
                r = requests.get(url, headers=headers)

                for i in r.json()['data']['children']:
                        title = i['data']['title']

                        try:
                                for pic in i['data']['preview']['images']:
                                        link = pic['source']
                                        width, height = link['width'], link['height']
                                        image_url = link['url']
                                        
                                        if sub != 'iWallpaper':
                                                
                                                if (width, height) in RESOLUTION:

                                                        accept[(width, height)] += 1

                                                        print(width,height)
                                                        image = requests.get(image_url, headers=headers)

                                                        full_path = format_name(title)

                                                        with open(full_path, 'wb') as f:
                                                                f.write(image.content)

                                                                ext = mime.from_file(full_path).split('/')[1]

                                                                file_name = f'{full_path}.{ext}'
                                                else:
                                                        decline[(width, height)] += 1

                                        if sub == 'iWallpaper':

                                                image = requests.get(image_url, headers=headers)

                                                full_path = format_name(title, directory=MOBILE_SUBDIR)

                                                with open(full_path, 'wb') as f:

                                                        f.write(image.content)

                                                        ext = mime.from_file(full_path).split('/')[1]

                                                        file_name = f'{full_path}.{ext}'

                        except:
                                pass

        print(f"Accept: {accept}")
        print(f"Decline: {decline}")


def format_name(sub_file,directory=SUBDIR):

        file_name = sub_file.replace('/', '-')
        REGEX = '[([].*?[])]'
        path = re.sub(REGEX,'', os.path.join(directory, file_name)).rstrip()

        # Remove period from end of string
        if path[-1] == '.':
                path = path[:-1]

        return path


if __name__ == '__main__':
        main()
