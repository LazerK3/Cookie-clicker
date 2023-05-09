import win32gui
import win32ui
import win32con
import win32api
import handle
import GetScreenShot
import cv2
from PIL import Image
import numpy as np
import time
import threading
# Get the handle of the window to capture
window_title = "Cookie Clicker"

def find_image_within_image(cookiewindow, image_path, threshold=0.5):
    # Load the template and image
    template = cookiewindow
    image = image_path

    # Perform template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    

    # Get the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    # Define the confidence threshold for a match
    confidence_threshold = threshold

    # If the maximum similarity score is above the confidence threshold, the template is present
    if max_val > confidence_threshold:
        x,y = top_left
        yh, xh, rr = image.shape
        return [x,y,xh+x,yh+y]
    else:
        print("Cant find cookie")
        return None

def changeim(im, topleft, text):
    img = cv2.rectangle(im,(topleft[0], topleft[1]), (topleft[2], topleft[3]), (0,255,0), 2)
    img = cv2.putText(img, text, (topleft[0],topleft[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
    return img

def getclicklocation(topleft):
    clicklocation = [round((topleft[0]+topleft[2])/2),round((topleft[1]+topleft[3])/2)]
    return clicklocation

def click(x, y, hwnd1):
    clickxoffset = 0
    clickyoffset = -71
    lparam = win32api.MAKELONG(x+clickxoffset, y+clickyoffset)

    hwnd1= win32gui.FindWindowEx(hwnd1, None, None, None)
    win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONUP, None, lparam)

def clicktimes(x,y,times, hwnd1):
    global isClicking
    isClicking = True
    clickxoffset = 0
    clickyoffset = -71
    lparam = win32api.MAKELONG(x+clickxoffset, y+clickyoffset)

    hwnd1= win32gui.FindWindowEx(hwnd1, None, None, None)
    for i in range(times):
        win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        win32gui.SendMessage(hwnd1, win32con.WM_LBUTTONUP, None, lparam)
        time.sleep(0.1)
    isClicking = False
    
        

#hwnd = win32gui.FindWindow(None, window_title)
hwnd = handle.find_window(window_title)

#display test.png 
image = cv2.imread("test.png")
cv2.imshow("test",image)
cv2.waitKey(1000)

print(hwnd)
print(win32gui.GetWindowText(hwnd))



cookieloc = [0,0]
cookieim = cv2.imread("images/maincookie.png", cv2.COLOR_RGB2BGR)
storeitem = cv2.imread("images/storeitem.png", cv2.COLOR_RGB2BGR)
upgradeitem = cv2.imread("images/upgradeitem.png", cv2.COLOR_RGB2BGR)
goldcookie = cv2.imread("images/goldcookie.png", cv2.COLOR_RGB2BGR)

isClicking = False

while True:
    time1 = time.time()
    
    
    im = GetScreenShot.screenshot(hwnd)
    img = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
    
    topleft = find_image_within_image(img, cookieim)
    
    #Main Cookie Click
    if topleft != None:
        
        #img = cv2.rectangle(img,(topleft[0], topleft[1]), (topleft[2], topleft[3]), (0,255,0), 2)
        #img = cv2.putText(img, "Cookie", (topleft[0],topleft[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        changeim(img, topleft, "Cookie")
        
        clicklocation = getclicklocation(topleft)
        
        img = cv2.circle(img, (clicklocation[0], clicklocation[1]), 5, (0,0,255), -1)
        
        if isClicking == False:
            t = threading.Thread(target=clicktimes, args=(clicklocation[0], clicklocation[1], 100, hwnd))
            t.start()
    
    topleft = find_image_within_image(img, upgradeitem, 0.98)
    
    
    #Store Item Click
    if topleft != None:
        
        img = changeim(img, topleft, "Upgrade")
        
        clicklocation = getclicklocation(topleft)
        
        img = cv2.circle(img, (clicklocation[0], clicklocation[1]), 5, (0,0,255), -1)
        
        click(clicklocation[0], clicklocation[1], hwnd)
    
    
    topleft = find_image_within_image(img, goldcookie, 0.44)
    #Store Item Click
    if topleft != None:
        
        img = changeim(img, topleft, "Gold Cookie")
        
        clicklocation = getclicklocation(topleft)
        
        img = cv2.circle(img, (clicklocation[0], clicklocation[1]), 5, (0,0,255), -1)
        
        click(clicklocation[0], clicklocation[1], hwnd)
        
        
    #look for rgb(138, 255, 124)
    # rgb(102, 255, 102)
    
    #Producer Click
    lower = np.array([100, 250, 100])
    higher = np.array([138, 260, 135])
    mask = cv2.inRange(img, lower, higher)
    coords = cv2.findNonZero(mask)
    if coords is not None:
        print("Buying producer")
        img = changeim(img, [coords[-1][0][0]-100,coords[-1][0][1]-40,coords[-1][0][0]+200,coords[-1][0][1]+20 ], "Producer")
        img = cv2.circle(img, (coords[-1][0][0], coords[-1][0][1]), 5, (0,0,255), -1)
        click(coords[-1][0][0], coords[-1][0][1], hwnd)
    
    
    
    cv2.imshow("test",img)
    cv2.waitKey(100)
    
    time2 = time.time()
    fps = 1/(time2-time1)
    print(fps)
#Image._show(im)