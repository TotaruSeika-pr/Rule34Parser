import json
import time
import argparse

VERSION = '1.0.0'

class Search:

    def __init__(self):
        self.all_tags = []
        self.find_tags = []
        self.tag_search = ''
        self.args = ''
        Search.ParsingArgs(self)

    def LoadsData(self):
        try:
            with open('tags.json', 'r', encoding='UTF-8') as f:
                self.all_tags = json.loads(f.read())
                f.close
        except FileNotFoundError:
            print('File not found. Run TagsParsing.py')
            Search.ExitProgram()

        if len(self.all_tags) == 0:
            print('No tags found in tags.json file')
            Search.ExitProgram()

    def Searching(self):
        for i in self.all_tags:
            if self.tag_search in i:
                self.find_tags.append(i)
        
        print('Similar tags: ')
        
        line = []
        for i in self.find_tags:
            if len(line) == 8:
                print(', '.join(line))
                line = []
            else:
                line.append(f'{i}')

        print(', '.join(line))

        if self.args.save:
            Search.SavingTags(self)

        self.find_tags = []


    def ParsingArgs(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-s', '--save', required=False, action='store_true', help='Saving search results')
        parser.add_argument('-v', '--version', required=False, action='store_true', help='Check app version')

        self.args = parser.parse_args()

    def ExitProgram():
        input('Press enter to exit...')
        exit(1)
    
    def SavingTags(self):
        with open(f'{self.tag_search}-{time.time()}.txt', 'w') as f:
            f.write(f"[{self.tag_search}]: {', '.join(self.find_tags)}")
            f.close()

            


def main():
    search = Search()
    if search.args.version:
        print(f'version: {VERSION}')
    search.LoadsData()
    try:
        while True:
            search.tag_search = input('\nSearch? ')
            search.Searching()
            print('CTRL + C for exit')
    except KeyboardInterrupt:
        input('\nThe program has ended. Press enter to exit... ')

if __name__ == '__main__':
    main()