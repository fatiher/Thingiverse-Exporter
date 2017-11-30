#!/usr/bin/python
# -*- coding: utf-8 -*-

# Thingiverse Exporter
# Fatih ER (http://www.fatiher.com)
# forked from the works of Carlos Garcia Saura (http://carlosgs.es)
# CC-BY-SA license (http://creativecommons.org/licenses/by-sa/3.0/)
# https://github.com/fatiher/Thingiverse-Exporter
# *Unofficial program, not associated with Thingiverse
# Use at your own risk!

# Modules
import requests
from bs4 import BeautifulSoup
import os,sys
import re
import urllib
import time
from natsort import natsort, ns

reload(sys)
sys.setdefaultencoding('utf-8') # Setting default encoding to utf-8

# EDIT THIS!
# --------------------------------------------------------------
user = "fatiher" # User from Thingiverse (as in the profile URL)
authorName = "fatihER" # Any string is OK
authorDescription = "<http://fatiher.com/>"

readmeHeader = "*** This list of things was [automatically generated](https://github.com/fatiher/export-things). ***  \n"

thingReadmeHeader = "*** Please note: This thing is part of a list that was [automatically generated](https://github.com/fatiher/export-things) and may have been updated since then. Make sure to check for the current license and authorship. ***  \n"

#listPageTitle = "Things designed by " + authorName
listPageTitle = "Things liked by " + authorName

urlPathToDownload = "/likes/page:" # "/designs/page:" # Set to the url you want to download from (either your posted designs or your liked designs)

authorMark = True # If set true, will write your author name and description at the bottom of all pages

downloadFiles = True # If set to false, will link to original files instead of downloading them
redownloadExistingFiles = False # This saves time when re-running the script in long lists (but be careful, it only checks if file already exists - not that it is good -)

redownloadExistingThings = False # If set False, it won't re-download anything from things that already have a folder (be careful, it ONLY checks if the THING FOLDER already exists - not that it is good -). Useful to save time when resuming long lists

url = "https://www.thingiverse.com"
# ---------------------------------------------------------------


# Helper function to create directories -------------------------
# ---------------------------------------------------------------
def makeDirs(path):
	try:
		os.makedirs(path)
	except:
		return -1
	return 0
# ---------------------------------------------------------------

# Helper function to perform the required HTTP requests ---------
# ---------------------------------------------------------------
def httpGet(page, filename=False, redir=True):
	if filename and not redownloadExistingFiles and os.path.exists(filename):
		return [] # Simulate download OK for existing file
	try:
		r = requests.get(page, allow_redirects=redir)
	except:
		time.sleep(10)
		return httpGet(page, filename, redir)
	if r.status_code != 200:
		print("\nHTTP Response ( " + str(r.status_code) + " )\n")
		return None
	if not filename:
		# Remove all non ascii characters
		text = (c for c in r.content if 0 < ord(c) < 127) # changed from r.text to r.content
		text = ''.join(text)
		return text.encode('ascii', 'ignore')
	else:
		with open(filename, 'wb') as fd:
			for chunk in r.iter_content(512):
				fd.write(chunk)
			fd.close()
		return r.history
# ---------------------------------------------------------------

# Helper function to remove all html tags and format to a BeautifulSoup object
# This is a patch, since the getText function gives problems with non-ascii characters
# ---------------------------------------------------------------
def myGetText(BScontent):
	try:
		text = str(BScontent.getText(separator=u' ')) # Won't work with non-ascii characters
	except:
		text = re.sub('<[^<]+?>', '', str(BScontent)) # If there are non-ascii characters, we strip tags manually with a regular expression
	return text.strip() # Remove leading and trailing spaces
# ---------------------------------------------------------------

# Helper function to get preview image path of all thing folders
# ---------------------------------------------------------------
def find_preview(dir):
	pattern = ".*preview\_card.*\Z(?ms)"
	imgpath = dir + str('/img/')
	
	if os.path.exists(imgpath):
		for f in os.listdir(imgpath):
			if re.search(pattern, f):
				return(f)
	else:
		return("../../na.png") # Default preview not available image path
# ---------------------------------------------------------------

