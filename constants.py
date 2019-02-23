import os

# DUMMYMODE should be True if no tracker is attached
# DUMMYMODE = False
DUMMYMODE = True

# Get Participant ID for logfile
LOGFILENAME = raw_input("Participant ID: ")
LOGFILE = LOGFILENAME[:]

# The DISPTYPE can be either 'pygame' or 'psychopy'
# DISPTYPE = 'psychopy'
DISPTYPE = "pygame"

# The DISPSIZE should match your monitor's resolution
# DISPSIZE = (1920, 1080)
DISPSIZE = (1440, 900)

# Set the TRACKERTYPE to the brand you use
TRACKERTYPE = "eyelink"
SACCVELTHRESH = 35
SACCACCTHRESH = 9500

# Dictionary of color codes
COLORS = {"darkgreen": (0, 100, 0),
          "green": (0, 128, 0),
          "lightgreen": (0, 204, 0),
          "lime": (0, 255, 0),
          "lightgray": (211, 211, 211),
          "silver": (192, 192, 192),
          "gray": (169, 169, 169),
          "darkgray": (128, 128, 128)}

# Foreground colour set to lime
FGC = COLORS["lime"]

# Background colour set to darkgray
BGC = COLORS["darkgray"]

# Fixation mark time (milliseconds)
FIXTIME = 5000

# Image time (milliseconds)
IMGTIME = 500

# Get the path to the current folder
DIR = os.path.dirname(os.path.abspath(__file__))
