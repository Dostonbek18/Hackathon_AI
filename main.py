import keyword
import pyautogui as pag
import cv2
from cvzone.HandTrackingModule import HandDetector

# variables
lengthBetweenHands = ['s']*10

# function

def Actions(str):
    if str == 'Switch off':
        pag.press('down')
    elif str == 'Switch on':
        pag.press('up')


def channgeList(station, element):
    if station == 1:
        lengthBetweenHands.pop(0)
        lengthBetweenHands.append(element)


cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, maxHands=2)
lnz = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        # length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            fingers2 = detector.fingersUp(hand2)
            # print(fingers1, fingers2)
            # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

            channgeList(1, length)
            print(lengthBetweenHands[0])
            if lengthBetweenHands[0] != 's':
                if lengthBetweenHands[0] > lengthBetweenHands[9]+80:
                    Actions('Switch off')
                elif lengthBetweenHands[0] < lengthBetweenHands[9]-100:
                    Actions('Switch on')
            lnz = length
    img = cv2.resize(img, (1200, 900))
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyWindowsAll()
