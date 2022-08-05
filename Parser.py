from copy import deepcopy
import traceback
import logging
import requests
import urllib.parse
from requests import ConnectTimeout
import argparse
from bs4 import BeautifulSoup as bs
from termcolor import colored
import os
import time

VERSION = '1.0.0'


class FileManager:

	def CreateFolders(self):
		try:
			os.mkdir('gifs')
			os.mkdir('images')
			os.mkdir('videos')
		except FileExistsError:
			pass

	def SaveFiles(image_URLs):
		paths = {
			'png': 'images', 
			'jpg': 'images',
			'mp4': 'videos', 
			'gif': 'gifs'}

		file_num = 1
		for images_URL in image_URLs:
			p = requests.get(images_URL)
			time_now = time.time()
			file_type = images_URL[-3:]
			
			with open(f'{paths[f"{file_type}"]}\\{time_now}.{file_type}', 'wb') as f:
				f.write(p.content)
				f.close()
				print(colored(f'{file_num}/70 File {time_now}.{file_type} downloaded\n', 'green'))
			file_num += 1


class ArgumentsParsing:
	
	def CreateAndGetArgs(self):
		args_parser = argparse.ArgumentParser()

		args_parser.add_argument('-p', '--page', type=int, required=False, default=1, help='Parsing start page')
		args_parser.add_argument('-s', '--search', type=str, required=False, help='Parsing by search')
		args_parser.add_argument('-t', '--tags', type=str, required=False, help='Search by tags')
		args_parser.add_argument('-v', '--version', action='store_true', required=False, help='Check app version')

		self.args = args_parser.parse_args()
	
	def TagsParsing(self):
		tags = deepcopy(self.args.tags)
		self.args.tags = []
		tag = ''
		index = 0
		for i in list(tags):
			if i == ',':
				self.args.tags.append(tag)
				tag = ''
				continue
			if i == ' ':
				if list(tags)[index-1] == ',':
					continue
				else:
					pass
			
			tag += i
			index += 1
		self.args.tags.append(tag)

		tags = deepcopy(self.args.tags)
		self.args.tags = []
		for i in tags:
			if i[:1] == ' ':
				self.args.tags.append(i[1:])
			else:
				self.args.tags.append(i)

class Parser(FileManager, ArgumentsParsing):

	def __init__(self):
		self.image_URLs = []
		self.URL = 'https://rule34.paheal.net/post/list/'
		self.args = ''
		self.create_URL = False
		self.paths = {
			'png': 'images', 
			'jpg': 'images',
			'mp4': 'videos', 
			'gif': 'gifs'}


		ArgumentsParsing.CreateAndGetArgs(self)
		if self.args.search == None and self.args.tags == None:
			self.separator_URL = ''
		else:
			self.separator_URL = '/'

		if self.args.tags != None:
			ArgumentsParsing.TagsParsing(self)
	
	def Parsing(self):
		while True:
			Parser.CreateURL(self)
			try:
				src = requests.get(self.URL)
			except ConnectionError:
				print(colored('Connection error', 'red'))
				Parser.ExitProgram()
			except ConnectTimeout:
				print(colored('Server response delay. Use VPN or proxy.', 'red'))
				Parser.ExitProgram()
			else:
				print(f'= = = = = = P A G E [{self.args.page-1}] = = = = =\n')
				out = Parser.CodeStatusCheck(code=src.status_code)
				print(out[0])
				if out[1]:
					soup = bs(src.text.encode(), 'lxml')
					images_blocks = soup.find('div', class_='shm-image-list').find_all('div', class_='shm-thumb thumb')
					for block in images_blocks:
						self.image_URLs.append(Parser.ParsingImageURL(tag=str(block)))

					FileManager.SaveFiles(self.image_URLs)
				else:
					Parser.ExitProgram()
			
			self.image_URLs = []

	def SpaceKeyParsin(line):
		answer = ''
		print(line)
		for i in list(line):
			if i == ' ':
				answer += '_'
			else:
				answer += i

		return urllib.parse.quote(answer.encode('utf8'))
	
	def CreateURL(self):
		if self.create_URL == False:
			if self.args.search != None:
				self.args.search = Parser.SpaceKeyParsin(self.args.search)
				self.URL = f'https://rule34.paheal.net/post/list/{self.args.search}'
			if self.args.tags != None:
				for i in self.args.tags:
					self.URL += str(f'{Parser.SpaceKeyParsin(i)}%20')
		
		
		
		self.URL += f'{self.separator_URL}{self.args.page}'
		self.args.page += 1

	def ParsingImageURL(tag):
		URL = ''
		first_href_find = False
		tag = tag.split()
		for i in tag:
			if i[:6] == 'href="':
				if first_href_find:
					URL = i[6:-6]
					break
				else:
					first_href_find = True
		
		if URL != '':
			return URL
		else:
			return None


	def ExitProgram():
		input(colored('Press enter to exit...', 'red'))
		exit(1)
	
	def CodeStatusCheck(code):
		codes = {
			200: [colored('Ready for parsing!', 'cyan'), True],
			302: [colored('No more pages', 'red'), False],
			404: [colored('Page not found', 'red'), False],
			429: [colored('Sending ban', 'red'), False],
			500: [colored('The server cannot process the request', 'red'), False],
			403: [colored('Site access denied', 'red'), False]
		}

		try:
			return codes[code]
		except IndexError:
			return colored(f'Code not recognized: {code} (CTRL + C for stop)', 'red')
	        	

def main():
	try:
		par = Parser()
		par.CreateFolders()
		if par.args.version:
			print(f'version6: {VERSION}')
		time_start = time.time()
		par.Parsing()
	except KeyboardInterrupt:
		print(f'The program ran for {round(time.time()-time_start, 2)} seconds')
	except ConnectionError:
		print(colored('Connection error. Check internet connection.', 'red'))
	except Exception as e:
		print(colored(f'Unknown error. The program stops working and writes the error to the log file. Brief content of the error:\n{e}', 'red'))
		logging.basicConfig(filename='log.txt', level=logging.ERROR)
		logging.error('\n--> ' + str(traceback.format_exc()))


if __name__ == '__main__':
	main()
	input(colored('Press enter to exit...', 'cyan'))