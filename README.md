# Face-Attendance-System

An AI-powered project that automates attendance using **Face Recognition technology**.  
It captures faces from a live webcam feed, matches them with known images, and records attendance with timestamps.  
Built using **OpenCV** and **face_recognition**, this system ensures accurate, real-time attendance tracking.


## 🚀 Project Highlights

- Detects and recognizes faces from a live webcam feed
- Matches with stored images to mark attendance
- Records attendance with **name**, **date**, and **time** in a CSV file
- Simple and fast interface using **OpenCV**


## 🛠️ Tech Stack

- **Python**
- **OpenCV** – for image capturing and display
- **face_recognition** – for face detection and encoding
- **NumPy**, **Datetime**, **CSV** – for backend logic and logging
- **Supabase** - to Store the detected face

## 📂 How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/umamahesh01/Face-Attendance-System.git

2. Add images of known individuals inside the Images folder.
File name should be the person's name (e.g., Mahesh.jpg → "Mahesh").

3. Run the script:
   ```bash
   python main.py
   
4. The webcam will open and recognize faces in real-time.
Attendance will be recorded in the Attendance.csv file.

