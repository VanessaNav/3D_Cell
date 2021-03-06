import cv2

# Package to crop images, generate masks and get particles points

def cropImageBorders(filename): #to crop the image black borders
    # read  image
    img = cv2.imread(filename)

    # threshold image
    ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 15, 255, cv2.THRESH_BINARY)
    # find contours and get the external one
    image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # with each contour, get its area and find the bigger one
    aux_area = 0
    for c in contours:
        # get the bounding rect
        contour_area = cv2.contourArea(c)
        if contour_area > aux_area:
            aux_area = contour_area
            x, y, w, h = cv2.boundingRect(c)

    # apply the crop to the bigger area
    crop = img[y:y + h, x:x + w]
    cv2.imwrite(filename, crop)