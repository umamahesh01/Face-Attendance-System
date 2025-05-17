import cv2
import face_recognition
import numpy as np
import datetime
from supabase_client import supabase
import cvzone

# Load known users
res = supabase.table('users').select('*').execute()
known_data = res.data
known_encodings = [np.array(user['embedding']) for user in known_data]
known_names = [user['name'] for user in known_data]
user_ids = [user['id'] for user in known_data]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    small_img = cv2.resize(img, (640, 480))
    rgb_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    faceLocs = face_recognition.face_locations(rgb_img)
    encodings = face_recognition.face_encodings(rgb_img, faceLocs)

    for encoding, faceLoc in zip(encodings, faceLocs):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_match = np.argmin(distances)

        if matches[best_match]:
            name = known_names[best_match]
            user_id = user_ids[best_match]

            y1, x2, y2, x1 = faceLoc
            bbox = x1, y1, x2 - x1, y2 - y1
            cvzone.cornerRect(img, bbox)

            cv2.putText(img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Log to Supabase
            supabase.table('attendance').insert({
                "user_id": user_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "image_path": known_data[best_match]['image_path']
            }).execute()

    cv2.imshow("Face Attendance", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
