import cv2
import sys
import matplotlib.pyplot as plt

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                     'haarcascade_frontalface_default.xml')

# Load image
img = cv2.imread('testAI.jpg', 1)

if img is None:
    sys.exit("Could not read the image.")
    
# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect the faces
faces = face_cascade.detectMultiScale(img_gray, 1.2, 4)

# Draw the rectangle around each face
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
# Display
# cv2.imshow('img', img)
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax.set_title('Recognized AI generated faces')
ax.axis('off')
fig.set_tight_layout(True)

cv2.imshow('img', img)
cv2.waitKey(0)
