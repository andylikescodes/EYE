# from psychopy.visual import Window
# from constants import *
#
# disp = Window(size=DISPSIZE, units='pix', fullscr=True)
# disp.close()

from constants import *
from pygaze.display import Display
import pygaze.libtime as timer
from pygaze.screen import Screen

disp = Display()
# fixscreen = Screen()
# fixscreen.draw_fixation(fixtype='dot')
#
imgscreen = Screen()
imgscreen.draw_image('test.jpg')

# disp.fill(fixscreen)
# disp.show()
# timer.pause(2000)

disp.fill(imgscreen)
timer.pause(200000)
disp.show()
timer.pause(200000)

timer.pause(200000)
#
disp.close()