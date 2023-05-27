import streamlit as st
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
from datetime import datetime
import smtplib
import csv
import os

d={"Prathik":"1ms21ai043","Nivedith":"1ms21ai024","YASH":"1ms21ai032"}#dictionary containing details of the student

#FUNCTION MARKING THE ATTENDANCE
def makeAttendanceEntry(name):
    with open(r"C:\Users\prath\Downloads\CODING\PROJECT\face_recognition\attendance1.csv", 'r+') as FILE:
        allLines = FILE.readlines()

        attendanceList = [entry.split(',')[0] for entry in allLines]
        if name not in attendanceList:
            now = datetime.now()
            dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
            FILE.writelines(f'\n{name},{dtString}')

#CODE FOR SENDING MAIL
def send_mail():
    body = r"C:\Users\prath\Downloads\CODING\PROJECT\face_recognition\attendance1.csv"
    filename = r"C:\Users\prath\Downloads\CODING\PROJECT\face_recognition\attendance1.csv"
    column_index = 0

    column_data = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > column_index:
                column_data.append(row[column_index])

    for x in column_data:
        try:
            body = body + d[x] + "\n"
        except KeyError:
            print("Key Error")
            pass

    sender = "pavancs325@gmail.com"
    login = "ndpyfheoexnpxusy"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, login)
    subject = 'attendance'
    message = "subject:{}\n\n{}".format(subject, body)
    server.sendmail(sender, 'prathik3110@gmail.com', message)
    server.quit()

#FOR CREATING THE KNOWN FACES LIST,AND ACCES WEBCAM TAKE THE IMG OF THE USER
def start_capture():
    face_encodings = []
    known_face_names = []
    attendanceList = []

    d = {"Prathik": "1ms21ai043", "Nivedith": "1ms21ai024", "YASH": "1ms21ai032", "Allu Arjun": "123424523"}

    face1 = r"C:\Users\prath\Downloads\CODING\PROJECT\MAIN\face_recognition"

    for file in os.listdir(face1):
        if not file.startswith('.'):
            file_path = os.path.join("./Assets/face_recognition", file)
            known_face_names.append(file.split('.')[0])

    vid = cv2.VideoCapture(0)
    ret, img = vid.read()
    vid.release()

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    pil_image = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_image)

    #loading the encodings of the known faces using .npy file
    loaded_face_encodings = np.load('face_encodings.npy')
    global name 
    name="unknown"

    #code for getting the name of the person recognised
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(loaded_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(loaded_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if best_match_index >= 0 and best_match_index < len(known_face_names):
            name = known_face_names[best_match_index]
        else:
            name = "Unknown"

    if name != "unknown":
        print("Matched name:", name)

    #function call for attendance entry
    makeAttendanceEntry(name)
    send_mail()
      

# Define CSS style for the page
    page_style = """
        <style>
            body {
                background-color: yellow;
                color: #333333;
                font-family: Arial, sans-serif;
                padding: 20px;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
            }

            .box {
                border: 1px solid #ccc;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 5px;
            }

            h1 {
                color: #0072B2;
                margin-bottom: 30px;
            }

            p {
                margin-bottom: 10px;
            }

            .unknown-image {
                color: red;
                font-weight: bold;
            }
        </style>
    """

# Apply the page style
    st.markdown(page_style, unsafe_allow_html=True)

    

    # Create a container for the content
    container = st.container()

    # Display the line captured image 
    with container:
        
        st.markdown(f'<p style="color: yellow;">Captured Image: {name}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<p style="color: red;">IF CAPTURED IMAGE IS SHOWING UNKNOWN ,PLEASE CLICK THE CAPTURE BUTTON AGAIN</p>', unsafe_allow_html=True)




def main():
    st.title("Face Recognition Based Attendance System")

    if st.button("Capture"):
        start_capture()
    

if __name__ == "__main__":
    main()
