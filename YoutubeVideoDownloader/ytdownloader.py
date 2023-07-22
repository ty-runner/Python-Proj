from pytube import YouTube
from sys import argv

link = argv[1]

yt = YouTube(link)
print(yt.title)


#RUN FROM TERMINAL AS python -m ytdownloader "LINK"