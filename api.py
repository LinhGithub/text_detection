import face_recognition
from PIL import Image, ImageTk
import os
import cv2 as cv
import time

from numpy import inexact
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'D:\tesseract\tesseract.exe'

BASE_DIR = os.getcwd()
dir_path = os.path.join(BASE_DIR, 'test_image')

basedir = os.path.abspath(os.path.dirname(__file__))

def crop_image(dir_image):
    image = face_recognition.load_image_file(dir_image)
    # face_locations = face_recognition.face_locations(image)
    face_locations = []
    # img = Image.open(dir_image)
    img = cv.imread(dir_image)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # hImg,wImg,_ = img.shape
    text = tess.image_to_data(img)
    for x, b in enumerate(text.splitlines()):
        if x!=0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                # x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                left, top, right, bottom = int(b[6]), int(b[7]), int(b[8]), int(b[9])

                # cv.rectangle(img, (x,y), (w+x,h+y), (0,0,225), 3)
                # mytuple = (x,hImg-y,w,hImg-h)
                mytuple = (top, right+left, bottom+top, left)

                face_locations.append(mytuple)
    # cv.imshow('Result', img)
    # cv.waitKey(0)

    path_folder = basedir+'/image_detection'
    if not os.path.exists(path_folder):
            os.mkdir(path_folder)

    index = 0
    lst_image_detection = []
    for face_location in face_locations:
        # in tung anh và vi tri
        top, right, bottom, left = face_location
        
        # luu anh
        name_image = ''
        location_1 = 0
        try:
            location_1 = dir_image.rindex("\\")+1
            name_image = dir_image[location_1:]
            location_2 = name_image.rindex('.')
            name_image = name_image[:location_2]
        except:
            location_1 = dir_image.rindex("/")+1
            name_image = dir_image[location_1:]
            location_2 = name_image.rindex('.')
            name_image = name_image[:location_2]
        face_image = image[top:bottom, left:right]
        name_image_detection = '{}{}{}.png'.format('D:/Baitapcacmon/Laptrinhhethong/text_detection/image_detection/',name_image+'_pic', index)
        dict_info = {}
        dict_info['file_path'] = name_image_detection
        dict_info['note'] = 'Ảnh khuôn mặt thứ ' + str(index+1) + ' cắt từ ' + dir_image[location_1:]
        lst_image_detection.append(dict_info)
        Image.fromarray(face_image).save('{}{}{}.png'.format('D:/Baitapcacmon/Laptrinhhethong/text_detection/image_detection/',name_image+'_pic', index))
        index+=1
        
    return lst_image_detection


def read_file_from_folder(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        img_path = os.path.join(dir_path, file)
        image = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        cv.imshow('image', image)
        cv.waitKey(3000)
    cv.destroyAllWindows()
    return True


def get_list_file_path_from_folder(dir_path):
    files = os.listdir(dir_path)
    list_file_path = []
    for file in files:
        img_path = os.path.join(dir_path, file)
        list_file_path.append(img_path)
    return list_file_path

# read_file_from_folder(dir_path)
# list_file_path = get_list_file_path_from_folder(dir_path)
# for file_path in list_file_path:
#     crop_image(file_path)
