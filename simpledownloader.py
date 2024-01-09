from pytube import YouTube
from tkinter import *
import customtkinter
import threading
import re

def clean_urls(urls):
	"""
	clean_urls takes a list of strings (urls) and filters out specific characters from each item.

	-returns a list

	-urls: the list of strings(urls), type list
	"""

	clean_urls = []

	for url in urls:
		url = re.sub("\\|_'\"%&*()|`", "", url) #filter out some characters
		clean_urls.append(url)

	return clean_urls

def download_as_mp4(url): #download as mp4
	"""
	download_as_mp4 downloads some content as a .mp4 file.

	-does not return anything

	-url: the url for the content to be downloaded, type string
	"""

	video = YouTube(url)
	video = video.streams.get_highest_resolution()
	print("Started downloading: "+url)
	try:
		video.download()
		print("Finished downloading: "+url)
	except Exception as e:
		print(e)


def download_as_mp3(url): #download as mp3
	"""
	download_as_mp4 downloads some content as a .mp3 file.

	-does not return anything

	-url: the url for the content to be downloaded, type string
	"""

	video = YouTube(url)
	print("Started downloading: "+url)
	try:
		video_audio = video.streams.filter(only_audio=True).first()
		video_audio.download(filename=f"{video.title}.mp3")
		print("Finished downloading: "+url)
	except Exception as e:
		print(e)

def getText(): #get urls from text-box
	"""
	getText gets the text in the GUI textbox and downloads the url(s) in the selected filetype.

	-does not return anything
	"""

	urls = textbox.get('1.0', "end-1c").splitlines()
	textbox.delete('1.0', "end") #clear textbox
	urls = clean_urls(urls)

	for url in urls: 
		if mp4_download.get() == 1:
			threading.Thread(target=download_as_mp4, args=(url,), daemon=True).start()
		else:
			threading.Thread(target=download_as_mp3, args=(url,), daemon=True).start()

root = customtkinter.CTk()
root.title("Simple Downloader")
textbox = customtkinter.CTkTextbox(root)

#main download button
button = customtkinter.CTkButton(root, text="Download", command=getText)

mp4_download = IntVar() #1 -> download as .mp4, 0 -> download as .mp3

#radio buttons
choose_mp3 = customtkinter.CTkRadioButton(root, text="Download .MP3", variable= mp4_download, value=0)
choose_mp4 = customtkinter.CTkRadioButton(root, text="Download .MP4", variable= mp4_download, value=1)

textbox.pack(expand=True, fill=BOTH)
choose_mp3.pack(side=TOP, anchor=NW)
choose_mp4.pack(side=TOP, anchor=NW)
button.pack()

root.mainloop()