# import libs
import cv2
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from skimage import io, img_as_ubyte
from scipy import ndimage
import numpy as np
import imutils
import matplotlib.pyplot as plt


def watershed_segmentation(image_path, min_distance):

    """
    This function performs watershed segmentation on an input image.
    Parameters:
    image_path: str, path to the input image
    min_distance: int, minimum distance between peaks
    Function Steps:
    Reads and processes the image (grayscale conversion if needed).
    Applies Otsu's thresholding and computes the distance transform.
    Identifies peaks and creates markers for segmentation.
    Applies the watershed algorithm to segment the image.
    Draws contours and labels each segmented region.
    Displays the segmented result using matplotlib.
    Requires OpenCV, NumPy, SciPy, scikit-image, imutils, and matplotlib.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    # Check if the image is grayscale or color
    if len(img.shape) == 2:
        # If grayscale, skip mean shift filtering
        gray = img
    else:
        # If color, apply mean shift filtering and convert to grayscale
        shifted = cv2.pyrMeanShiftFiltering(img, 21, 51)
        gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    
    # Ensure the image is 8-bit
    gray = img_as_ubyte(gray)
    
    # Apply thresholding
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Compute the distance transform
    D = ndimage.distance_transform_edt(thresh)
    
    # Find peaks in the distance map
    localMax = peak_local_max(D, min_distance=min_distance, labels=thresh)
    
    # Create a binary mask for the local maxima
    localMaxMask = np.zeros(D.shape, dtype=bool)
    localMaxMask[tuple(localMax.T)] = True
    
    # Perform connected component analysis
    markers = ndimage.label(localMaxMask, structure=np.ones((3, 3)))[0]
    
    # Apply the Watershed algorithm
    labels = watershed(-D, markers, mask=thresh)
    
    # Prepare the output image
    output = img.copy() if len(img.shape) == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    # Loop over unique labels
    for label in np.unique(labels):
        if label == 0:
            continue
        
        # Create a mask for the current label
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[labels == label] = 255
        
        # Find contours
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        
        # Draw contour and label
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.putText(output, f"#{label}", (int(x) - 10, int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.drawContours(output, [c], -1, (0, 255, 0), 2)
    
    # Display the result
    plt.figure(figsize=(12, 12))
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title('Watershed Segmentation Result')
    plt.axis('off')
    plt.show()



# function of kmeans
