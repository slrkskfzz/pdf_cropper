from PyPDF2 import PdfFileWriter, PdfFileReader

input1 = PdfFileReader(open("in.pdf", "rb"))
output = PdfFileWriter()

numPages = input1.getNumPages()
print ("document has %s pages." % numPages)

position = [[(0.2, 0.8)], [(0.543, 0.543+0.317), (0.1445, 0.1445+0.317)]]  # for 2-up

for i in range(numPages):
    
    #print (page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())
    #page.trimBox.lowerLeft = (40, 40)
    #page.trimBox.upperRight = (225, 225)
    for x_pos in position[0]:
        for y_pos in position[1]:
            input1 = PdfFileReader(open("in.pdf", "rb"))
            page = input1.getPage(i)
            W = int(page.mediaBox.getUpperRight_x())
            H = int(page.mediaBox.getUpperRight_y())
            xs = x_pos[0] * W
            xe = x_pos[1] * W
            ys = y_pos[0] * H
            ye = y_pos[1] * H

            print("%f.%f > %d %d %d %d" % (y_pos[0], y_pos[1], xs, xe, ys, ye))
            page.cropBox.lowerLeft = (xs, ys)
            page.cropBox.upperRight = (xe, ye)
            output.addPage(page)

outputStream = open("out.pdf", "wb")
output.write(outputStream)
outputStream.close()