import random
import string
import time
import os, glob
from constants import *
from pygaze import libtime
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from pygaze.libscreen import Display, Screen


def close_all(tracker, log, disp):
    if tracker.recording:
        tracker.stop_recording()
    tracker.close()
    log.close()
    disp.close()
    quit()


def check_key(disp, quitscr, prevscr, keylist=None, timeout=None):
    if kb.get_key(keylist=keylist, timeout=timeout)[0] == 'escape':
        disp.fill(quitscr)
        disp.show()
        if kb.get_key()[0] == 'y':
            close_all(tracker, log, disp)
        else:
            disp.fill(prevscr)
            disp.show()
            kb.get_key(keylist=keylist, timeout=timeout)


# Initialize Display
disp = Display()

# Initialize Logfile
log = Logfile()
header = ['trialnum', 'fixonset_ms', 'imgonset_ms', 'imgoffset_ms',
          'presstime_ms', 'deltatime_ms', 'trueletter', 'userletter', 'sequence']
log.write(header)

# Initialize Keyboard
kb = Keyboard(keylist=None, timeout=None)

# Initialize Screens
inscr = Screen(fgc=COLORS['darkgreen'])
inscr.draw_text(
            text='Instructions:\nPress ENTER to pick a letter.\n' +
                 'You may press ESCAPE at any time to end the program.\n' +
                 '(Press any key to continue)',
            fontsize=24)

pickscr = Screen(fgc=COLORS['darkgreen'])
pickscr.draw_text(
            text='What letter was on screen when you first decided to move?',
            fontsize=24)

quitscr = Screen(fgc=COLORS['darkgreen'])
quitscr.draw_text(text='Are you sure you want to quit (y/[n])?', fontsize=24)

fixscr = Screen(fgc=COLORS['darkgreen'])
fixscr.draw_fixation(fixtype='cross', pw=2, diameter=16)

imgscr = Screen(fgc=COLORS['darkgreen'])
trialscr = Screen(fgc=COLORS['darkgreen'])

# Initialise EyeTracker
tracker = EyeTracker(disp)
tracker.calibrate()

# Make animation stuff
def libet_clock(disp):
    imgscr = Screen()
    imgscr.draw_image('/Users/Work/Documents/brain/EYE/test.jpg')
    disp.fill(imgscr)
    disp.show()
    key, press = kb.get_key(keylist=['return', 'escape'],
                        timeout=100)

''' START EXPERIMENT '''


# Show instructions on Display then wait for key press
disp.fill(inscr)
disp.show()
check_key(disp, quitscr, inscr)

# Test the image
cwd = os.getcwd()
asset_path = os.path.join(cwd, 'assets')

file_paths = []
# for file in os.listdir(asset_path):
#     if file.endswith(".gif"):
#         file_paths.append(os.path.join(asset_path, file))

for infile in sorted(glob.glob( os.path.join(asset_path, '*.gif') )):
    file_paths.append(infile)
#sorted(glob.glob('*.png'))
# imgscr.clear()
# imgscr.draw_image(file_paths[0])
# print(file_paths[0])
# disp.fill(imgscr)
# disp.show()
# check_key(disp, quitscr, imgscr)
print(file_paths)

key = ''

while (key != 'escape'):
    for path in file_paths:
        imgscr.clear()
        imgscr.draw_image(path)
        disp.fill(imgscr)
        disp.show()
        key, press = kb.get_key(keylist=['return', 'escape'],
                        timeout=100)
    #check_key(disp, quitscr, imgscr)


# Iterate through n trials
for n in range(1, TRIALS + 1):

    # Show trial number then wait for key press
    trialscr.clear()
    trialscr.draw_text(
                    text='Trial #%s\n' % n +
                         'wait until letters appear and press enter when ' +
                         'you feel the urge to.\n(Press any key to begin)',
                    fontsize=24)
    disp.fill(trialscr)
    disp.show()
    check_key(disp, quitscr, trialscr)

    # Start recording and display status message on EyeLink trackers
    tracker.start_recording()
    tracker.status_msg('Trial No.%s' % n)
    tracker.log('TRIAL %s START' % n)

    # Show fixation Screen on Display
    disp.fill(fixscr)
    fixonset = disp.show()
    tracker.log('FIXATION ONSET')
    check_key(disp, quitscr, fixscr, keylist=['escape'], timeout=FIXTIME)

    # list for storing letter sequence
    sequence = []

    # Variables for delayed loop termination
    afterpress = -1
    keysave = None

    # list of randomized alphabet to iterate through
    alpha = ''.join(random.sample(string.ascii_lowercase, 26))




    # Show alphabet Screen on Display
    for i in range(26):

        # append letter to sequence list
        sequence.append(alpha[i])

        # Check if pressed
        if afterpress > 0:
            afterpress -= 1
        elif afterpress == 0:
            break

        # Display letter
        imgscr.clear()
        imgscr.draw_text(text=alpha[i], fontsize=64)
        disp.fill(imgscr)
        if afterpress == -1:
            imgonset = disp.show()
        else:
            disp.show()
        tracker.log('IMAGE ONSET, letter=%s' % alpha[i])

        # Handle input
        key, press = kb.get_key(keylist=['return', 'escape'],
                                timeout=IMGTIME[i])
        if key == 'return':
            keysave = key
            presstime = press
            deltatime = presstime - imgonset
            trueletter = alpha[i]
            afterpress = 2
            tracker.log('ACTION RECORDED, delta_t=%.2f ms' % deltatime)
            libtime.pause(int(IMGTIME[i] - deltatime))
        if key == 'escape':
            disp.fill(quitscr)
            disp.show()
            if kb.get_key()[0].lower() == 'y':
                close_all(tracker, log, disp)

        # Clear Display
        disp.fill()
        if afterpress == 2 or afterpress == -1:
            imgoffset = disp.show()
        else:
            disp.show()
        tracker.log('IMAGE OFFSET, letter=%s, imgtime=%ims' % (alpha[i], int(IMGTIME[i])))

    # Ask participant for the letter they picked and log trial
    if keysave is not None:  # TODO: tests needed
        keysave = None
        disp.fill(pickscr)
        disp.show()
        userletter = kb.get_key()[0]
        log.write([n, fixonset, imgonset, imgoffset, presstime,
                   deltatime, trueletter, userletter, sequence])
    else:
        log.write([n, fixonset, 'NaN', 'NaN', 'NaN',
                   'NaN', 'NaN', 'NaN', sequence])

    # Log the end of trial
    tracker.log('TRIAL %s END' % n)
    tracker.stop_recording()

# Notify end to participant then wait for key press
inscr.clear()
inscr.draw_text(text='All done!\n(Press any key to exit)', fontsize=24)
disp.fill(inscr)
disp.show()
kb.get_key()

# Close connection to eye tracker and Display
close_all(tracker, log, disp)
