from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, GetWindowRect
from PIL import ImageGrab
import pytesseract as pyt
import numpy as np
import time

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
    Takes an image capture of active window. Only works with windowed @2560x1440(2576x1426)
    ### Parameters
        bbox : tuple
            Bounding box of active window
    ### Returns
        Image : PIL Image'''
    
    expected_width, expected_height = 2576, 1426
    image = ImageGrab.grab(bbox)
    width, height = image.size

    if width != expected_width:
        print("WARNING: Width of window is not 2576px, program will not work as expected")
    if height != expected_height:
        print("WARNING: Height of window is not 1426, program will not work as expected")

    '''
    crop box is created in top left corner.
    box = [left, upper, right, lower]
    left - how far from the left to start
    right - how far from the left to stop
    upper - how far from top to start
    lower - how far from top to stop'''

    bot_image = image.crop((width/3, 3*height/4, width - width/3, height))

    width, height = bot_image.size
    coords_image = bot_image.crop((width/4, height/2, width - width/4, height - height/4))

    coords_image.show()
    return coords_image
        
while True:
    window = GetForegroundWindow()

    window_state = checkWindowName(window)

    if window_state:
        # Take screenshot to find coords
        SetForegroundWindow(window)
        bbox = GetWindowRect(window)
        takeScreenshot(bbox)
        
    time.sleep(1)