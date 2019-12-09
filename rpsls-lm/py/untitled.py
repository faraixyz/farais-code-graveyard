################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################



from __future__ import division
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import math


gesture = sys.argv[1]


outfile = open('data'+gesture+'.csv','wb')

finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']


def calc_dist(p1,p2):
    return math.sqrt((p2.x - p1.x) ** 2 +
                     (p2.y - p1.y) ** 2 +
                     (p2.z - p1.z) ** 2)   




def getSpeed(p1):
    return math.sqrt(p1.x**2 + p1.y**2 + p1.z**2)

class HandInformation(object):

    def __init__(self,hand):
        self.record_time = time.time() 

        # measure distances
        self.palm_position = hand.palm_position
        # print "Palm position:",self.palm_position/10
        self.finger_positions = {}

        # Get fingers
        for finger in hand.fingers:
            # create a dictionary for that finger type
            self.finger_positions[finger.type] = {}
            # get bones and save only the end of each bone
            for b in range(0,4):
                bone = finger.bone(b)
                #now get the x and y directions
                self.finger_positions[finger.type][b] = bone.next_joint

        # print self.finger_positions
        self.palm_to_fingers = {}
        #now create all the matchings
        for key in self.finger_positions:
            for i in range(4):
                self.palm_to_fingers[(key,i)] = calc_dist(self.palm_position,self.finger_positions[key][i])
                if i==3:
                    print "Finger: ",key," bone ",i," end: ",self.finger_positions[key][i]," to palm:",self.palm_to_fingers[(key,i)]

        self.finger_to_finger = {}
        for i in range(5):
            for j in [x for x in range(5) if x!=i]:
                if ((j,i) in self.finger_to_finger.keys()):
                    continue
                else:
                    self.finger_to_finger[(i,j)] = calc_dist(self.finger_positions[i][3],self.finger_positions[j][3])
                    print "Finger:",i," to finger:",j," distance is ",self.finger_to_finger[(i,j)]
        
        self.palm_velocity = getSpeed(hand.palm_velocity)
        print "Palm velocity: ",self.palm_velocity, " and direction is ",hand.direction


    def __str__(self):

        ret = str(self.palm_position)
        ret += "," + str(self.palm_velocity) + ","
        return ret

    def getArray(self):

        returnArray = []
        returnArray.append(self.record_time)
        returnArray.append(self.palm_velocity)
        for i in range(5):
            returnArray.append(self.palm_to_fingers[(i,3)])


        for i in range(5):
            for j in [x for x in range(5) if x!=i]:
                if ((j,i) in self.finger_to_finger.keys()):
                    continue
                else:
                    returnArray.append(self.finger_to_finger[(i,j)])
        return returnArray

        


class FPS(object):

    def __init__(self):
        self.frames = []
        self.frames.append(time.time())
        self.startTime = time.time()

    def new(self):
        if self.frames == []:
            self.frames = time.time()
        else:
            self.frames.append(time.time())
        
        now = time.time()
        self.frames = [x for x in self.frames if x > (now-1)]
        print "FPS: ",len(self.frames)



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"
        self.FPS1 = FPS()

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        self.FPS1.new()
        time.sleep(0.02)
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            if not hand.is_left:
                h = HandInformation(hand)
                resultStr = [int(x) for x in h.getArray()]
                outfile.write(str(resultStr)[1:-1]+'\n')



    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller


    print "READY?"
    time.sleep(1)
    print "3"
    time.sleep(1)
    print "2"
    time.sleep(1)
    print "1"
    time.sleep(1)
    
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
