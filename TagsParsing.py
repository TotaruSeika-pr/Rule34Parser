import requests
from requests import ConnectTimeout
from bs4 import BeautifulSoup as bs
from termcolor import colored
import time
import json

VERSION = '1.0.0'

class TagsParser:

    def __init__(self):
        self.rule_tags_start = './:@[0123456789abcdefghijklmnopqrstuvwxyz'
        self.all_tags = []

    def Parsing(self):

        for tag in list(self.rule_tags_start):
            try:
                out = requests.get(f'https://rule34.paheal.net/tags?starts_with={tag}')
            except ConnectionError:
                print(colored('Connection error. Check internet connection', 'red'))
                TagsParser.ExitProgram()
            except ConnectTimeout:
                print(colored('Server response delay. Use VPN or proxy.', 'red'))
                TagsParser.ExitProgram()
            else:
                print(f'\n\tT A G : "{tag}"\n')
                print(TagsParser.CodeStatusCheck(out.status_code))
                soup = bs(out.text.encode(), 'lxml')
                a_tags = soup.find('section', id='Tagsmain').find('div', class_='blockbody').find_all('a')

                for i in range(41): # Removing unnecessary tags
                    a_tags.pop(0)
                
                for i in range(len(a_tags)): # Getting text content from a tag
                    a_tags[i] = a_tags[i].text

                self.all_tags += a_tags
            
            print(colored(f'Parsing of the "{tag}" tag is complete! Number of tags: {len(a_tags)}', 'green'))

    def ExitProgram():
        input('Press enter to exit...')
        exit(1)
    
    def CodeStatusCheck(code):
        codes = {
            200: colored('Ready for parsing!', 'cyan'),
            302: colored('No more pages (CTRL + C for stop)', 'red'),
            404: colored('Page not found (CTRL + C for stop)', 'red'),
            429: colored('Sending ban (CTRL + C for stop)', 'red'),
            500: colored('The server cannot process the request (CTRL + C for stop)', 'red'),
            403: colored('Site access denied (CTRL + C for stop)', 'red')
        }

        try:
            return codes[code]
        except IndexError:
            return colored(f'Code not recognized: {code} (CTRL + C for stop)', 'red')

    def SaveTags(self):
        with open('tags.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(self.all_tags))
            f.close()

def main():
    global par, time_start
    print(f'version: {VERSION}')
    try:
        par = TagsParser()
        time_start = time.time()
        par.Parsing()
        par.SaveTags()
    except KeyboardInterrupt:
       print(f'The program ran for {round(time.time()-time_start, 2)} seconds')

if __name__ == '__main__':
    main()
    print(colored(f'Parsing was successful! Total number of tags: {len(par.all_tags)}\nProgram work {round(time.time()-time_start, 2)} seconds', 'cyan'))
    input(colored('Press enter to exit...', 'cyan'))