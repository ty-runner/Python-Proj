from pytube import YouTube
from sys import argv

link = argv[1]

yt = YouTube(link)
print("Downloading: " + yt.title)
yd = yt.streams.get_highest_resolution()
yd.download()

#how can this be grown?
#make it a global script?
#RUN FROM TERMINAL AS python -m ytdownloader "LINK"