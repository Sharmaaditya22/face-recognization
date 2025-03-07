import numpy as np
import cv2
import pickle
face_cascade=cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade=cv2.CascadeClassifier('cascades/data/haarcascade_eye_tree_eyeglasses.xml')

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels={"person_name": 1}
with open("label.pickle",'rb') as f:#for see name
    og_labels=pickle.load(f)
    labels={v:k for k,v in og_labels.items()}#reverse the labels v:k is key value pair

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)#capture face and only access in gray
    for (x,y,w,h) in faces:
       # print(x,y,w,h)
        roi_gray=gray[y:y+h, x:x+w]# coordinates of image
        roi_color=frame[y:y+h, x:x+w]

        #recognizer? deep learned model predict keras tensorflow
        id_,conf=recognizer.predict(roi_gray)# predict region of interest
       # if conf >= 45 :# and conf <= 85:# config various lot so use this if condition issue :- this one is not accurate so use deep learn model
        print(id_)
        print(labels[id_])
        font=cv2.FONT_HERSHEY_SIMPLEX
        name=labels[id_]
        color=(255,255,255)
        stroke=2
        cv2.putText(frame,name,(x+w,y+h), font, 1, color , stroke, cv2.LINE_AA)
        img_item="7.png"
        cv2.imwrite(img_item,roi_color)#write image

        color=(255,0,0)# in BGR
        stroke=2# width of rectangle
        end_cord_x=x+w
        end_cord_y=y+h
        cv2.rectangle(frame, (x,y), (end_cord_x,end_cord_y),color,stroke)
        eyes=eye_cascade.detectMultiScale(roi_gray)# for detect eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)



    # Display the resulting frame
    cv2.imshow('frame', frame)
    #cv2.imshow('gray', gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
yAllWindow()