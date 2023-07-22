from PIL import Image, ImageEnhance, ImageFilter
import os
path = "./Images"
pathout = '/Edited'

#os.listdir grabs extension of current path and pulls out ls of that dir

#if(os.access(path, os.F_OK)):
for file in os.listdir(path):
    print(file)
    img = Image.open(f"{path}/{file}")
    edit = img.filter(ImageFilter.GaussianBlur(2))
    name = os.path.splitext(file)
    edit.save(f'.{pathout}/{name[0]}_edited.jpg')

    #what could we add to this project?
    #choose what type of edit you want?