# Helper function to make HTML Directory of all things archived.
# ---------------------------------------------------------------
def makeThingList():
	html_str_begin = """
<html lang="en-US" prefix="og: http://ogp.me/ns#" class="">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width">
	<title>Thingiverse Exporter</title>
<style>
body {
    font: 1em/1.67 Arial, Sans-serif;
    margin: 0;
	background: #87e0fd; /* Old browsers */
	background: -moz-linear-gradient(-45deg, #87e0fd 0%, #53cbf1 40%, #05abe0 100%); /* FF3.6-15 */
	background: -webkit-linear-gradient(-45deg, #87e0fd 0%,#53cbf1 40%,#05abe0 100%); /* Chrome10-25,Safari5.1-6 */
	background: linear-gradient(135deg, #87e0fd 0%,#53cbf1 40%,#05abe0 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#87e0fd', endColorstr='#05abe0',GradientType=1 ); /* IE6-9 fallback on horizontal gradient */
	color: #3f4c6b;
}

img, iframe {
max-width: 100%;
height: auto;
padding: 1.5em;
display: block;
}

.wrapper {
    width: 95%;
    margin: 1.5em auto;
}

.masonry {
	margin: 1.5em 0;
	padding: 0;
	-moz-column-gap: 1.5em;
	-webkit-column-gap: 1.5em;
	column-gap: 1.5em;
	font-size: .50em;
	display: grid;
	grid-auto-rows: 50px;
	grid-gap: 10px;
	grid-template-columns: repeat(auto-fill, minmax(30%, 1fr));
}

.item {
	column-count: 3;
	grid-row: span 5;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1em;
	font-weight: regular;
	background: #fff;
	padding: 1.1em;
	margin: 0 0 1.1em;
	width: 100%;
	box-sizing: border-box;
	-moz-box-sizing: border-box;
	-webkit-box-sizing: border-box;
	box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.18);
	border-radius: 3px;
	-moz-border-radius: 3px;
	-webkit-border-radius: 3px;
}

.title, .footer {
text-align: center;
}

.title {
font-size: 1.2em;
margin: .25em 0;
}

.title a {
display: inline-block;
padding: .75em 1.25em;
color: #888;
border: 2px solid #aaa;
margin: .25em 1em 1em;
text-decoration: none;
border-radius: 3px;
-moz-border-radius: 3px;
-webkit-border-radius: 3px;
-ms-border-radius: 3px;
-o-border-radius: 3px;
}

.title {
color: #3f4c6b;
}

.title a:hover {
color: #3f4c6b;
border-color: #888;
}

a {
color: #3f4c6b;
}


@media only screen and (min-width: 700px) {
    .masonry {
        -moz-column-count: 2;
        -webkit-column-count: 2;
        column-count: 2;
    }
}

@media only screen and (min-width: 900px) {
    .masonry {
        -moz-column-count: 3;
        -webkit-column-count: 3;
        column-count: 3;
    }
}

@media only screen and (min-width: 1100px) {
    .masonry {
        -moz-column-count: 4;
        -webkit-column-count: 4;
        column-count: 4;
    }
}

@media only screen and (min-width: 1280px) {
    .wrapper {
        width: 1260px;
    }
}</style></head>
<body>
	<div class="wrapper">
"""	
	dirpath = '.'
	files = natsort.natsorted((os.listdir(dirpath)), reverse=True, alg=ns.PATH, key=os.path.getctime)
	#files = os.listdir(dirpath)
	
	tlf = open("ThingList.html", 'w') # Generate the global Thing Directory file with the list of the all things archived.
	tlf.write(html_str_begin)
	tlf.write('<div class="title"><h1>Thingiverse Exporter</h1></div>')
	tlf.write('<div class="title"><h2>' + listPageTitle + '</h2></div>')
	tlf.write('<div class="title"><strong>' + readmeHeader + '</strong></div>')
	tlf.write('    <div class="masonry">')

	itemCount = 1

	for dirname in files:
		full_path = os.path.join(dirpath, dirname)
		#inode = os.stat(full_path)
	
		if os.path.isdir(full_path):
			previewImage = find_preview(dirname)
			
			tlf.write('<div class="item"><img src="' + str(dirname).encode('utf-8') + '/img/' + str(previewImage).encode('utf-8') + '" alt="Preview Image" /><br/>\n')
			tlf.write('<h2>' + str(itemCount) + '. ' + '<a href="' + str(dirname).encode('utf-8') + '">' +  str(dirname).encode('utf-8').replace('-', ' ') + '</a></h2></div>\n')
			itemCount += 1

	tlf.write('</div></body></html>')
	tlf.close()
	
	print('Total things in the Archive : ' + str(itemCount-1))
	print('ThingList.html created for Thing Directory for archive') 

