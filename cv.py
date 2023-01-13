#code reference 
# from https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
#from https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
#from https://pythonprogramming.net/color-filter-python-opencv-tutorial/
###########################
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX
    return bar



cap = cv2.VideoCapture(0)
clt = KMeans(n_clusters=3) #cluster number
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
while True:
    _, imgOriginal = cap.read()
    croppedImg = imgOriginal[len(imgOriginal)//2 - 20 : len(imgOriginal)//2 + 20, len(imgOriginal[1])//2 -20 : len(imgOriginal[1])//2 + 20]
    img = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2RGB)
    

    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    
    clt.fit(img)
    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)
    normalizedRGB = clt.cluster_centers_.astype('uint8')
    hsvCenters = cv2.cvtColor(np.array([normalizedRGB]), cv2.COLOR_RGB2HSV)
    print("Printing RGB values of the 3 cluster centers:\n", clt.cluster_centers_, "\nPrinting their HSV values:\n", hsvCenters)

    plt.axis("off")
    plt.imshow(bar)
    cv2.imshow('img',imgOriginal)
    cv2.imshow('cropped', croppedImg)
    plt.show()
############################

# import numpy as np
# import cv2


# cap = cv2.VideoCapture(0)

# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])


# while(True):
#     # Capture frame-by-frame
    
#     _, frame = cap.read()

#     transcodedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     thresh = cv2.inRange(transcodedFrame, lower_blue, upper_blue)
#     contours,_ = cv2.findContours(thresh, 1, 2)
    
#     if contours: #

#         cnt = max(contours, key=cv2.contourArea) 
#         rect = cv2.minAreaRect(cnt)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(frame,[box],0,(0,0,255),2) 
#         cv2.drawContours(thresh,[box],0,(255, 255, 255),2) 


#     cv2.imshow('frame',frame)
#     cv2.imshow('rawThreshold',thresh)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cap.release()
# cv2.destroyAllWindows()