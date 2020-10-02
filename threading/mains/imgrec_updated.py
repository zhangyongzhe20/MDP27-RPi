import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import random

IMG_DIR = '/home/nishka/ImgRec/mdp_labels/templates'
# SYMBOL_TYPES = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E', 'Arrow', 'Circle']
SYMBOL_TYPES = ['0', '6', '7', '8', '9', 'v', 'w', 'x', 'y', 'z', 'Arrow', 'Circle']

SYMBOL_ID_MAP = {
    'Arrow': 0,
    'Arrow_white': 1,
    'Arrow_blue': 2,
    'Arrow_yellow': 3,
    'Arrow_red': 4,
    'Circle': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 10,
    'v': 11,
    'w': 12,
    'x': 13,
    'y': 14,
    'z': 15
}
THRESHOLD = 190
MIN_CONTOUR_AREA = 2000 # Assuming at a distance of 20 - 25cm
MAX_CONTOUR_AREA = 9000 # Assuming min distance of 10 - 15cm
MATCH_THRESHOLD = 0.23 + 4 #SWA MADE IT 5
MATCH_CONFIDENCE_COUNT = 5
ARROW_PIXEL_THRESHOLD = 7


colourDict = {
    'blue': [6, 14, 0],
    'green' : [7,12, 5],  
    'red' : [8, 11, 0],   
    'white' : [9, 13, 0],
    'yellow': [10, 15, 0]
}


class Symbol:
    '''
    Holds information about the Symbol Images, each symbol image
    will have an image and name
    '''
    def __init__(self):
        self.id = 0
        self.name = ''
        self.contour = None

def load_symbols(filepath):
    '''
    Loads the thresholded symbol images from directory, stores
    them into a list of Symbol objects
    '''
    symbols = []
    for i, symbol in enumerate(SYMBOL_TYPES):

        # print "i and symbol are", i, symbol

        symbols.append(Symbol())
        symbols[i].name = symbol
        symbols[i].id = SYMBOL_ID_MAP[symbol]
        filename = '{}.jpg'.format(symbol)

        full_path = filepath + '/' + 't'+ filename
        # print "full path is ", full_path 
        symbol_img = cv2.imread(full_path)
        train_symbol_gray = cv2.cvtColor(symbol_img, cv2.COLOR_BGR2GRAY)

        _, train_symbol_thresh = cv2.threshold(train_symbol_gray, 70, 255, 0)

        _, train_symbol_ctrs, _ = cv2.findContours(train_symbol_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv2.contourArea, reverse=True)
        
        # cv2.drawContours(symbol_img, train_symbol_ctrs, -1, (255, 0, 0), 3)
        # cv2.imshow("contours", symbol_img)
        # cv2.waitKey(0)

        # print "trainsymbolctrs is ", train_symbol_ctrs[0]
        symbols[i].contour = train_symbol_ctrs[0]
        
    return symbols
#############################################################################################

