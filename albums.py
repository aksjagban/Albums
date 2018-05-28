# Program takes selected albums data (i.e. #id, artist, album, year) which I have in my Linux directory: /home/user/Music/Albums and returns script.sql to insert album data as values into table created in MySQL database. 
# All used folders have in this case the same structure: /home/user/Music/Albums/Artist/Year - Album. 
# If you want to test this program on your computer, replace 'user' catalogue name - and other catalogue names if necessary - respectively by your user name - and other catalogue names - on your Linux. 
# Folders to testing have been included in 'Albums.zip'.
# Script is executed in MySQL with command: "source script.sql".
# -*- coding: utf-8 -*-
import os
import re

albumno = 0

for artist in os.listdir(r'/home/user/Music/Albums'):
	for yearalbum in os.listdir(r'/home/user/Music/Albums'+artist):

		yearregex = re.compile(r'\d\d\d\d')
		year = yearregex.search(yearalbum)

		albumregex = re.compile(r'(?<=\d\d\d\d\s-\s).*')
		album = albumregex.search(yearalbum)

#	Problem with album names including apostrophe: '.
		apoartist = artist.replace('\'', '\\'+'\'')
		apoalbum = album.group().replace('\'', '\\'+'\'')

#	Main key as albumno.

		albumid = apoartist+apoalbum
		albumid = albumid.lower()

		nw = [' ', '\'', '\\']

		for i in albumid:
			if i in nw:
				albumid = albumid.replace(i, '')

		albumno = albumno + 1

		data = ("INSERT INTO my_albums (Album_Id, Artist , Album , Year) VALUES ('"+"#"+str(albumno)+"' , '"+apoartist+"' , '"+apoalbum+"' , "+year.group()+");")

		print(data)
		
		tosql = open('script.sql', 'a')
		tosql.write(data+"\n")


#	Escaping apostrophe.
file = open("script.sql","r")

for title in file:

	titleregex = re.compile(r'(?<=\'\s,\s\').*(?=\'\s,\s)')
	title = titleregex.search(title)

	print (title.group())

file.close


#	Adding constant sql commands in first line.
firstline = "CREATE DATABASE music;\nSELECT DATABASE();\nUSE music;\nCREATE TABLE my_albums\n(Album_Id VARCHAR(150) NOT NULL,\nArtist VARCHAR(50) NOT NULL,\nAlbum VARCHAR(100) NOT NULL,\nYear SMALLINT)ENGINE=MyISAM  DEFAULT CHARSET=utf8;\nDESCRIBE my_albums;\n"
with open('script.sql', 'r+') as f:
	script = f.read()
	f.seek(0, 0)
	f.write(firstline.rstrip('\r\n') + '\n' + script)


