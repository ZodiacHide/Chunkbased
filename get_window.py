from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, GetWindowRect
from PIL import ImageGrab, Image
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from typing import Union
import pytesseract as pyt
pyt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from minimap import MinimapPlotter

"""
This program is designed for use with Coordinates HUD from VanillaTweaks: https://vanillatweaks.net/

Minecraft OCR data by xHayden: https://github.com/xHayden/Minecraft-OCR

Created by https://github.com/ZodiacHide
Repository: https://github.com/ZodiacHide/Chunkbased
"""
class UnknownVersionError(TypeError):
    pass

def check_window_name_is_minecraft(window_id: int) -> bool:
    """
    Checks if target window is Minecraft.

    ### Parameters 
        ``window_id``: ID of active window
    """
    
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
        raise UnknownVersionError(f"Attempted to find coordinates of unknown window or Minecraft version. {name_window} is unknown")
    else:
        print("Target window is not Minecraft.")
        return False

def get_screenshot_active_window(bbox: tuple[int, int, int, int]) -> Image.Image:
    """
    Takes an image capture of target window. Only works with windowed @2560x1440(2576x1426)
    ### Parameters
        ``bbox``: Bounding box of active window
    ### Returns
        ``coords_image``: PIL image of target window"""
    
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
    coords_image = bot_image.crop((width/3 + width/22, height/2, width - width/3 - width/9, height - height/4))

    return coords_image

def get_coordinate_string_from_image(image: Image.Image) -> str:
    """
    Get the coordinates of VanillaTweaks HUD with image.
    
    ### Parameters
        ``image``: PIL style image of active Minecraft window.
        
    ### Returns
        ``image_text``: String containing player's X, Y and Z coordinates.
    """
    
    ## Image preprocessing
    # Convert PIL Image to OpenCV format (BGR)
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to emphasize digits
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    image_text = pyt.image_to_string(thresh_image, lang='mc', config='--psm 6 tessedit_char_whitelist=0123456789')   
    
    return image_text

def get_cardinal_char_from_image_colour(image: Image.Image) -> str:
    """
    Get the cardinal direction from VanillaTweaks HUD with image.
    
    ### Parameters
        ``image``: PIL style image of active Minecraft window.
        
    ### Returns
        ``image_text``: String containing player's cardinal viewing direction.
    """
    ## Image preprocessing
    # Convert PIL Image to OpenCV format
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 

    # Convert the image to HSV
    hsv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2HSV)

    # Define range of orange color in HSV
    lower_orange = np.array([30, 50, 50])  # Lower bound for orange in HSV
    upper_orange = np.array([50, 255, 255])  # Upper bound for orange in HSV

    # Threshold the HSV image to get only orange colors
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Invert the mask to keep the Orange
    orange_mask_inv = cv2.bitwise_not(orange_mask)

    # Bitwise-AND mask and original image
    isolated_orange = cv2.bitwise_and(open_cv_image, open_cv_image, mask=orange_mask_inv)

    image_text = pyt.image_to_string(isolated_orange, lang='mc', config='--psm 6 tessedit_char_whitelist=NEWS')

    return image_text

def get_cardinal_from_string(coords: str) -> Union[str, bool]:
    """
    Returns cardinal direction from image text.
    """
    # split coordinate string with spaces
    # if input is correct should have 3 indecies
    coords_split = coords.split(' ')
    if len(coords_split) < 3:
        pass
    if len(coords_split) > 3:
        if len(coords_split[3]) == 2:
            try:
                direction = int(coords_split[3][0])  
                if direction == 5:
                    return 'S'
            except ValueError:
                return coords_split[3][0]

def get_coordinate_from_string(coords: str) -> Union[np.ndarray, bool]:
    """
    Returns X, Y and Z values from image text.
    
    ### Parameters
        ``coords``: String containing coordinates from OCR.
    ### Returns
        ``np.array([x_pos, y_pos, z_pos])``: Numpy array containing player's X, Y and Z coordinates.
    ### Variables
        ``x_pos``: ``int``
            X position of player
        ``y_pos``: ``int``
            Y position of player
        ``z_pos``: ``int``
            Z position of player
    """
    
    # split coordinate string with spaces
    # if input is correct should have 3 indecies
    coords_split = coords.split(' ')
    if len(coords_split) < 3:
        pass
    else:  
        try:
            x_pos = int(coords_split[0])
            y_pos = int(coords_split[1])
            z_pos = int(coords_split[2])
        except ValueError:
            pass
        else:
            return np.array([x_pos, y_pos, z_pos])