# ---------------------------------------------------------------
def downloadAllThings():           
	thingList = {}

	print("Username: " + user)


	thingCount = 1
	pgNum = 1
	while 1: # Iterate over all the pages of things
		print("\nPage number: " + str(pgNum))
		res = httpGet(url + "/" + user + urlPathToDownload + str(pgNum), redir=False)
		if res == None:
			break
		res_xml = BeautifulSoup(res,"lxml")
		things = res_xml.findAll("div", { "class":"thing thing-interaction-parent item-card" })
		for thing in things: # Iterate over each thing
			thingList[thingCount] = {}
			
			title = str(thing.findAll("span", { "class":"thing-name" })[0].text.encode('utf-8', 'ignore'))
			title = re.sub("\[[^\]]*\]","", title) # Optional: Remove text within brackets from the title
			title = title.strip()
			id = str(thing["data-thing-id"]) # Get title and id of the current thing
		
			thingList[thingCount]["title"] = title
			thingList[thingCount]["id"] = id
		
			print("\nProcessing thing: " + id + " : " + title)
		
			folder = id + "-" + "-".join(re.findall("[a-zA-Z0-9]+", title)) # Create a clean title for our folder
			print(folder)
			previewImgUrl = str(thing.findAll("img", { "class":"thing-img" })[0]["src"]) # Get the link for the preview image
			previewImgName = previewImgUrl.split('/')[-1]
			previewImgFile = folder + "/img/" + previewImgName
		
			thingList[thingCount]["folder"] = folder
			thingList[thingCount]["previewImgUrl"] = previewImgUrl
			thingList[thingCount]["previewImgName"] = previewImgName
			thingList[thingCount]["previewImgFile"] = previewImgFile
		
			if redownloadExistingThings or not os.path.exists(folder):
				makeDirs(folder) # Create the required directories
				makeDirs(folder + "/img")
		
				print("Downloading preview image ( " + previewImgName + " )")
				httpGet(previewImgUrl, previewImgFile) # Download the preview image
		
				print("Loading thing data")
		
				res = httpGet(url + "/thing:" + id, redir=False) # Load the page of the thing
				if res == -1:
					print("Error while downloading " + id + " : " + title)
					exit()
				res_xml = BeautifulSoup(res,"lxml")
		
				description = res_xml.findAll("div", { "id":"description" })
				if description:
					description = "".join(str(item) for item in description[0].contents) # Get the description
					description = description.strip()
				else:
					description = "None"
				thingList[thingCount]["description"] = description
			
				instructions = res_xml.findAll("div", { "id":"instructions" })
				if instructions:
					instructions = "".join(str(item) for item in instructions[0].contents) # Get the instructions
					instructions = instructions.strip()
				else:
					instructions = "None"
				thingList[thingCount]["instructions"] = instructions
			
				license = res_xml.findAll("div", { "class":"license-text" })
				if license:
					license = myGetText(license[0]) # Get the license
				else:
					license = "CC-BY-SA (default, check actual license)"
				thingList[thingCount]["license"] = license
		
		
				tags = res_xml.findAll("div", { "class":"thing-info-content thing-detail-tags-container" })
				if tags:
					tags = myGetText(tags[0]) # Get the tags
				else:
					tags = "None"
				if len(tags) < 2: tags = "None"
				thingList[thingCount]["tags"] = tags
		
		
				header = res_xml.findAll("div", { "class":"thing-header-data" })
				if header:
					header = myGetText(header[0]) # Get the header (title + date published)
				else:
					header = "None"
				if len(header) < 2: header = "None"
				thingList[thingCount]["header"] = header
		
		
				files = {}
				for file in res_xml.findAll("div", { "class":"thing-file" }): # Parse the files and download them
					fileUrl = url + str(file.a["href"])
					fileName = str(file.a["data-file-name"])
					filePath = folder + "/" + fileName
					if downloadFiles:
						print("Downloading file ( " + fileName + " )")
						httpGet(fileUrl, filePath)
					else:
						print("Skipping download for file: " + fileName + " ( " + fileUrl + " )")
			
					filePreviewUrl = str(file.img["src"])
					filePreviewPath = filePreviewUrl.split('/')[-1]
					filePreview = folder + "/img/" + filePreviewPath
					print("-> Downloading preview image ( " + filePreviewPath + " )")
					httpGet(filePreviewUrl, filePreview)
			
					files[filePath] = {}
					files[filePath]["url"] = fileUrl
					files[filePath]["name"] = fileName
					files[filePath]["preview"] = filePreviewPath
				thingList[thingCount]["files"] = files
			
				gallery = res_xml.findAll("div", { "class":"thing-page-slider main-slider" })[0]
				images = []
				images_full = {}
				for image in gallery.findAll("div", { "class":"thing-page-image featured" }): # Parse the images and download them
					imgUrl = str(image["data-large-url"])
					imgName = imgUrl.split('/')[-1]
					imgFile = folder + "/img/" + imgName
					print("Downloading image ( " + imgName + " )")
					httpGet(imgUrl, imgFile)
					images.append(imgName)
					images_full[imgFile] = {}
					images_full[imgFile]["url"] = imgUrl
					images_full[imgFile]["name"] = imgName
				thingList[thingCount]["images"] = images_full
		
				# Write in the page for the thing
				with open(folder + "/README.md", 'w') as fd: # Generate the README file for the thing
					fd.write(title)
					fd.write("\n===============\n")
					fd.write(thingReadmeHeader + "\n")
					fd.write(header)
					if len(images) > 0:
						fd.write('\n\n![Image](img/' + urllib.quote(images[0]) + ')\n\n')
					fd.write("Description\n--------\n")
					fd.write(description)
					fd.write("\n\nInstructions\n--------\n")
					fd.write(instructions)
			
					fd.write("\n\nFiles\n--------\n")
					for path in files.keys():
						file = files[path]
						fileurl = file["url"]
						if downloadFiles:
							fileurl = file["name"]
						fd.write('[![Image](img/' + urllib.quote(file["preview"]) + ')](' + file["name"] + ')\n')
						fd.write(' [ ' + file["name"] + '](' + fileurl + ')  \n\n')
			
					if len(images) > 1:
						fd.write("\n\nPictures\n--------\n")
						for image in images[1:]:
							fd.write('![Image](img/' + urllib.quote(image) + ')\n')
			
					fd.write("\n\nTags\n--------\n")
					fd.write(tags + "  \n\n")
			
					fd.write("  \n\nLicense\n--------\n")
					fd.write(license + "  \n\n")
					if authorMark:
						fd.write("\n\nBy: " + authorName + "\n--------\n")
						fd.write(authorDescription)
					fd.close()
		
			thing = thingList[thingCount]
			thingCount += 1
		
		pgNum += 1

	print("\n\nExport is complete! Do you want to generate Thing Directory Gallery?")
	input_q = raw_input("yes/NO : ")

	if input_q == str("yes") :
		makeThingList()
		print("\n\nThing Directory generated.. Quiting script. Bye!!\n")
	else:
		print("\n\nQuiting script. Bye!! \n")
			
