import os

# Get the path to the current folder
DIR = os.path.dirname(os.path.abspath(__file__))

# DUMMYMODE should be True if no tracker is attached
DUMMYMODE = True

# Get Participant ID for logfile
LOGFILENAME = raw_input("Participant ID: ")
LOGFILE = LOGFILENAME[:]

# The DISPTYPE can be either 'pygame' or 'psychopy'
DISPTYPE = "psychopy"

# The DISPSIZE should match your monitor's resolution
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
          "darkgray": (169, 169, 169),
          "gray": (128, 128, 128)}

# Foreground colour set to lime
FGC = COLORS["green"]

# Background colour set to darkgray
BGC = COLORS["darkgray"]

# Fixation mark time (milliseconds)
FIXTIME = 5000

# Image time (milliseconds)
IMGTIME = 500

# Number of trials
while True:
    try:
        NUMTRIALS = int(raw_input("Number of trials: "))
    except ValueError:
        print "Invalid input: non-integer value"
        continue
    if NUMTRIALS < 1 or NUMTRIALS > 100:
        print "Invalid input: out of range, select from 1 to 100 trials"
        continue
    else:
        break
