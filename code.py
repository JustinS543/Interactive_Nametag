import time
import board
import displayio
# import neopixel
import adafruit_touchscreen
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font

screen_width = 320
screen_height = 480
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_YD, board.TOUCH_YU,
                                      board.TOUCH_XR, board.TOUCH_XL,
                                      calibration=((5200, 59000),
                                                   (5800, 57000)),
                                      size=(screen_width, screen_height))

# pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)
# WHITE = 0xffffff
# RED = 0xff0000
# YELLOW = 0xffff00
# GREEN = 0x00ff00
# BLUE = 0x0000ff
# PURPLE = 0xff00ff
# BLACK = 0x000000

pyportal = PyPortal()
display = board.DISPLAY
display.rotation = 270 

splash = displayio.Group()  # The Main Display Group
view1 = displayio.Group()  # Group for View 1 objects
view2 = displayio.Group()  # Group for View 2 objects
view3 = displayio.Group()  # Group for View 3 objects
bg_group = displayio.Group()
view_live = 1

font = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')

def hideLayer(hide_target):
    try:
        splash.remove(hide_target)
    except ValueError:
        pass 

def showLayer(show_target):
    try:
        time.sleep(0.1)
        splash.append(show_target)
    except ValueError:
        pass
    
def switch_view(what_view):
    global view_live
    if what_view == 1:
        hideLayer(view2)
        hideLayer(view3)
        showLayer(view1)
        view_live = 1
        
    elif what_view == 2:
        # global icon
        hideLayer(view1)
        hideLayer(view3)
        showLayer(view2)
        view_live = 2
        
    else:
        hideLayer(view1)
        hideLayer(view2)
        showLayer(view3)
        view_live = 3
        
showLayer(view1)
hideLayer(view2)
hideLayer(view3)

board.DISPLAY.show(splash)

def set_image(group, filename):
    """Set the image file for a given goup for display.
    This is most useful for Icons or image slideshows.
        :param group: The chosen group
        :param filename: The filename of the chosen image
    """
    print("Set image to ", filename)
    if group:
        group.pop()

    if not filename:
        return  # we're done, no icon desired

    # CircuitPython 6 & 7 compatible
    image_file = open(filename, "rb")
    image = displayio.OnDiskBitmap(image_file)
    image_sprite = displayio.TileGrid(image, pixel_shader=getattr(image, 'pixel_shader', displayio.ColorConverter()))

    # # CircuitPython 7+ compatible
    # image = displayio.OnDiskBitmap(filename)
    # image_sprite = displayio.TileGrid(image, pixel_shader=image.pixel_shader)

    group.append(image_sprite)

set_image(bg_group, "/images/BGimage.bmp")
set_image(view1, "images/test1.bmp")
set_image(view2, "images/Newtest.bmp")
set_image(view3, "images/Billie.bmp")

# Default button styling:
BUTTON_HEIGHT = int(40)
BUTTON_WIDTH = int(80)

# We want three buttons across the top of the screen
TAPS_HEIGHT = int(screen_height/3)
TAPS_WIDTH = int(screen_width)
TAPS_Y = 0

buttons = []

button_view1 = Button(x=0, y=0, width=TAPS_WIDTH, height=TAPS_HEIGHT, label=" ", label_font=font, label_color=0xffffff,
                     fill_color=0xffffff, outline_color=0xffffff,
                     selected_fill=0xffffff, selected_outline=0xffffff,
                     selected_label=0xffffff, style=Button.RECT)
buttons.append(button_view1)
button_view2 = Button(x=0, y=TAPS_HEIGHT, width=TAPS_WIDTH, height=TAPS_HEIGHT, label=" ", label_font=font, label_color=0xffffff,
                     fill_color=0xffffff, outline_color=0xffffff,
                     selected_fill=0xffffff, selected_outline=0xffffff,
                     selected_label=0xffffff, style=Button.RECT)
buttons.append(button_view2)
button_view3 = Button(x=0, y=TAPS_HEIGHT*2, width=TAPS_WIDTH, height=TAPS_HEIGHT, label=" ", label_font=font, label_color=0xffffff,
                     fill_color=0xffffff, outline_color=0xffffff,
                     selected_fill=0xffffff, selected_outline=0xffffff,
                     selected_label=0xffffff, style=Button.RECT)
buttons.append(button_view3)

button_view1.selected = True
button_view2.selected = True
button_view3.selected = True

for b in buttons:
    splash.append(b)

while True:
    touch = ts.touch_point
    
    if touch:
        
        for i, b in enumerate(buttons):
            
            if b.contains(touch):
            
                if i == 0 and view_live != 1:
                    switch_view(1)
                    while ts.touch_point:
                        pass
                if i == 1 and view_live != 2:
                    switch_view(2)
                    while ts.touch_point:
                        pass
                if i == 2 and view_live != 3:
                    switch_view(3)
                    while ts.touch_point:
                        pass
                else:
                    switch_state = 0
                    # pixel.fill(BLACK)
                    print("Swich OFF")
                    # for debounce
                    while ts.touch_point:
                        pass