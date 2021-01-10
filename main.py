import os
from datetime import datetime
from time import sleep

import face_recognition
import cv2
import numpy as np
import wave

import speech_recognition as sr
import pyaudio

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
from gtts import gTTS

from Person import Person
from voiceRecognition.BasicVoiceRecognition import record_responce


while True:

    display=True
    is_already_recognized={}
    video_capture = cv2.VideoCapture(0)
    need_of_reset=False

    persons={}

    #adding faces
    known_face_encodings = [
     #   biden_face_encoding
    ]
    known_face_names = [

    ]
    for name in os.listdir(r"C:\Users\macie\PycharmProjects\faceRecognition\photos\known"):
        #is_already_recognized[name.split(".")[0]]=False




    # Load a sample picture and learn how to recognize it.
        temp_image = face_recognition.load_image_file(f"photos/known/{name}")
        temp_face_encoding = face_recognition.face_encodings(temp_image)[0]

        known_face_encodings.append(temp_face_encoding)
        known_face_names.append(name.split(".")[0])

        persons[name.split(".")[0]]=Person(name)

    # victoria_image = face_recognition.load_image_file("photos/known/Victoria.jpg")
    # victoria_face_encoding = face_recognition.face_encodings(victoria_image)[0]

    # # Load a second sample picture and learn how to recognize it.
    # biden_image = face_recognition.load_image_file("biden.jpg")
    # biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    unknown_faces=[0,datetime.now().strftime("%d%m%Y%H%M")]


    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:

                    name = known_face_names[best_match_index]

                    #if not is_already_recognized[name]:

                    if not persons[name].is_active:
                        is_already_recognized[name]=True
                        print(f'hello {name}')
                        #saying hello
                        text=f"Hello {name}"

                        #add check if there is already recording
                        if not f"welcome{name}.mp3" in  os.listdir(r"C:\Users\macie\PycharmProjects\faceRecognition\photos\known"):
                            myobj = gTTS(text=text, lang="pl", slow=False)
                            myobj.save(f"audiofiles/welcome{name}.mp3")



                        os.system(f'start audiofiles/"welcome{name}.mp3"')

                        persons[name].start()

                    else:
                        persons[name].refresh()
                else:
                    img_name = f"photos/unknown/unknown{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.jpg"
                    cv2.imwrite(img_name, frame)

    #                is_already_recognized[f"unknown{datetime.now().strftime('%d%m%Y')}"]=False
                    # unknown_image = face_recognition.load_image_file(img_name)
                    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                    # known_face_encodings.append(unknown_face_encoding)
                    #
                    print("Unknown person - {} written!".format(img_name))
                    if datetime.now().strftime("%d%m%Y%H%M") == unknown_faces[1]:
                        unknown_faces[0]+=1
                        if unknown_faces[0]>10:
                            print("Let's identify that dude!")
                            os.system(f"start audiofiles/unknownask.mp3")

                            #
                            # def record_responce():
                            #     r = sr.Recognizer()
                            #     CHUNK = 1024
                            #     WIDTH = 2
                            #     CHANNELS = 2
                            #     RATE = 44100
                            #     RECORD_SECONDS = 5
                            #     FORMAT = pyaudio.paInt16
                            #
                            #     p = pyaudio.PyAudio()
                            #
                            #     stream = p.open(format=p.get_format_from_width(WIDTH),
                            #                     channels=CHANNELS,
                            #                     rate=RATE,
                            #                     input=True,
                            #                     output=True,
                            #                     frames_per_buffer=CHUNK)
                            #     print("here")
                            #     print(f"* recording {datetime.now()}")
                            #     chunks = []
                            #     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                            #         data = stream.read(CHUNK)  # read audio stream
                            #         chunks.append(data)
                            #         # stream.write(data, CHUNK)  #play back audio stream
                            #
                            #     print(f"* done {datetime.now()}")
                            #     wf = wave.open("undentified.wav", 'wb')
                            #     wf.setnchannels(CHANNELS)
                            #     wf.setsampwidth(p.get_sample_size(FORMAT))
                            #     wf.setframerate(RATE)
                            #     wf.writeframes(b''.join(chunks))
                            #     wf.close()
                            #
                            #     stream.stop_stream()
                            #     stream.close()
                            #
                            #     p.terminate()
                            #     with sr.AudioFile('undentified.wav') as source:
                            #         audio = r.record(source)
                            #
                            #     return r.recognize_google(audio)
                            #
                            while(True):
                                sleep(6)
                                newname = record_responce()

                                os.system(f"start audiofiles/dziekuje.mp3")
                                # myobj = gTTS(text=f"Dziękuję", lang="pl", slow=False)
                                # myobj.save(f"audiofiles/dziekuje.mp3")
                                if newname in is_already_recognized.keys():
                                    os.system(f"start audiofiles/notuniquename.mp3")
                                    continue
                                else:
                                    cv2.imwrite(f"photos/known/{newname}.jpg", frame)
                                    need_of_reset = True
                                    break






                    else:
                        unknown_faces[0]=0
                        unknown_faces[1]=datetime.now().strftime("%d%m%Y%H%M")





                face_names.append(name)

            #restoring falses to the list
            for check_name in [x for x in list(is_already_recognized.keys())]:
                if check_name not in face_names:
                    is_already_recognized[check_name]=False
            #print(face_names)

        process_this_frame = not process_this_frame

        if display:
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            if need_of_reset:
                break
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()