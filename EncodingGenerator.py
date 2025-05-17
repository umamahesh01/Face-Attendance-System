import cv2
import pickle as pkl
import os
import face_recognition

imgpath = 'images'
imgdir = os.listdir(imgpath)
imgs = []
stdIds = []

for i in imgdir:
    img = cv2.imread(os.path.join(imgpath, i))
    imgs.append(img)
    stdIds.append(os.path.splitext(i)[0])

print(len(imgs))
print(imgs[0])

def findEncodings(imgList) :

    encodeList = []
    for i in imgList :
        img = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodingListknown = findEncodings(imgs)
encodingListknownwithids = [encodingListknown, stdIds]
print(encodingListknownwithids)
print(len(encodingListknownwithids))

file = open('encoderFile.p', 'wb')
pkl.dump(encodingListknownwithids, file)
file.close()









