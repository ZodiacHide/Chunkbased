import time
import numpy as np
from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, GetWindowRect
from PIL import ImageGrab
import cv2

def checkWindowName(window_id: int) -> bool:
    '''
    Checks if target window is Minecraft.

    ### Parameters 
    window_id : int
        ID of target window'''
    
    name_window = GetWindowText(window_id)
    
    # Only care about in-game instance of minecraft
    # Launcher is not a game session
    if 'Minecraft' in name_window and 'Launcher' not in name_window:
        # Split the window title by spaces
        # try and split with period
        # if the substring is not split into 3
        # it is not the version string
        parsed_window_title = name_window.split()
        version = parsed_window_title[1]
        parsed_version = version.split('.')

        if len(parsed_version) == 3 and np.all(isinstance(i, int) for i in parsed_version):
            return True
        print("NOT VERSION")
        return False
    else:
        return False

def takeScreenshot(bbox: tuple[int, int, int, int]):
    '''
    Takes an image capture of active window.
    ### Parameters
        bbox : tuple
            Bounding box of active window
    ### Returns
        Image : PIL Image'''
    
    image = ImageGrab.grab(bbox)
    width, height = image.size

    # print(height)
    # exit()
    lower = 0
    upper = height
    left, right = 0, width
    box = (left, lower, right, upper)
    image_crop = image.crop(box)

    image_crop.show()
    return image_crop
        
while True:
    window = GetForegroundWindow()

    window_state = checkWindowName(window)

    if window_state:
        # Take screenshot to find coords
        SetForegroundWindow(window)
        bbox = GetWindowRect(window)
        takeScreenshot(bbox)
        
    time.sleep(1)