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

### TagsParsing v1.0.0

A program that receives all existing tags from the site https://rule34.paheal.net. After full parsing, the program collects all tags into one tags.json file. This file is needed for the program that we will analyze next.
Also, this program should be run 2 times a month, as additional tags may appear on the site. Requires internet connection to work
