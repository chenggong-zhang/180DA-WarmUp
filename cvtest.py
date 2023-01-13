import cv2

im = cv2.imread('/Users/charles_zhang/Desktop/ECE180D/180DA-WarmUp/ID_photo.jpg', cv2.IMREAD_COLOR)
cv2.imshow('what', im)
cv2.waitKey(0)
cv2.destroyAllWindows()