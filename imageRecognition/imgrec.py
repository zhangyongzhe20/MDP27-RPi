import cv2
import numpy as np
import os
# from picamera import PiCamera
# from picamera.array import PiRGBArray
import time

# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF','cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

#REUSABLE FUNCTIONS
def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

def get_key(thisDict,val): 
    for key, value in thisDict.items(): 
        if (type(val) == str):
            if (val == value):
                return key
        elif is_similar(val, value): 
             return key 
  
    return "key doesn't exist"


#INPUT IMAGE
# image = cv2.imread('/home/pi/MDP27-RPi/imageRecognition/mdp_labels/x.jpg')
# print("this is ", os.listdir("/home/nishka/Desktop/ImgRec/mdp_labels/"))


def image_rec():
    imgID = -1
    image = cv2.imread('/home/nishka/Desktop/MDP27-RPi/imageRecognition/mdp_labels/x.jpg')

    # with PiCamera() as camera:
    #     with PiRGBArray(camera) as stream:
    #         # At this point the image is available as stream.array
    #         image = stream.array


    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()


    #READ ALL TEMPLATE IMAGES
    tv = cv2.imread('./mdp_labels/templates/tv.jpg',0)
    tw = cv2.imread('./mdp_labels/templates/tw.jpg',0)
    tx = cv2.imread('./mdp_labels/templates/tx.jpg',0)
    ty =  cv2.imread('./mdp_labels/templates/ty.jpg',0)
    tz = cv2.imread('./mdp_labels/templates/tz.jpg',0)

    t6 = cv2.imread('./mdp_labels/templates/t6.jpg',0)
    t7 = cv2.imread('./mdp_labels/templates/t7.jpg',0)
    t8 = cv2.imread('./mdp_labels/templates/t8.jpg',0)
    t9 = cv2.imread('./mdp_labels/templates/t9.jpg',0)
    t0 = cv2.imread('./mdp_labels/templates/t0.jpg',0)

    tright = cv2.imread('./mdp_labels/templates/tright.jpg',0)
    tleft = cv2.imread('./mdp_labels/templates/tleft.jpg',0)
    tup = cv2.imread('./mdp_labels/templates/tup.jpg',0)
    tdown = cv2.imread('./mdp_labels/templates/tdown.jpg',0)
    tgo = cv2.imread('./mdp_labels/templates/tgo.jpg',0)


    tdict = {
        0 : [tleft, t8, tv],  #red
        1 : [tdown, t6, ty],  #blue
        2 : [tgo, t7, tw],    #green
        3 : [tright, t0, tz], #yellow
        4 : [tup, t9, tx]     #white
    }

    namedict = {
        'up' : tup, 'down' : tdown, 'right' : tright, 'left' : tleft, 'go' : tgo, '6' : t6,
        '7' : t7, '8' : t8, '9' : t9, '0' : t0, 'v' : tv, 'w' : tw, 'x' : tx, 'y' : ty, 'z' : tz
    } 

    iddict = { 1 : 'up',2 : 'down', 3 : 'right', 4 : 'left', 5 : 'go', 6 : '6', 7 : '7', 
        8 : '8', 9 : '9', 10 : '0', 11 : 'v', 12 : 'w', 13 : 'x', 14 : 'y', 15 : 'z'}


    #LOWER AND UPPER HSV BOUNDARIES
    boundaries = [
        [[(0,120,70), (10,255,255)], [(170,120,70), (180,255,255)]], #red
        [[(100,180,80), (110,245,180)], [(100,180,80), (110,245,180)]], #blue
        [[(70,165, 60), (90,220,130)], [(70,165, 60), (90,220,130)]], #green
        [[(20, 130, 150), (30, 190, 190)], [(20, 130, 150), (30, 190, 190)]], #yellow
        [[(0, 0, 90), (15, 40, 190)], [(160, 0, 90), (180, 40, 190)]], #white
    ]

    #COLOUR DETECTION + #THE 3 POSSIBLE TEMPLATES
    hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # cv2.imshow("image", image)
    # # cv2.setMouseCallback("imageWindow1",onMouse, 0)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() 

    templateList = []
    index = 0

    # loop over the colours
    for curColour in boundaries:
        # create NumPy arrays for LOWER boundaries
        lowerl = np.array(curColour[0][0], dtype = "uint8")
        upperl= np.array(curColour[0][1], dtype = "uint8")
        # find the colors within the specified boundaries and apply the mask
        maskl = cv2.inRange(hsvImg, lowerl, upperl)

        # do the same for UPPER boundaries
        loweru = np.array(curColour[1][0], dtype = "uint8")
        upperu= np.array(curColour[1][1], dtype = "uint8")
        masku = cv2.inRange(hsvImg, loweru, upperu)

        mask = maskl + masku
        # print"non zero elements are    " , np.count_nonzero(mask)
        
        if (np.count_nonzero(mask) > 4000):    #can be used to pick templates

            # cv2.imshow("imageWindow2", mask)
            # cv2.setMouseCallback("imageWindow2",onMouse, 0)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows() 

            templateList.append(tdict[index][0])
            templateList.append(tdict[index][1])
            templateList.append(tdict[index][2])

        index += 1


    #TEMPLATE MATCHING
    img = img2.copy()
    method = eval('cv2.TM_SQDIFF')

    chosenTem = []
    minTem = 90000000000
    top_left = 'lala'
    for template in templateList: 
        w, h = template.shape[::-1]
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if min_val < minTem:
            minTem = min_val
            chosenTem = template
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w-10, top_left[1] + h-10)

    if (top_left != 'lala'):
        #print("this is", chosenTem)
        name = get_key(namedict, chosenTem)
        text = "Image ID " + str(get_key(iddict, name)) + ": " + name 
        cv2.putText(image,text, (top_left[0], top_left[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(image,top_left, bottom_right, 255, 2)
        #cv2.imshow('Output Image', image) 

        ts = time.time()
        oName = str(int(ts)) + ".jpg"
        cv2.imwrite(oName, image)
        #cv2.waitKey(0) 
        #cv2.destroyAllWindows() 
        
        imgID = str(get_key(iddict, name))
        print "ID is: ", imgID

    return imgID

print(image_rec())

