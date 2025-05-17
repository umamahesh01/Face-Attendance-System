import os
import cv2
import face_recognition
import pickle
import json
from supabase_client import supabase

imgpath = 'images'
imgdir = os.listdir(imgpath)
imgs = []
names = []

for file in imgdir:
    img = cv2.imread(os.path.join(imgpath, file))
    imgs.append(img)
    names.append(os.path.splitext(file)[0])

def get_encodings(imgList):
    encodingList = []
    for img in imgList:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(rgb)[0]
        encodingList.append(encode.tolist())
    return encodingList

encodingList = get_encodings(imgs)

# Upload to Supabase
for name, encode in zip(names, encodingList):
    # Upload image to storage
    image_path = f"{name}.jpg"
    with open(os.path.join(imgpath, image_path), 'rb') as file:
        supabase.storage.from_('face-images').upload(f'faces/{image_path}', file)

    # Save to users table
    supabase.table('users').insert({
        "name": name,
        "image_path": f'faces/{image_path}',
        "embedding": encode
    }).execute()
