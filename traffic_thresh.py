import cv2
import numpy as np

WIDTH = 800
HEIGHT = 600

def holder(x):
    pass

cv2.namedWindow("Color Thresholds", cv2.WINDOW_NORMAL)

cv2.createTrackbar("min_blue", "Color Thresholds", 0, 255, holder)
cv2.createTrackbar("min_green", "Color Thresholds", 0, 255, holder)
cv2.createTrackbar("min_red", "Color Thresholds", 0, 255, holder)

cv2.createTrackbar("max_blue", "Color Thresholds", 0, 255, holder)
cv2.createTrackbar("max_green", "Color Thresholds", 0, 255, holder)
cv2.createTrackbar("max_red", "Color Thresholds", 0, 255, holder)

source = "/Users/felipepesantez/Movies/inference/top_traffic2.mp4"
cap = cv2.VideoCapture(source)

while cap.isOpened():
    sucess, imageBGR = cap.read()
    imageBGR = cv2.resize(imageBGR, (WIDTH, HEIGHT))

    imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV",imageHSV)

    #mask
    min_blue = cv2.getTrackbarPos("min_blue","Color Thresholds")
    min_green = cv2.getTrackbarPos("min_green","Color Thresholds")
    min_red = cv2.getTrackbarPos("min_red","Color Thresholds")

    max_blue = cv2.getTrackbarPos("max_blue","Color Thresholds")
    max_green = cv2.getTrackbarPos("max_green","Color Thresholds")
    max_red = cv2.getTrackbarPos("max_red","Color Thresholds")

    mask = cv2.inRange(imageHSV, 
                        (min_blue, min_green, min_red),
                        (max_blue, max_green, max_red),
                       )

    cv2.imshow("Binary mask", mask)

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        #possible loop of instances
        #for i in range(len(contours)):
        seg_contours = contours[:12]
        for i in seg_contours:
            (x_min, y_min, box_width, box_height) = cv2.boundingRect(i)
            cv2.rectangle(imageBGR, (x_min -15, y_min - 15),
                        (x_min + box_width +15, y_min + box_height + 15),
                          (0,255,0),3
                          )
            label = "Detected Object"
            cv2.putText(imageBGR, label, (x_min -5, y_min - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0),2)

    cv2.imshow("Original",imageBGR)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
