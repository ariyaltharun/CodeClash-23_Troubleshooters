import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import os
from datetime import datetime
import smtplib
import csv


def start_capture():
    face_encodings = []
    known_face_names = []
    attendanceList = []

    d = {"Prathik": "1ms21ai043", "Nivedith": "1ms21ai024", "YASH": "1ms21ai032", "Allu Arjun":"123424523"}

    face1 = "./Assets/face_recognition"

    def makeAttendanceEntry(name):
        with open("./RegisterAttendence/attendance1.csv", 'r+') as FILE:
            allLines = FILE.readlines()

            for line in allLines:
                entry = line.split(',')
                attendanceList.append(entry[0])
            if name not in attendanceList:

                now = datetime.now()
                dtString = now.strftime('%d/%b/%Y, %H:%M:%S')
                FILE.writelines(f'\n{name},{dtString}')

    def send_mail():
        body = ""
        filename = "./RegisterAttendence/attendance1.csv"
        column_index = 0

        column_data = []

        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > column_index:
                    column_data.append(row[column_index])


        for x in column_data:
            try:
                body = body+d[x]+"\n"
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
        server.sendmail(sender, 'yaswanthyeshu50@gmail.com', message)
        server.quit()

    for file in os.listdir(face1):
        if not file.startswith('.'):
            file_path = os.path.join(
                "./Assets/face_recognition", file)
            known_face_names.append(file.split('.')[0])

    vid = cv2.VideoCapture(0)
    for i in range(55):
        ret, img = vid.read()
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
    unknown_image_to_draw = img
    # img=cv2.imread(r"C:\Users\prath\Downloads\CODING\PROJECT\MAIN\Unknown images\images (13) (1).jpeg")

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    pil_image = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_image)

    loaded_face_encodings = np.load('known_face_encodings.npy')
    name = "unknown"
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)

        matches = face_recognition.compare_faces(
            loaded_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(
            loaded_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)

        if best_match_index >= 0 and best_match_index < len(known_face_names):
            name = known_face_names[best_match_index]
        else:
            name = "Unknown"

    if name != "unknown":
        print("Matched name:", name)

    # Draw a box around the face using the Pillow module
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 255))
        cv2.putText(img, name, (left, top-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        makeAttendanceEntry(name)
        cv2.imshow("detected", img)

    send_mail()
