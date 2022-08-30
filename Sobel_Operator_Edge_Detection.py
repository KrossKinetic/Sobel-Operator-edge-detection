# Imageio library simplifies reading images, like removing headers
# imageio returns a numpy array
import imageio.v3 as iio
# PIL allows me to quickly remove alpha values
from PIL import Image
# numpy arrays are in general faster than python lists, good for reading 4k images
import numpy
from math import sqrt

def save(img):
    x = img
    namefnew = input("Enter new name of the file: ")
    while True:
        print("Choose extension to store file as: ")
        print("1.JPG (Alpha data will be lost, smaller file size)")
        print("2.PNG (Alpha data will be retained, larger file size)")
        temp1 = input("Choose 1 or 2 ?: ")
        if temp1 == "1":
            img = Image.fromarray(img).convert("RGB")
            img = numpy.array(img)
            newext = ".jpg"
            break
        elif temp1 == "2":
            newext = ".png"
            break
        print("That is not an option. Please t[3] again.")
    newname = namefnew + newext
    iio.imwrite(newname,img)

def detectedge(img,height,width,type):
    tempimage = numpy.zeros([height+2,width+2,type])
    
    for i in range(1,height+1):
        for j in range(1,width+1):
            tempimage[i][j] = img[i-1][j-1]

    for i in range(0,width+2):
        for m in range(0,3):
            tempimage[0][i][m] = 0
            tempimage[height + 1][i][m] = 0

    for i in range(0,height+2):
        for m in range(0,3):
            tempimage[i][0][m] = 0
            tempimage[i][width + 1][m] = 0
            
    kR = kG = kB = 0

    for i in range(1,height+1):
        for j in range(1,width+1):
            sum = [0,0,0,0,0,0]
            for k in range(-1,2):
                for t in range(0,3):
                    sum[t] = sum[t] + (k)*tempimage[i - 1][j + k][t]            
                    sum[t+3] = sum[t+3] + (k)*tempimage[i + k][j - 1][t]
                    sum[t] = sum[t] + (k)*tempimage[i + 1][j + k][t]
                    sum[t+3] = sum[t+3] + (k)*tempimage[i + k][j + 1][t]
                    sum[t] = sum[t] + (2*k)*tempimage[i][j + k][t]
                    sum[t+3] = sum[t+3] + (2*k)*tempimage[i + k][j][t]
            
            kR = round(sqrt(sum[0]**2 + sum[3]**2))
            kG = round(sqrt(sum[1]**2 + sum[4]**2))
            kB = round(sqrt(sum[2]**2 + sum[5]**2))

            if kR >= 256:
                img[i - 1][j - 1][0] = 255
            else:
                img[i - 1][j - 1][0] = kR

            if kG >= 256:
                img[i - 1][j - 1][1] = 255
            else:
                img[i - 1][j - 1][1] = kG

            if kB >= 256:
                img[i - 1][j - 1][2] = 255
            else:
                img[i - 1][j - 1][2] = kB

nameold = str(input("Enter name of the file with the file extension: "))
temp1 = iio.imread(nameold)
img = temp1.copy()
height = img.shape[0]
width = img.shape[1]
type = img.shape[2]
detectedge(img,height,width,type)
save(img)