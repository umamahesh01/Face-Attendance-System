import pickle
import cv2
import os
import face_recognition
import numpy as np
import cvzone
from Data_to_Database import insert_attendance, get_person_name_by_id
import datetime

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

folderpath = 'Resources/Modes'
imgdir = os.listdir(folderpath)
imgModeList = [cv2.imread(os.path.join(folderpath, i)) for i in imgdir]

file = open('encoderFile.p', 'rb')
encodingListknownwithids = pickle.load(file)
file.close()

encodingListknown, stdIds = encodingListknownwithids

while True:
    success, img = cap.read()
    imgs = cv2.resize(img, (640, 480))

    FaceCurrFrame = face_recognition.face_locations(imgs)    # getting location of the face
    encodeCurrFrame = face_recognition.face_encodings(imgs, FaceCurrFrame)    # encoding the face(which is going to detect by camera, so it helps for face detection

    imgBackground[162:162 + 480, 55:55 + 640] = imgs   # putting our face in that specific box
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[0]

    for encodeFace, faceLoc in zip(encodeCurrFrame, FaceCurrFrame):
        matches = face_recognition.compare_faces(encodingListknown, encodeFace)  # compares the conding of encodingListknown(already encodes of stored face) to encodeFace (which is face that is captured by camera)
        faceDis = face_recognition.face_distance(encodingListknown, encodeFace)

        matchId = np.argmin(faceDis)
        print('match_id', matchId)
        if matches[matchId]:
            print('Matched')
            y1, x2, y2, x1 = faceLoc
            bbox = 52 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            detected_id = stdIds[matchId]  # it gives id based on the
            person_name = get_person_name_by_id(detected_id)

            if person_name:
                print(f"Detected name: {person_name}")
                result = insert_attendance(int(detected_id))
                if result == "inserted":
                    print(f"Attendance marked for {person_name}")
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[2]  # Marked
                elif result == "already_marked":
                    print(f"Attendance already marked today for {person_name}")
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]  # Already marked

            else:
                print(f"No matching person name found in database for ID: {detected_id}")

    cv2.imshow('Background', imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
