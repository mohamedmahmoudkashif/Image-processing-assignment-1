import cv2
import numpy as np


img = cv2.imread("coins.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#kernels used

kernel10 = np.ones((4,3),np.uint8)
kernel4 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))
kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
kernel12 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

#otsuthresholding
ret,thresh1 = cv2.threshold(gray,150,255, cv2.THRESH_OTSU)

#closing operation
img1 = thresh1.copy()
#opening = cv2.morphologyEx(img1, cv2.MORPH_OPEN,kernel1)
closing = cv2.morphologyEx(img1, cv2.MORPH_CLOSE,kernel2,iterations=1)

#filling black noisy in one of the circles
img2 = closing.copy()
im2, contours, hierarchy = cv2.findContours(img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im2,contours,6,(255,255,255),-4)
cv2.drawContours(im2,contours,-1,(255,255,255),-4)

#finding number of all coins
img4 = im2.copy()
im4,contours, hierarchy = cv2.findContours(img4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt1 = contours[0]
(x1,y1),radius1 = cv2.minEnclosingCircle(cnt1)
center1 = (int(x1),int(y1))
radius1 = int(radius1)
cv2.circle(im2,center1,radius1,(0,255,0),2)
x2 = len(contours)
print ('Number of all coins %d' % x2)

#operation function to remove small circled
opening1 = cv2.morphologyEx(im2, cv2.MORPH_OPEN,kernel1)

#finding numbers of large coins
img3=opening1.copy()
im3,contours, hierarchy = cv2.findContours(img3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(opening1,center,radius,(0,255,0),2)
x3 = len(contours)
print ('Number of large coins %d' % x3)
print ('Number of small coins %d' % (x2-x3))
print  ('Amount of all coins %d' % (x3*100 + (x2-x3)*50) + ' cent' )

img5 = img.copy()

img8 = im2.copy()
im6, contours, hierarchy = cv2.findContours(img8,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt2 = contours[0]
(x2,y2),radius2 = cv2.minEnclosingCircle(cnt2)
center2 = (int(x2),int(y2))
radius2 = int(radius2)
img7=cv2.circle(img5,center2,radius2,(250,255,0),2)

#find the image of large coins only
img9=opening1.copy()
dilationb = cv2.dilate(img9,kernel12,iterations=1)
largecoins = dilationb - img9

#find image of small coins only
smallcoins = im2-opening1
opening3 = cv2.morphologyEx(smallcoins, cv2.MORPH_OPEN,kernel4)

#highlight the large coins withred color
img13 = largecoins.copy()
im7 , contours, hierarchy = cv2.findContours(img13,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt3 in im7[0,:]:
 cv2.drawContours(img5,contours,-1,(0,0,255),3)


#Hilighlight the small coins with blue color
img12 = opening3.copy()
im8 , contours, hierarchy = cv2.findContours(img12,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt4 in im8[0,:]:
 cv2.drawContours(img5,contours,-1,(255,0,0),3)



cv2.imshow('After otsu thresholding',thresh1)
cv2.imshow('After closing',closing)
cv2.imshow('After filling',im2)
cv2.imshow('Remove small coins',opening1)
#cv2.imshow('win5',img7)
#cv2.imshow('win6',largecoins)
cv2.imshow('win7',img7)
cv2.imshow('win8',opening3)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('win.png',thresh1)

cv2.imwrite('win3.png',closing)

