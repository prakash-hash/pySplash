#! /usr/bin/env python3

import requests
from oauth import url
from hidden import api_keys
import wget
import os
import platform
import subprocess

# def open_file(path):
#     if platform.system() == "Windows":
#         os.startfile(path)
#     elif platform.system() == "Darwin":
#         subprocess.Popen(["open", path])
#     else:
#         subprocess.Popen(["xdg-open", path]).

#dictinary for 
resolution_list = ["raw", "full", "regular", "small", "thumb"]

#url and api key
my_url = url(api_keys())  

#query for the image we want to search
keyword = input("Enter what type of images you want to search. ex - cat, dog, tree etc : ")

#page number
page = input("\nEnter page no. : ")

#maximum images
max_image = input("\nEnter number of maximum number of images you wan to download.(30 is max) : ")

#choosing the resolution
quality = -1
while quality not in range(1,6):
	quality = int(input("\nChoose resolution of the image : \n1.raw\n2.full\n3.regular\n4.small\n5.thumb\n: "))


flag = True
#merging all the queries
try:
	search = requests.get(my_url+"&page={}&per_page={}&query={}".format(page, max_image, keyword,))
except socket.gaierror:
	print("Something Went Wrong please try again or after sometime")
	flag = False

if flag:
		#printng the allowed limit and remaining tries
	print("---------------------------------------------------------------------------------------")
	print("X-Ratelimit-Limit:{}\nX-Ratelimit-Remaining:{}".format(search.headers['X-Ratelimit-Limit'], 
		search.headers['X-Ratelimit-Remaining']))

	#printing the status code of the response
	print("Response code : ",search.status_code)
	print("---------------------------------------------------------------------------------------")

	#empty path
	path = ''

	if search.status_code == 200:
		
		if(int(search.headers['X-Ratelimit-Remaining']) > 10): #to limit the requests 50 to 40/hr

			#opening the default linux file manager
			path = subprocess.check_output("zenity --directory --file-selection", shell=True).strip().decode()
			
			#checking if folder exists or not
			if not os.path.exists(path+'/{}'.format(keyword)):
				os.mkdir(path+'/{}'.format(keyword))
			
			#changing to the destination folder
			os.chdir(path+'/{}'.format(keyword))
		
			#saving files
			for image in search.json()['results']:
				url2 = image['urls'][resolution_list[quality-1]]
				wget.download(url2, '{}.jpeg'.format(image["id"]))
				print('{}.jpeg done\n'.format(image["id"]))
			
			#opening the destination folder	
			# subprocess.call('nautilus --browser {}'.format(path+'/{}'.format(keyword)), shell = True)
		print("\nDone\n")
