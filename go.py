import sys
import os
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader


inname = sys.argv[1]
outname= inname.replace(".pdf", "_out.pdf")

print("Obtaining the positions for cropping")

comm = "gswin64c -dFirstPage=1 -dLastPage=1 -dBATCH -dNOPAUSE -sDEVICE=pnggray -r300 -dUseCropBox -sOutputFile=temp-%%03d.png  %s" % inname
os.system(comm)

I = Image.open("temp-001.png")
W, H = I.size

# Vertical
ys1, ye1, ys2, ye2 = 0, 0, 0, 0
state = 0
for y in range(0, H//2):
    if I.getpixel((W//2, y)) == 0:
        state = 1
    elif state != 0:
        ys1 = y
        break

state = 0        
for y in range(H//2, 0, -1):
    if I.getpixel((W//2, y)) == 0:
        state = 1
    elif state != 0:
        ye1 = y
        break

        
state = 0
for y in range(H//2, H):
    if I.getpixel((W//2, y)) == 0:
        state = 1
    elif state != 0:
        ys2 = y
        break
        
state = 0
for y in range(H-1, H//2, -1):
    if I.getpixel((W//2, y)) == 0:
        state = 1
    elif state != 0:
        ye2 = y
        break

yy = (ys1 + ye1) // 1
xs, xe = 0, 0

state = 0
for x in range(0, W):
    if I.getpixel((x, yy)) == 0:
        state = 1
    elif state != 0:
        xs = x
        break

state = 0
for x in range(W-1, 0, -1):
    if I.getpixel((x, yy)) == 0:
        state = 1
    elif state != 0:
        xe = x
        break

os.system("del temp-001.png")


xs /= W
xe /= W

ys1 /= H
ye1 /= H
ys2 /= H
ye2 /= H

print("%f, %f, %f, %f // %f %f" % (ys1, ye1, ys2, ye2, xs, xe))

inname = "slide03-camerain3d.pdf"
outname = "slide03-camerain3d_out.pdf"

input1 = PdfFileReader(open(inname, "rb"))
output = PdfFileWriter()

numPages = input1.getNumPages()
print ("document has %s pages." % numPages)

position = [[(xs, xe)], [(1-ys1, 1-ye1), (1-ys2, 1-ye2)]]  # for 2-up

for i in range(numPages):
    
    #print (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())
    #page.trimBox.lowerLeft = (40, 40)
    #page.trimBox.upperRight = (225, 225)
    for x_pos in position[0]:
        print("Processing page %d / %d" % (i+1, numPages))
        for y_pos in position[1]:
            input1 = PdfFileReader(open(inname, "rb"))
            page = input1.getPage(i)
            W = int(page.mediaBox.getUpperRight_x())
            H = int(page.mediaBox.getUpperRight_y())
            xs = x_pos[0] * W
            xe = x_pos[1] * W
            ys = y_pos[0] * H
            ye = y_pos[1] * H

            #print("%f.%f > %d %d %d %d" % (y_pos[0], y_pos[1], xs, xe, ys, ye))
            page.cropBox.lowerLeft = (xs, ys)
            page.cropBox.upperRight = (xe, ye)
            output.addPage(page)
print("Saving to output file")
outputStream = open(outname, "wb")
output.write(outputStream)
outputStream.close()


