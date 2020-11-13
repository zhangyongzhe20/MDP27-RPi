import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import random
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

# initialise directory of image templates for template matching
IMG_DIR = '/home/pi/MDP27-RPi/threading/mains/mdp_labels/templates'

# mapping dictionary for images and their IDs
SYMBOL_ID_MAP = {
    'Arrow': 0,
    'up': 1,
    'down': 2,
    'right': 3,
    'left': 4,
    'go': 5,
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

#initialise some constants and threshods
MIN_CONTOUR_AREA = 2000 
MAX_CONTOUR_AREA = 9000 
MATCH_THRESHOLD = 4.23
MATCH_CONFIDENCE_COUNT = 5

# colour dictionary mapping colours to template IDs
colourDict = {
    'blue': [6, 14, 0],
    'green' : [7,12, 5],  
    'red' : [8, 11, 0],   
    'white' : [9, 13, 0],
    'yellow': [10, 15, 0],
    'nil': [-1, -1,-1]
}

# class for each possible symbol containing image and name
class Symbol:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.contour = None
        
# function to load all symbol/template images from specified directory
def load_symbols(filepath, clr_arr):
    symbols = []
    for i, symbol in enumerate(clr_arr):
        symbols.append(Symbol())
        symbols[i].name = symbol
        symbols[i].id = SYMBOL_ID_MAP[symbol]
        filename = '{}.jpg'.format(symbol)
        full_path = filepath + '/' + 't'+ filename
        symbol_img = cv2.imread(full_path)
        
        train_symbol_gray = cv2.cvtColor(symbol_img, cv2.COLOR_BGR2GRAY)
        _, train_symbol_thresh = cv2.threshold(train_symbol_gray, 70, 255, 0)
        _, train_symbol_ctrs, _ = cv2.findContours(train_symbol_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv2.contourArea, reverse=True)
        symbols[i].contour = train_symbol_ctrs[0]
    return symbols

# function to adjust brightness so that all images have similar HSV values for a given colour
def fix_brightness(img):
    img_dot = img
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    y,x,z = img.shape
    l_blur = cv2.GaussianBlur(l, (11, 11), 5)
    maxval = []
    count_percent = 3 #percent of total image
    count_percent = count_percent/100
    row_percent = int(count_percent*x) #1% of total pixels widthwise
    column_percent = int(count_percent*y) #1% of total pizel height wise
    for i in range(1,x-1):
        if i%row_percent == 0:
            for j in range(1, y-1):
                if j%column_percent == 0:
                    pix_cord = (i,j)
                    img_segment = l_blur[i:i+3, j:j+3]
                    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_segment)
                    maxval.append(maxVal)

    avg_maxval = round(sum(maxval) / len(maxval))
    if avg_maxval>35 and avg_maxval<45:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=1.8, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    elif avg_maxval<35 and avg_maxval>30:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=2.4, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    elif avg_maxval <30:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=2.7, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    elif avg_maxval > 70:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=0.7, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    elif avg_maxval > 60:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=1.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    else:
        norm_img2 = cv2.normalize(img, None, alpha=0, beta=1.4, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img2 = np.clip(norm_img2, 0, 1)
        norm_img2 = (255*norm_img2).astype(np.uint8)
        img = norm_img2
    return img

# extract binary mask for detected red area using HSV range
def extractRed(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 80, 100]) # used to be 80 - 2nd column
    upper_red = np.array([5, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([168, 80, 100])
    upper_red = np.array([182, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask1+mask2
    return mask

# extract binary mask for detected green area using HSV range
def extractGreen(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([50, 75, 60]) # used to be 60 2nd col
    upper_green = np.array([65, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    return mask


# extract binary mask for detected blue area using HSV range
def extractBlue(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([80, 80, 138])    #98 3rd col 
    upper_blue = np.array([98, 255, 255])  
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    return mask

# extract binary mask for detected yellow area using HSV range
def extractYellow(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 80, 120]) # original - 140 3rd col
    upper_yellow = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return mask

# extract binary mask for detected white area using HSV range
def extractWhite(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 0, 130])
    upper_red = np.array([55, 75, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    return mask

# extract colour masks for all colours and return those having maximum number of non-zero values
def preprocess_frame(image):
    colours = ['blue', 'green', 'red', 'white', 'yellow']
    extractColour = [extractBlue, extractGreen,
                     extractRed, extractWhite, extractYellow]
    clr = []
    res = []
    for i in range(len(colours)):
        colour = colours[i]
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = extractColour[i](image)
        if (np.count_nonzero(gray) > 16000 and colour!= 'white'):   
            res.append(gray)
            clr.append(colour)
        elif (np.count_nonzero(gray) > 20000 and np.count_nonzero(gray) < 77000 and colour == 'white'):        
            w, h = gray.shape
            gray_crop = gray[int(w/2):int(w), int(h/4): int(3*h/4)]
            if (np.count_nonzero(gray_crop) >500):
                res.append(gray)
                clr.append(colour)
    if clr == []:
        res.append(gray)
        clr.append("nil") 
    return res, clr
    
# extract bounding box coordinates around contours for input image
def extract_extreme_points(contour):
    extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
    extRight = tuple(contour[contour[:, :, 0].argmax()][0])
    extTop = tuple(contour[contour[:, :, 1].argmin()][0])
    extBottom = tuple(contour[contour[:, :, 1].argmax()][0])
    return extLeft, extTop, extRight, extBottom

# returns thresholded form of input image withtin coordinates obtained above
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

# main image recognition function
def img_rec_updated(image):
    train_symbols_here = []
    match_symbol_id = None
    # detect colours and get binary masks of corrrespnding input image
    pre_proc_frame , clr = preprocess_frame(image)
    
    # load templates for detected colours only
    if 'blue' in clr:
        blue_clr = ['6', 'y', 'down']
        train_symbols_here.append(load_symbols(IMG_DIR, blue_clr))
    if 'red' in clr:
        red_clr = ['8', 'v', 'left']
        train_symbols_here.append(load_symbols(IMG_DIR, red_clr))
    if 'green' in clr:
        green_clr = ['7', 'w', 'go']
        train_symbols_here.append(load_symbols(IMG_DIR, green_clr))
    if 'yellow' in clr:
        yellow_clr = ['0', 'z', 'right']
        train_symbols_here.append(load_symbols(IMG_DIR, yellow_clr))
    if 'white' in clr:
        white_clr = ['9', 'x', 'up']
        train_symbols_here.append(load_symbols(IMG_DIR, white_clr))


    #for each preprocessed image
    clostest_match_arr = []
    for i in range(len(pre_proc_frame)):
        fin_match = []
        # find and filter contours
        _, contours, hierarchy = cv2.findContours(pre_proc_frame[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        if contours == []:
            return -1
        filtered_contours = contours[0] 
        match_results = []

        # find bounding box coordinates around detected contours
        if len(filtered_contours) > 0:
            symbol_contour = filtered_contours
            extLeft, extTop, extRight, extBottom = extract_extreme_points(symbol_contour)
            symbol_thresh = extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom)
               
            # match detected contours to template and append required results to match_results list
            for i in range(len(train_symbols_here)):
                for train_symbol in train_symbols_here[i]:
                    match_score = cv2.matchShapes(symbol_contour, train_symbol.contour, 1, 0.0)
                    match_results.append({
                        'score': match_score,
                        'symbol': train_symbol.name,
                        'id': train_symbol.id
                    })
            
        # print("match_results is ",match_results)  

        fin_match.append(match_results)
        if match_results == []:
            return -1
        
        #find closest match (having minimum score)
        min_score = 1000
        for match in match_results:
            if match['score'] < min_score:
                closest_score = match['score']
                closest_id = match['id']
                closest_symbol = match['symbol']
                min_score = closest_score
        closest_match = {
            'score' : closest_score,
            'id': closest_id,
            'symbol': closest_symbol
        }

        if closest_match['score'] < MATCH_THRESHOLD:

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

        clostest_match_arr.append(closest_match)

    # find best possible match after checking all colour templates
    min_score = 10000
    for i in range(len(clostest_match_arr)):
        if clostest_match_arr[i]['score'] < min_score:
            min_score = clostest_match_arr[i]['score']
            the_closest_match = clostest_match_arr[i]

    # draw bounding box on output image
    x, y, w, h = cv2.boundingRect(symbol_contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    ts = int(time.time())
    # save output image 
    cv2.imwrite("/home/pi/MDP27-RPi/threading/mains/output_images/" + ts + ".jpg", image)
    print('Symbol: ' + str(the_closest_match['symbol']) + '; ID: ' + str(the_closest_match['id']))
    return the_closest_match['id']



def img_rec():
    # capture RAW image using RPi camea module
    camera = PiCamera()
    camera.resolution = (320,256)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture,format='bgr',use_video_port=True)
    img = rawCapture.array
    # rotate image required due to positioning of camera on robot
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # crop to approximate location of label in captured image to remove noise
    image = img[80:, 40:500]
    # adjust image brightness
    image = fix_brightness(image)
    # recognize input image label
    # image ID if label found, -1 if no label detected
    label = img_rec_updated(image)
    return label