def extractRed(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # red [(0,80,150), (5,175,225)], [(170,80,150), (180,175,225)]
    # define range of red color in HSV
    lower_red = np.array([0, 80, 150])
    upper_red = np.array([5, 175, 225])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Range for upper range
    lower_red = np.array([170, 80, 150])
    upper_red = np.array([180, 175, 225])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Generating the final mask to detect red color
    mask = mask1+mask2
    return mask


def extractGreen(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #green [(58,80, 170), (72,140,215)]
    # define range of green color in HSV
    lower_green = np.array([45, 45, 150])
    upper_green = np.array([90, 140, 235])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    return mask


def extractBlue(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #blue [(90,90,165), (100,180,222)]
    # define range of blue color in HSV
    lower_blue = np.array([90, 80, 145])
    upper_blue = np.array([100, 180, 235])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    return mask


def extractYellow(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # yellow [(25, 60, 190), (30, 150, 250)]
    # define range of red color in HSV
    lower_yellow = np.array([25, 60, 190])
    upper_yellow = np.array([30, 150, 250])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    return mask


def extractWhite(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # white [(0,0,170), (55,25,255)]
    # define range of white color in HSV
    lower_red = np.array([0, 0, 170])
    upper_red = np.array([55, 25, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    return mask



#############################################################################################

def preprocess_frame(image):
    '''
    Returns the grayscaled, blurred and threshold camera image
    Currently threshold value of 40 seems to be working fine
    for all colors, but may need to look into adaptive thresholding
    depending on ambient light conditions
    '''
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # _, thresh = cv2.threshold(blur, THRESHOLD, 255, cv2.THRESH_BINARY)
    # return thresh


    colours = ['blue', 'green', 'red', 'white', 'yellow']
    extractColour = [extractBlue, extractGreen,
                     extractRed, extractWhite, extractYellow]
    clr = []

    for i in range(len(colours)):
        colour = colours[i]
        # print("colour ", colour)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = extractColour[i](image)
        # gray = cv2.GaussianBlur(gray, (3, 3), 0)
        # ip = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # _, contours, hierachy = cv2.findContours(gray, 1, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.fillPoly(gray, contours, (255, 255, 255))
        if (np.count_nonzero(gray) > 700 and colour!= 'white'):    #can be used to pick templates
            # cv2.imshow(colour, gray)
            res = gray
            clr.append(colour)
        elif colour == 'white':
            w, h = gray.shape
            gray_crop = gray[w/2:w, h/4: 3*h/4]
            if (np.count_nonzero(gray_crop) >100):
                # cv2.imshow("crapppppppppp", gray_crop)
                res= gray
                clr.append(colour)

            
    
    return res, clr
    


def filter_contour_size(contours):
    filtered = filter(
        lambda x: cv2.contourArea(x) >= MIN_CONTOUR_AREA and cv2.contourArea(x) <= MAX_CONTOUR_AREA,
        contours)
    return list(filtered)

def extract_extreme_points(contour):
    extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
    extRight = tuple(contour[contour[:, :, 0].argmax()][0])
    extTop = tuple(contour[contour[:, :, 1].argmin()][0])
    extBottom = tuple(contour[contour[:, :, 1].argmax()][0])

    return extLeft, extTop, extRight, extBottom


def extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom):
    placeholder_box = np.zeros((4, 2), dtype="float32")
    placeholder_box[0] = (extLeft[0], extTop[1]) # Top Left
    placeholder_box[1] = (extRight[0], extTop[1]) # Top Right
    placeholder_box[2] = (extRight[0], extBottom[1]) # Bottom Left
    placeholder_box[3] = (extLeft[0], extBottom[1]) # Bottom Right

    placeholder_width = extRight[0] - extLeft[0]
    placeholder_height = extBottom[1] - extTop[1]

    dst = np.array([
        [0,0],
        [placeholder_width - 1, 0],
        [placeholder_width - 1, placeholder_height - 1],
        [0, placeholder_height - 1]
    ], np.float32)
    M = cv2.getPerspectiveTransform(placeholder_box, dst)
    warp = cv2.warpPerspective(image, M, (placeholder_width, placeholder_height))
    warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

    symbol_card_blur = cv2.GaussianBlur(warp, (5, 5), 0)
    _, symbol_thresh = cv2.threshold(symbol_card_blur, 100, 255, cv2.THRESH_BINARY)
    
    return symbol_thresh

def derive_arrow_orientation(extLeft, extTop, extRight, extBottom):
    '''
    Filter which points are on the same x and y axis as the midpoint
    There should only be 3 points passing through the two filters at max
    in total since the extracted point on the flat edge of the arrow will
    not be at the midpoint.
    Whichever axis only one filtered point, the arrow's orientation will be
    in the other axis. i.e if len(filter_y) == 1, arrow is horizontal
    This implies that arrow tip is at the same y level as the midpoint
    Finally we check in the axis with only one filtered point whether it's
    before or after the midpoint to determine the exact direction of the arrow.
    '''
    x_midpoint = int((extLeft[0] + extRight[0]) / 2)
    y_midpoint = int((extTop[1] + extBottom[1]) /2 )

    arrow_name = ''
    filter_x = []
    filter_y = []
    
    for pnt in [extLeft, extTop, extRight, extBottom]:
        if abs(pnt[0] - x_midpoint) < ARROW_PIXEL_THRESHOLD:
            filter_x.append(pnt)
        elif abs(pnt[1] - y_midpoint) < ARROW_PIXEL_THRESHOLD:
            filter_y.append(pnt)

    # print "filter_x is", filter_x
    # print "filter_y is", filter_y

    if len(filter_x) == 1:
        # Arrow is vertical
        arrow_tip = filter_x[0][1]
        if (arrow_tip > y_midpoint):
            # Arrow is Down
            arrow_name =  'Arrow_blue'
        else:
            # Arrow is Up
            arrow_name =  'Arrow_white'
    elif len(filter_y) == 1:
        # Arrow is horizontal
        arrow_tip = filter_y[0][0]
        if (arrow_tip > x_midpoint):
            # Arrow is Right
            arrow_name = 'Arrow_yellow'
        else:
            # Arrow is Left
            arrow_name = 'Arrow_red'
    else:
        arrow_name = 'Arrow'
        
    return arrow_name, SYMBOL_ID_MAP[arrow_name]
    


def img_rec_updated(image):

    image = cv2.resize(image, (640, 480))
    resImg = image
    image = image[150:325, 210:370] 
    train_symbols = load_symbols(IMG_DIR)    
    match_symbol_id = None
    match_symbol_id = None
    pre_proc_frame , clr = preprocess_frame(image)
    

    # Uncomment if debugging threshold value
    # cv2.imshow('Frame Thresh', pre_proc_frame)
    # cv2.waitKey(0)

    edges = cv2.Canny(pre_proc_frame, 100,200)
    # cv2.imshow("canny", edges)
    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # cv2.fillPoly(image, contours, (255, 255, 255))
    
    # cv2.drawContours(image, contours[0], -1, (255, 0, 0), cv2.FILLED)
    # cv2.imshow("contours", image)
    # cv2.waitKey(0)
    filtered_contours = contours[0]
    
   



    # # _, thresh = cv2.threshold(blur, THRESHOLD, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(pre_proc_frame, 127, 255, 0)
    #  _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # filtered_contours = filter_contour_size(contours)
    # print "this is -----------", filtered_contours
    # cv2.drawContours(image, filtered_contours, -1, (255, 0, 0), 3)
    # cv2.imshow("contours", image)
    # cv2.waitKey(0)

   

    if len(filtered_contours) > 0:
        symbol_contour = filtered_contours
        
        x, y, w, h = cv2.boundingRect(symbol_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        extLeft, extTop, extRight, extBottom = extract_extreme_points(symbol_contour)
        symbol_thresh = extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom)
        # cv2.imshow("Detected Object", symbol_thresh)

        match_results = []
        for train_symbol in train_symbols:
            match_score = cv2.matchShapes(symbol_contour, train_symbol.contour, 1, 0.0)
            match_results.append({
                'score': match_score,
                'symbol': train_symbol.name,
                'id': train_symbol.id
            })

        # print "match results are  ", match_results
        colIDs = []
        for c in clr:
            cid = colourDict[c]
            colIDs.append(cid)

        potentialIDs = []
        potentialSymbols = []
        potentialScores = []
        for thisRes in range(len(match_results)):
            thisID = match_results[thisRes]['id'] 
            if thisID in colIDs[0]:
                #store in new
                
                # potentialIDs[thisID] = [match_results[thisRes]['symbol'] , match_results[thisRes]['score'] ]
                potentialIDs.append(thisID)
                potentialScores.append(match_results[thisRes]['score'])
                potentialSymbols.append(match_results[thisRes]['symbol'])
                

        # print("--------potentialScores------", potentialIDs)   
        
        closest_index = potentialScores.index(min(potentialScores))
        closest_score = min(potentialScores)
        closest_id = potentialIDs[closest_index]
        closest_symbol = potentialSymbols[closest_index]

        closest_match = {
            'score' : closest_score,
            'id': closest_id,
            'symbol': closest_symbol
        }
        # print "closest match", closest_match
        # closest_match = min(potentialIDs, key=lambda x: x)
        if closest_match['score'] < MATCH_THRESHOLD:
            # If detected arrow, further derive arrow orientation
            if closest_match['id'] == 0:
                # Uncomment if debugging for arrow detection
                # cv2.circle(image, (extLeft[0], extLeft[1]), 8, (0, 0, 255), 2)
                # cv2.circle(image, (extTop[0], extTop[1]), 8, (0, 0, 255), 2)
                # cv2.circle(image, (extRight[0], extRight[1]), 8, (0, 0, 255), 2)
                # cv2.circle(image, (extBottom[0], extBottom[1]), 8, (0, 0, 255), 2)
                # cv2.circle(image, (int(((extLeft[0] + extRight[0]) / 2)), int(((extTop[1] + extBottom[1]) / 2))), 8, (0, 0, 255), 2)

                arrow_name, arrow_id = derive_arrow_orientation(extLeft, extTop, extRight, extBottom)
                
                closest_match['symbol'] = arrow_name
                closest_match['id'] = arrow_id
                
            cv2.putText(
                image,
                # 'Symbol: ' + str(closest_match['symbol']) + '; ID: ' + str(closest_match['id']),
                "Image ID " + str(closest_match['id']),
                (extLeft[0] - 20, extTop[1] -5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255,0,0),1,cv2.LINE_AA
                # cv2.FONT_HERSHEY_DUPLEX,
                # 0.5, 
                # (255, 0, 0)
            )

            
            if match_symbol_id == closest_match['id']:
                match_count = match_count + 1
                
            else:
                match_symbol_id = closest_match['id']
                match_count = 1
                
            if (match_count == MATCH_CONFIDENCE_COUNT):
                    return(closest_match['id'])
        else:
            match_symbol_id = None
            match_count = 0

    print('Symbol: ' + str(closest_match['symbol']) + '; ID: ' + str(closest_match['id']))
    # Uncomment to visualize stream
    resImg[150:325, 210:370] = image
    cv2.imshow("output", resImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#generate 5 random inputs
# inPath = '/home/nishka/ImgRec/mdp_labels/'
# allInputs = [f for f in listdir(inPath) if isfile(join(inPath, f))]
# print "this is", allInputs
# rInputs = random.sample(range(0, len(allInputs)), 5)
# print "rInputs is ", rInputs

# for index in rInputs:
#     fileName = inPath + allInputs[index]
#     print("filename here is ", fileName

inPath = '/home/nishka/ImgRec/mdp_labels/'
fileName = inPath + 'up.jpeg'
img = cv2.imread(fileName)

img_rec_updated(img)



