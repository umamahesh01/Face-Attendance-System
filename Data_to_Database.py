from supabase import create_client, Client
import datetime
import os
import cv2


# === CONFIG ===
SUPABASE_URL = "https://crfsyqgtifoilanqrjqr.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNyZnN5cWd0aWZvaWxhbnFyanFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcxMjA5MTUsImV4cCI6MjA2MjY5NjkxNX0.utQFmL7XJUCg2nLOuboNgFSm-Cm9EGrTFt5VTBcZzoE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

folderpath = 'Resources/Modes'
imgdir = os.listdir(folderpath)
imgModeList = [cv2.imread(os.path.join(folderpath, i)) for i in imgdir]

def insert_attendance(person_id: int):
    now = now = datetime.datetime.now().replace(microsecond=0).isoformat()
    today = datetime.datetime.now().date().isoformat()

    # Check if already marked today
    existing = supabase.table("attendance") \
        .select("id") \
        .eq("id", person_id) \
        .gte("time", today) \
        .execute()

    if existing.data:
        print(f"Already marked today for ID {person_id}")
        return 'already_marked'

    # Get student name
    name = get_person_name_by_id(person_id)
    if not name:
        print(f"No name found for ID {person_id}. Skipping attendance.")


    # Prepare row
    data = {
        "id": person_id,
        "Student_Name": name,  # Be sure to match exact case
        "time": now,
    }

    # Insert into Supabase
    response = supabase.table("attendance").insert(data).execute()
    print("Attendance inserted:", response)
    return 'inserted'

def get_person_name_by_id(person_id: int):
    try:
        response = supabase.table("FirstOne") \
            .select("name") \
            .eq("id", person_id) \
            .execute()

        print("Supabase response:", response)

        if response.data and len(response.data) > 0:
            return response.data[0].get("name")   # name is column name in FirstOneTable
        else:
            return None

    except Exception as e:
        print(f"Error getting person name by id: {e}")
        return None


