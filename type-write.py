import xml.etree.ElementTree as ET
import fileinput
import os
import cv2 as cv
import xmlformatter

print('Which manuscript (CF or Ein) should be considered:')
manu = input().strip()

if manu == 'CF':
    print('Which Calvo file number (09-20, 24-27 currently) should be parsed: ')
elif manu == 'Ein':
    print('Which Ein file number (01v-05v, 02r-05r currently) should be parsed: ')
else:
    print('Please try again.')
    exit()

file = input().strip()

stave_tree = ET.parse(f'./xml/{ manu }-0{ file }-position-updated.xml')
stave_root = stave_tree.getroot()

image = cv.imread(f'./originals/{ manu }/{ manu }-0{ file }.png')
inc = 0
for glyph in stave_root.find('glyphs'):
    uly = int(glyph.get('uly'))
    ulx = int(glyph.get('ulx'))
    nrows = int(glyph.get('nrows'))
    ncols = int(glyph.get('ncols'))

    type_class = glyph.find('type')

    cv.imshow('image', image[uly:uly+nrows,ulx:ulx+ncols])
    cv.waitKey(2)
    print('Type: ')
    type = str(input().strip())
    type_class.set('name', type)
    # if inc == 20:
    #     break
    # inc += 1

stave_tree.write(f'./xml/{ manu }-0{ file }-position-updated.xml')