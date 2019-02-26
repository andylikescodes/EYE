import string
from constants import *
from pygaze import libtime
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from pygaze.libscreen import Display, Screen


def close_all(tracker, log, disp):
    tracker.close()
    log.close()
    disp.close()
    quit()


# Initialize Display to interact with monitor
disp = Display()

# Initialize Logfile for saving text data
log = Logfile()
header = ['trialnum', 'fixonset (ms)', 'imgonset (ms)', 'imgoffset (ms)',
          'presstime (ms)', 'deltatime (ms)', 'trueletter', 'userletter']
log.write(header)

# Initialize Keyboard to collect key presses
kb = Keyboard(keylist=None, timeout=None)

# Create Screen for task instructions
inscr = Screen()
inscr.draw_text(
            text='-Instructions-\nPress ENTER to pick a letter.\n' +
                 'You may press ESCAPE at any time to end the program.\n' +
                 '(Press any key to continue)',
            fontsize=24)

# Create Screen for user's letter choice
pickscr = Screen()
pickscr.draw_text(
            text='What letter was on screen when you first decided to move?',
            fontsize=24)

# Create Screen with central fixation cross
fixscr = Screen()
fixscr.draw_fixation(fixtype='cross', pw=2, diameter=16)

# Create Trial Screen and Image Screen to draw alphabetic letters on later
trialscr = Screen()
imgscr = Screen()

# Initialise new EyeTracker
tracker = EyeTracker(disp, logfile=LOGFILE)
tracker.calibrate()

# Show instructions on Display then wait for key press
disp.fill(inscr)
disp.show()
if kb.get_key()[0] == 'escape':
    close_all(tracker, log, disp)

# Iterate through n trials
for n in range(1, NUMTRIALS + 1):

    # Show trial number then wait for key press
    trialscr.clear()
    trialscr.draw_text(
                    text='Trial #%s\n' % n +
                         'wait until letters appear and press enter when ' +
                         'you feel the urge to\n(Press any key to begin)',
                    fontsize=24)
    disp.fill(trialscr)
    disp.show()
    if kb.get_key()[0] == 'escape':
        close_all(tracker, log, disp)

    # Start recording and display status message on EyeLink trackers
    tracker.start_recording()
    tracker.status_msg('Trial No.%s' % n)
    tracker.log('TRIAL %s START' % n)

    # Show fixation Screen on Display then wait for key press
    disp.fill(fixscr)
    fix_onset = disp.show()
    tracker.log('FIXATION ONSET')
    libtime.pause(FIXTIME)

    # Variable for timed loop termination
    afterpress = -1

    # Show alphabet Screen on Display
    for letter in string.ascii_lowercase:

        # Check if pressed
        if afterpress > 0:
            afterpress -= 1
        elif afterpress == 0:
            break

        # Display letter
        imgscr.clear()
        imgscr.draw_text(text=letter, fontsize=64)
        disp.fill(imgscr)
        if afterpress == -1:
            img_onset = disp.show()
        else:
            disp.show()
        tracker.log('IMAGE ONSET, letter=%s' % letter)

        # Handle input
        key, press = kb.get_key(
                                keylist=['return', 'escape'],
                                timeout=IMGTIME)
        if key == 'return':
            presstime = press
            deltatime = presstime - img_onset
            trueletter = letter
            afterpress = 2
            tracker.log('ACTION RECORDED, delta_t=%.2f ms' % deltatime)
            libtime.pause(int(IMGTIME - deltatime))
        if key == 'escape':
            tracker.stop_recording()
            close_all(tracker, log, disp)

        # Clear Display
        disp.fill()
        if afterpress == 2 or afterpress == -1:
            img_offset = disp.show()
        else:
            disp.show()
        tracker.log('IMAGE OFFSET, letter=%s' % letter)

    # Ask participant for the letter they picked
    disp.fill(pickscr)
    disp.show()
    userletter = kb.get_key()[0]

    # Save trial to Logfile
    log.write([n, fix_onset, img_onset, img_offset, presstime,
               deltatime, trueletter, userletter])

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
close_all(tracker, log, disp)
