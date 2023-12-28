from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, GetWindowRect
from PIL import ImageGrab
import pytesseract as pyt
import numpy as np
import time
pyt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

"""
This program is designed for Coordinates HUD from VanillaTweaks: https://vanillatweaks.net/

Created by https://github.com/ZodiacHide
Repository: https://github.com/ZodiacHide/Chunkbased
"""

def checkWindowName(window_id: int) -> bool:
    """
    Checks if target window is Minecraft.

    ### Parameters 
    window_id: int
        ID of target window"""
    
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

def takeScreenshot(bbox: tuple[int, int, int, int]) -> ImageGrab:
    """
    Takes an image capture of active window. Only works with windowed @2560x1440(2576x1426)
    ### Parameters
        bbox: tuple
            Bounding box of active window
    ### Returns
        Image: PIL Image"""
    
    expected_width, expected_height = 2576, 1426
    # screengrab with bounding box
    image = ImageGrab.grab(bbox)
    # image width and height
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

    # bottom quarter of image
    # middle third of image
    bot_image = image.crop((width/3, 3*height/4, width - width/3, height))

    # refine image
    width, height = bot_image.size
    coords_image = bot_image.crop((width/3 + width/22, height/2, width - width/3 - width/7, height - height/4))

    # coords_image.show()
    return coords_image

def getImageText(image: ImageGrab.grab) -> str:
    """
    Get the coordinates of VanillaTweaks HUD with image.
    
    ### Parameters
        image: Image
        
    ### Returns
        image_text: str"""
    
    image_text = pyt.image_to_string(image, lang='eng')

    return image_text

def getCoords(coords: str) -> np.ndarray:
    """
    Returns X, Y and Z values from image.
    
    ### Parameters
        coords: str
    ### Returns
        np.array([x_pos, y_pos, z_pos]): np.ndarray
    ### Variables
        x_pos: int
            X position of player
        y_pos: int
            Y position of player
        z_pos: int
            Z position of player"""
    
    # split coordinate string with spaces
    # if input is correct should have 3 indecies
    coords_split = coords.split(' ')
    if len(coords_split) < 3:
        return False
    
    try:
        x_pos = int(coords_split[0])
        y_pos = int(coords_split[1])
        z_pos = int(coords_split[2])
    except ValueError:
        return False
    else:
        return np.array([x_pos, y_pos, z_pos])

while True:
    window = GetForegroundWindow()

    window_state = checkWindowName(window)

    if window_state:
        # Take screenshot to find coords
        SetForegroundWindow(window)
        bbox = GetWindowRect(window)
        image = takeScreenshot(bbox)
        coords = getImageText(image)
        res = getCoords(coords)
        if res is not False:
            print(coords)
        
    time.sleep(1)