# ---------------------------------------------------------------
def downloadThing(thingID):
	print("\nProcessing thing: " + thingID)
	print("Loading thing data")

	res = httpGet(url + "/thing:" + thingID, redir=False) # Load the page of the thing
	if res == -1:
		print("Error while downloading " + thingID + " : " + title)
		exit()
	res_xml = BeautifulSoup(res, "lxml")


	try:
		header_data = res_xml.findAll("div", { "class":"thing-header-data" })[0]
		title = str(header_data.h1.text.encode('utf-8', 'ignore'))
	except:
		title = str(res_xml.findAll("title")[0].text.encode('utf-8', 'ignore'))

	title = re.sub("\[[^\]]*\]","", title) # Optional: Remove text within brackets from the title
	title = title.strip()

	folder = thingID + "-" + "-".join(re.findall("[a-zA-Z0-9]+", title)) # Create a clean title for our folder
	print(folder)

	makeDirs(folder) # Create the required directories
	makeDirs(folder + "/img")


	description = res_xml.findAll("div", { "id":"description" })
	if description:
		description = "".join(str(item) for item in description[0].contents) # Get the description
		description = description.strip()
	else:
		description = "None"

	instructions = res_xml.findAll("div", { "id":"instructions" })
	if instructions:
		instructions = "".join(str(item) for item in instructions[0].contents) # Get the instructions
		instructions = instructions.strip()
	else:
		instructions = "None"

	license = res_xml.findAll("div", { "class":"license-text" })
	if license:
		license = myGetText(license[0]) # Get the license
	else:
		license = "CC-BY-SA (default, check actual license)"



	tags = res_xml.findAll("div", { "class":"thing-info-content thing-detail-tags-container" })
	if tags:
		tags = myGetText(tags[0]) # Get the tags
	else:
		tags = "None"
	if len(tags) < 2: tags = "None"



	header = res_xml.findAll("div", { "class":"thing-header-data" })
	if header:
		header = myGetText(header[0]) # Get the header (title + date published)
	else:
		header = "None"
	if len(header) < 2: header = "None"


	files = {}
	for file in res_xml.findAll("div", { "class":"thing-file" }): # Parse the files and download them
		fileUrl = url + str(file.a["href"])
		fileName = str(file.a["data-file-name"])
		filePath = folder + "/" + fileName
		if downloadFiles:
			print("Downloading file ( " + fileName + " )")
			httpGet(fileUrl, filePath)
		else:
			print("Skipping download for file: " + fileName + " ( " + fileUrl + " )")

		filePreviewUrl = str(file.img["src"])
		filePreviewPath = filePreviewUrl.split('/')[-1]
		filePreview = folder + "/img/" + filePreviewPath
		print("-> Downloading preview image ( " + filePreviewPath + " )")
		httpGet(filePreviewUrl, filePreview)

		files[filePath] = {}
		files[filePath]["url"] = fileUrl
		files[filePath]["name"] = fileName
		files[filePath]["preview"] = filePreviewPath

	gallery = res_xml.findAll("div", { "class":"thing-page-slider main-slider" })[0]
	images = []
	for image in gallery.findAll("div", { "class":"thing-page-image featured" }): # Parse the images and download them
		imgUrl = str(image["data-large-url"])
		imgName = imgUrl.split('/')[-1]
		imgFile = folder + "/img/" + imgName
		print("Downloading image ( " + imgName + " )")
		httpGet(imgUrl, imgFile)
		images.append(imgName)


	# Write in the page for the thing
	with open(folder + "/README.md", 'w') as fd: # Generate the README file for the thing
		fd.write(title)
		fd.write("\n===============\n")
		fd.write(thingReadmeHeader + "\n")
		fd.write(header)
		if len(images) > 0:
			fd.write('\n\n![Image](img/' + urllib.quote(images[0]) + ')\n\n')
		fd.write("Description\n--------\n")
		fd.write(description)
		fd.write("\n\nInstructions\n--------\n")
		fd.write(instructions)

		fd.write("\n\nFiles\n--------\n")
		for path in files.keys():
			file = files[path]
			fileurl = file["url"]
			if downloadFiles:
				fileurl = file["name"]
			fd.write('[![Image](img/' + urllib.quote(file["preview"]) + ')](' + file["name"] + ')\n')
			fd.write(' [ ' + file["name"] + '](' + fileurl + ')  \n\n')

		if len(images) > 1:
			fd.write("\n\nPictures\n--------\n")
			for image in images[1:]:
				fd.write('![Image](img/' + urllib.quote(image) + ')\n')

		fd.write("\n\nTags\n--------\n")
		fd.write(tags + "  \n\n")

		fd.write("  \n\nLicense\n--------\n")
		fd.write(license + "  \n\n")
	
	print("\n\nExport is completed.. Keep knowledge free!!\n")
	print("\n\nQuiting script. Bye!! \n")

print("                                                       ")
print(" _____ _   _         _                                 ")
print("|_   _| |_|_|___ ___|_|_ _ ___ ___ ___ ___             ")
print("  | | |   | |   | . | | | | -_|  _|_ -| -_|            ")
print("  |_| |_|_|_|_|_|_  |_|\_/|___|_| |___|___|            ")
print("                |___|                                  ")
print("                                                       ")
print("                     _____                 _           ")
print("                    |   __|_ _ ___ ___ ___| |_ ___ ___ ")
print("                    |   __|_'_| . | . |  _|  _| -_|  _|")
print("                    |_____|_,_|  _|___|_| |_| |___|_|  ")
print("                              |_|                      ")
print("\n-------------------------------------------------------")
print("\n 1. Export All Things ")
print(" 2. Export Thing with Thind ID ")
print(" 3. Generate Thing Directory Gallery ")
print("\n-------------------------------------------------------")
input = raw_input("Please select operation : ")

if input == str(1) :
	downloadAllThings()
else:
	if input == str(2) :
		thingID = raw_input("Please enter ThingID : ")
		downloadThing(thingID)
		
	else:
		if input == str(3) :
			makeThingList()
		else:
			print("unknow selection, quiting script!")
