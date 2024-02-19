import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import os

# def find_license_plate_contour(contours):
#     results = []
#     for contour in contours:
#         perimeter = cv2.arcLength(contour, True)
#         approx_vector = [cv2.approxPolyDP(contour, param * perimeter, True) for param in np.arange(0.01, 1.1, 0.01)]
#         for approx in approx_vector:
#             if len(approx) == 4:  # Check for quadrilateral
#                 (x, y, w, h) = cv2.boundingRect(approx)
#                 aspect_ratio = w / float(h)
#                 if 2 <= aspect_ratio <= 5:  # Typical aspect ratio for license plates
#                     results.append(approx)
#     return results

if __name__ == "__main__":

    # import car images
    images = [img for img in os.listdir(os.path.curdir) if img.endswith(".jpg") and "car" in img]
    images.sort()

    for img_name in images:
        
        # 
        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620,480) )
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
        # cv2.imshow('gray',gray)
        # cv2.waitKey(0)
        gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
        # cv2.imshow('gray',gray)
        # cv2.waitKey(0)
        edged = cv2.Canny(gray, 20, 200) #Perform Edge detection

        cv2.imshow('edged',edged)
        cv2.waitKey(0)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        # screenCnt = find_license_plate_contour(cnts)

        # loop over our contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)
            # print(c, peri)
        
            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        # if len(screenCnt):
        #     print(len(screenCnt))
        #     for a in screenCnt:
        #         edited = cv2.drawContours(img, [a], -1, (0, 255, 0), 3)
        #         cv2.imshow('edged',edited)
        #         cv2.waitKey(0)

        if screenCnt is None:
            detected = 0
            print ("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        # Masking the part other than the number plate
        try:
            mask = np.zeros(gray.shape,np.uint8)
            new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
            new_image = cv2.bitwise_and(img,img,mask=mask)

            # Now crop
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx+1, topy:bottomy+1]

            cv2.imshow('image',img)
            cv2.imshow('Cropped',Cropped)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except:
            print("Some error occurred, sorry")
