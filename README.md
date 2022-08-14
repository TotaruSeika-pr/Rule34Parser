# Documentation for Rule34Parser

#### Installation for python:
`git clone https://github.com/TotaruSeika-pr/Rule34Parser`

#### For python users, you need to make sure that all the necessary libraries are installed with the command:
`pip install requests lxml argparse beautifulsoup4 termcolor`

##### The project is currently divided into 3 programs:

+ TagsParsing
+ TagSearch
+ Parser

##### About each in order.

## TagsParsing v1.0.0

A program that receives all existing tags from the site https://rule34.paheal.net. After full parsing, the program collects all tags into one tags.json file. This file is needed for the program that we will analyze next.
Also, this program should be run 2 times a month, as additional tags may appear on the site. Requires internet connection to work.

## TagSearch v1.0.0

Script to search for existing tags. Uses the tags.json file to work. Asks you for the search text and returns a list of similar tags.

##### The script has keys:

##### `--save or -s` - Saves all search results to files.

##### `--version or -v` - Before starting work, the program displays its version.

## Parser v1.0.0
The main program for downloading media content. After the first launch, it creates 3 folders for pictures, videos and gifs. The program can work both without additional commands and with keys.

##### `--version or -v` - Before starting work, the program displays its version.

##### `--page or -p` - Sets the parsing start page

##### `--search or -s` - When the key is activated, the program will parse according to a certain pseudo-tag. Only 1 pseudo tag possible.

##### `--tags or -t` - It accepts as parameters a string of tags, separated by a comma, by which it performs parsing. It is important to know that the program will generate an error if you specify more than three tags without being authorized on the site.

