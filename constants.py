import os

# The DISPTYPE can be either 'pygame' or 'psychopy'
DISPTYPE = 'psychopy'
# DISPTYPE = 'pygame'

# The DISPSIZE should match your monitor's resolution
# DISPSIZE = (1920, 1080)
DISPSIZE = (1440, 900)

# DUMMYMODE should be True if no tracker is attached
DUMMYMODE = True

# Set the TRACKERTYPE to the brand you use
# TRACKERTYPE = 'eyelink'
TRACKERTYPE = 'dummy'

# Foreground colour set to green
FGC = (0, 128, 0)

# Background colour set to gray
BGC = (128, 128, 128)

# Fixation mark time (milliseconds)
FIXTIME = 5000

# Image time (milliseconds)
IMGTIME = 500

# Get the path to the current folder
DIR = os.path.dirname(__file__)
