import numpy as np
import cv2
import xml.etree.ElementTree as ET
import os

print('Which manuscript (CF or Ein) should be considered:')
manu = input().strip()

if manu == 'CF':
    print('Which Calvo file number (09-20, 24-27 currently) should be parsed: ')
elif manu == 'Ein':
    print('Which Ein file number (01v-05v, 02r-05r currently) should be parsed: ')
else:
    print('Please try again.')
    exit()

file = input()

img = cv2.imread(f'./originals/{ manu }/CF-0{ file }.png', 1)
img_line = cv2.imread(f'./layer/{ manu }/CF-0{ file }/CF-0{ file }_2.png')
img_glyphs = cv2.imread(f'./layer/{ manu }/CF-0{ file }/CF-0{ file }_1.png')

if img is not None:
    os.system('rm -f ./stave_boxes/*')
    os.system('rm -f ./stave_boxes_glyphs/*')
    os.system('rm -f ./stave_boxes_lines/*')



if not os.path.isdir('./stave_boxes'):
    os.system('mkdir stave_boxes')
if not os.path.isdir('./stave_boxes_lines'):
    os.system('mkdir stave_boxes_lines')
if not os.path.isdir('./stave_boxes_glyphs'):
    os.system('mkdir stave_boxes_glyphs')

stave_coords = []

stave_tree = ET.parse(f'./xml/{ manu }/CF-0{ file }-stave.xml')
stave_root = stave_tree.getroot()

for stave in stave_root.findall('staves'):
    bounding_box = stave.find('bounding_box')
    stave_coords.append([
        0,
        int(bounding_box.find('uly').text),
        int(bounding_box.find('nrows').text),
        int(bounding_box.find('ulx').text),
        int(bounding_box.find('ncols').text)
    ])

col = 1

stave_coords = np.array(stave_coords)

stave_coords = stave_coords[np.argsort(stave_coords[:,1])]


x_start = 10**20
x_end = 0

index = 0
increment = 0

# Loop for numbering stave fractions into the same vertical orientation

for y_dim in stave_coords:
    print(y_dim[0])
    if y_dim[3] < x_start:
        x_start = y_dim[3]
    if y_dim[3] + y_dim[4] > x_end:
        x_end = y_dim[3] + y_dim[4]
    if y_dim[0] == 0:
        y_dim[0] = index + 1
        for y_dim_next in stave_coords[index+1:]:
            if y_dim[1] <= y_dim_next[1] <= y_dim[1] + y_dim[2]:
                y_dim_next[0] = index + 1
        index += 1

print(stave_coords)

final_stave_coords = []

index = 1

for dim in stave_coords:
    if dim[0] == index:
        final_stave_coords.append([
            dim[1],
            dim[1]+dim[2],
            dim[3],
            dim[3]+dim[4]
        ])
        for dim_next in stave_coords[index:]:
            if dim_next[0] == index:
                final_stave_coords[index-1][1] = dim_next[1] + dim_next[2]
                if dim_next[3] < dim[3]:
                    final_stave_coords[index-1][2] = dim_next[3]
                if dim_next[3] + dim_next[4] > dim[3] + dim[4]:
                    final_stave_coords[index-1][3] = dim_next[3] + dim_next[4]
        index += 1

print(final_stave_coords)

for index, stave_coord in enumerate(final_stave_coords):
    cv2.imwrite(f'./stave_boxes/{ manu }_{ file }_stave_{ index }_bb.png',
        img[
            stave_coord[0]-60:stave_coord[1]+60,
            x_start-30:x_end+30
        ])
    cv2.imwrite(f'./stave_boxes_lines/{ manu }_{ file }_stave_lines_{ index }_bb.png',
        img_line[
            stave_coord[0]-60:stave_coord[1]+60,
            x_start-30:x_end+30
        ])
    cv2.imwrite(f'./stave_boxes_glyphs/{ manu }_s{ file }_stave_glyphs_{ index }_bb.png',
        img_glyphs[
            stave_coord[0]-60:stave_coord[1]+60,
            x_start-30:x_end+30
        ])

# uly_temp = 0
# index = 0
#
# for staff in staff_root.findall('staves'):
#     uly = int(staff.find('bounding_box').find('uly').text)
#     ulx = int(staff.find('bounding_box').find('ulx').text)
#     ncols = int(staff.find('bounding_box').find('ncols').text)
#     nrows = int(staff.find('bounding_box').find('nrows').text)
#
#     print(uly, ulx)
#
#     # if abs(uly - uly_temp) > 200:
#     cv2.imwrite(f'./staff_boxes/staff_{ index }_bb.png',
#         img[uly:uly+nrows, ulx:ulx+ncols])
#     index += 1




#
#     uly_temp = uly

# x_len = 0
# y_len = 0
#
# for stave_index, stave in enumerate(staff_root.findall('staves')):
#     print(stave_index)
#     for stave_next in staff_root.findall('staves')[stave_index+1:]:
#         if int(stave_next.find('bounding_box').find('ulx').text) > int(stave.find('bounding_box').find('ulx').text):
#             print('yeet!')
#         else:
#             break
