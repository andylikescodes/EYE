import string
from pygaze import libtime
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.libscreen import Display, Screen
from constants import *

# Initialize Display to interact with monitor
disp = Display()

# Initialize Keyboard to collect key presses
kb = Keyboard(keylist=None, timeout=None)

# Create Screen for task instructions
inscr = Screen()
inscr.draw_text(
            text='Instructions:\nPress ENTER when you see your letter.\n\n' +
                 '(Press any key to continue)',
            fontsize=24)

# Create Screen with central fixation cross
fixscr = Screen()
fixscr.draw_fixation(fixtype='cross', diameter=16)

# Create Trial Screen and Screen to draw alphabetic letters on later
trialscr = Screen()
imgscr = Screen()

# Initialise new EyeTracker
tracker = EyeTracker(disp)
tracker.calibrate()

# Show instructions on Display then wait for key press
disp.fill(inscr)
disp.show()
kb.get_key()

# Iterate through n trials
for n in range(1, NUMTRIALS + 1):

    # Show trial number
    trialscr.clear()
    trialscr.draw_text(
                    text='Trial #%s\n(Press any key to begin)' % n,
                    fontsize=24)
    disp.fill(trialscr)
    disp.show()
    kb.get_key()

    # Start recording and display status message on EyeLink trackers
    tracker.start_recording()
    tracker.status_msg('Trial No.%s' % n)
    tracker.log('TRIAL %s START' % n)

    # Show fixation Screen on Display
    disp.fill(fixscr)
    disp.show()
    tracker.log('FIXATION ONSET')
    libtime.pause(FIXTIME)

    # Bool for looping
    pressed = False

    # Show alphabet Screen on Display
    for letter in string.ascii_lowercase:

        # Check if pressed
        if pressed:
            break

        # Prepare image Screen
        imgscr.clear()
        imgscr.draw_text(text=letter, fontsize=64)
        tracker.log('IMAGE ONSET, letter=%s' % letter)

        # Display letter
        imgscr.draw_text(text=letter, fontsize=64)
        disp.fill(imgscr)
        disp.show()

        # Initialize timer for each letter
        t0 = libtime.get_time()
        tstim = libtime.get_time()

        # Check for input
        key, presstime = kb.get_key(
                                keylist=['return', 'escape'],
                                timeout=IMGTIME)
        if key:
            tstim = presstime - t0
            tracker.log('ACTION RECORDED, delta_t=%.2f ms' % tstim)
            pressed = True

        # Clear Display
        tracker.log('IMAGE OFFSET, letter=%s' % letter)
        disp.fill()
        disp.show()

    # Log the end of trial
    tracker.log('TRIAL %s END' % n)
    tracker.stop_recording()

# Notify end to participant then wait for key press
inscr.clear()
inscr.draw_text(text='All done!\n\n(Press any key to exit)', fontsize=24)
disp.fill(inscr)
disp.show()
kb.get_key()

# Close connection to eye tracker and Display
tracker.close()
disp.close()
