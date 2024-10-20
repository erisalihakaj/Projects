from pytube import YouTube
from sys import argv

link = argv[1]
yt = YouTube(link)

print("Title:", yt.title)
print("Views:", yt.views)

yvid = yt.streams.get_highest_resolution()

yvid.download('/Users/_Nightshade_/Documents/python projects/yt_download')