def get_current_coordinates_error_handling(coords: tuple[Union[np.ndarray, bool], Union[np.ndarray, bool], Union[np.ndarray, bool]], 
                                           incorrect_coords_counter: int) -> tuple[np.ndarray, int]:
    """
    Returns current coordinates.

    Does not return coordinates immediately if there's a large change in coordinate values. \n
    
    ### Parameters
        ``coords``: ``np.ndarray([first_coord, second_coord, third_coord])``
            Array containing arrays of X, Y and Z coordinates \n
        ``incorrect_coords_counter``: ``int``
            Counter keeping track of consecutive large position offsets. Initial value should always be zero.
    ### Returns
        ``tuple`` containing ``np.ndarray`` containing X, Y and Z coordinates for player's current position and counter for consecutive large position offsets.
    """
    
    first_coord, second_coord, third_coord = coords
    # Verify all coordinates are arrays
    if not all((isinstance(first_coord, np.ndarray), isinstance(second_coord, np.ndarray), isinstance(third_coord, np.ndarray))):
        return first_coord, incorrect_coords_counter

    # All coordinates are arrays
    first_coord: np.ndarray; second_coord: np.ndarray; third_coord: np.ndarray
    coords_average = (second_coord+third_coord)/2

    # If fail to be close enough to average position too many times
    # assume player has travelled too fast for program and reset to current pos
    if incorrect_coords_counter > 2:
        second_coord, third_coord = first_coord, first_coord 
        incorrect_coords_counter = 0
        print(f"Resetting position to {first_coord}")
        return first_coord, incorrect_coords_counter
    for i, value in enumerate(first_coord):
        if value > 2*coords_average[i]:
            print(f"{axis[i]}={value} is very far away from average coordinate {axis[i]}={coords_average[i]}")
            incorrect_coords_counter += 1
            print(f"{incorrect_coords_counter} conescutive fails.")
            # ignore current position, assume it's wrong
            # assume second and third are good coords
            return second_coord, incorrect_coords_counter
        if abs(abs(value) - abs(coords_average[i])) > 16:
            print(f"{axis[i]}={value} is too far away from average coordinate {axis[i]}={coords_average[i]}")
            incorrect_coords_counter += 1
            print(f"{incorrect_coords_counter} conescutive fails.")
            # ignore current position, assume it's wrong
            # assume second and third are good coords
            return second_coord, incorrect_coords_counter
        
    return first_coord, incorrect_coords_counter

def check_player_standing_still(first_coord: np.ndarray, second_coord: np.ndarray, third_coord: np.ndarray) -> bool:
    """
    Checks if the player is standing still.
    """
    if np.array_equal(first_coord, second_coord) and np.array_equal(first_coord, third_coord):
        print("Player is standing still")
        return True
    else:
        print("Player is moving")
        return False

def set_new_coordinates_if_moving(first_coord: np.ndarray, second_coord: np.ndarray, 
                                  third_coord: np.ndarray, incorrect_coords_counter: int
                                  ) -> Union[tuple[np.ndarray, np.ndarray, int], bool]:
    """
    If the player is moving, update old coordinates.
    """
    is_player_standing_still = check_player_standing_still(first_coord, second_coord, third_coord)

    # first_coord is False after program startup
    # first_coord is False if poor data
    # ignore in both cases
    if first_coord is False or None:
        pass
    
    # player standing still
    # return first_coord
    elif is_player_standing_still:
        return first_coord, first_coord, incorrect_coords_counter
    
    # player is not moving
    # update previous positions
    elif not is_player_standing_still:
        third_coord = second_coord
        second_coord, incorrect_coords_counter = get_current_coordinates_error_handling((first_coord, second_coord, third_coord), incorrect_coords_counter)
        return second_coord, third_coord, incorrect_coords_counter

if __name__=='__main__':
    axis = np.array(['X', 'Y', 'Z'])
    incorrect_coords_counter = 0
    third_coord = False
    second_coord = False
    first_coord = False

    # Initiate Minimap
    map = MinimapPlotter()

while True:
    window = GetForegroundWindow()

    window_state = check_window_name_is_minecraft(window)

    if window_state:
        # Take screenshot to find coords
        SetForegroundWindow(window)
        # bounding box of window
        bbox = GetWindowRect(window)
        # screenshot of window
        image = get_screenshot_active_window(bbox)
        # coordinate text from screenshot
        text_coords = get_coordinate_string_from_image(image)
        # cardinal text from screenshot
        text_cardinal = get_cardinal_char_from_image_colour(image)
        # cardinal direction from string
        cardinal = get_cardinal_from_string(text_cardinal)

        first_coord = get_coordinate_from_string(text_coords)
        if first_coord is not None:
            try:
                # New player coordinates
                second_coord, third_coord, incorrect_coords_counter = set_new_coordinates_if_moving(first_coord, second_coord, third_coord, incorrect_coords_counter)
                # Update player position
                map.update_minimap(second_coord, chunk_range=2, direction=cardinal)
            except TypeError:
                print("Something wrong")
                pass

    plt.pause(0.1)
    time.sleep(0.1)
