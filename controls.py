import numpy as np
from constants import *


def libet_clock(imgscr, clock_speed=100):
	'''
		clock_speed = How fast the clock rotate
		imgscr = The pygaze screen that the clock is draw on.
	'''
	for path in LIBETCLOCKPATH:
	    imgscr.clear()
	    imgscr.draw_image(path)
	    disp.fill(imgscr)
	    disp.show()
	    key, press = kb.get_key(keylist=['return', 'escape'],
	                    timeout=clock_speed)

class Trial:
	def __init__(tracker, imgscr, report):
		self.report=report
		self.imgscr=imgscr

	def 

class Block:
	def __init__():