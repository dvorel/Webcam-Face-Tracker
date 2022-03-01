import cv2
import numpy as np
import serial
import time

#arduino shit
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    #time.sleep(0.05)
    #data = arduino.readline()
    #return data

def face_location(x1, y1, x2, y2, px, py, of=50):

    mx =  (x1+x2)/2
    my = (y1+y2)/2
    px /= 2
    py /= 2
    move = ""
    print(mx, px, my, py)

    if px>mx and (px-mx)>of:
        move += "R"
    elif px<mx and (mx-px)>of:
        move += "L"

    if py>my and (py-my)>of:
        move += "U"
    elif py<my and (my-py)>of:
        move += "D"

    print("move: ", move)
    write_read(move)
    


#import imutils

# TODO: definirajte putanje do modela
prototxt_path = 'ferit/face_detection/models/deploy.prototxt'
caffemodel_path = 'ferit/face_detection/models/trained.caffemodel'

# ucitaj mrezu
print("Ucitavanje SDD detektora...")
net = cv2.dnn.readNet(caffemodel_path, prototxt_path)

# ucitavanje slike
#image = cv2.imread("ferit/face_detection/img/test2.jpg")
vid = cv2.VideoCapture(0)
_, image = vid.read()
(h, w) = image.shape[:2]


# kreiranje bloba
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

# detekcija lica u slici pomocu mreze
net.setInput(blob)
detections = net.forward()

# prag detekcije
confidenceTH = 0.7
max_conf = 0
max_i = 0
count = 0
# TODO: napravite petlju po detekcijama
# ako confidence prelazi prag confidenceTH nacrtajte u izlaznu sliku BB i vjerojatnost
while(True):
    count+=1
    _, image = vid.read()
    
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # detekcija lica u slici pomocu mreze
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        
        confidence = detections[0, 0, i, 2]
        
        if confidence > max_conf:
            max_conf = confidence
            max_i = i

        if confidence < confidenceTH:
            continue
        
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 220, 255), 2)
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 1)


    #track highest confidence face
    if count %2 and max_conf>0.55:
        (h, w) = image.shape[:2]    
        boxx = detections[0, 0, max_i, 3:7] * np.array([w, h, w, h])     #first face
        (x1, y1, x2, y2) = boxx.astype("int")
        face_location(x1, y1, x2, y2, w, h)

    # show the output image with the face detections + facial landmarks
    cv2.imshow("Output", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("done")
