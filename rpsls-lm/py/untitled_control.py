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

import json


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
                # if i==3:
                    # print "Finger: ",key," bone ",i," end: ",self.finger_positions[key][i]," to palm:",self.palm_to_fingers[(key,i)]

        self.finger_to_finger = {}
        for i in range(5):
            for j in [x for x in range(5) if x!=i]:
                if ((j,i) in self.finger_to_finger.keys()):
                    continue
                else:
                    self.finger_to_finger[(i,j)] = calc_dist(self.finger_positions[i][3],self.finger_positions[j][3])
                    # print "Finger:",i," to finger:",j," distance is ",self.finger_to_finger[(i,j)]
        
        self.palm_velocity = getSpeed(hand.palm_velocity)
        # print "Palm velocity: ",self.palm_velocity, " and direction is ",hand.direction


    def __str__(self):

        ret = str(self.palm_position)
        ret += "," + str(self.palm_velocity) + ","
        return ret

    def getArray(self):

        returnArray = []
        # returnArray.append(self.record_time)
        returnArray.append(self.palm_velocity)
        for i in range(5):
            returnArray.append(self.palm_to_fingers[(i,3)])


        for i in range(5):
            for j in [x for x in range(5) if x!=i]:
                if ((j,i) in self.finger_to_finger.keys()):
                    continue
                else:
                    returnArray.append(self.finger_to_finger[(i,j)])

        # print "returning ",returnArray
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


def get_averages(m,i,data):

    print "Getting averages for ",m," and frame: ",i

    #for each list in data
    # print data
    averages = [0]*(len(data[0])-1)

    for i in range(len(data[0])-1):
        dt = [x[i] for x in data]
        averages[i] = sum(dt)/len(dt)

    # print averages
    return averages




def main():
    # Create a sample listener and controller

    record = False
    
    # listener = SampleListener()
    FPS1 = FPS()
    controller = Leap.Controller()

    everything = {}

    for m in ['r','s','p','l','sp']:
        print "\n\n \t \tWILL START RECORDING FOR ",m

        frames_recorded = -1
        record = False

        print "READY?"
        print "3"
        # time.sleep(1)
        print "2"
        time.sleep(1)
        print "1"
        time.sleep(1)
        time.sleep(1)
        movements_captured = 0
        all_movements = {}

        while (movements_captured < 20):
            FPS1.new()
            time.sleep(0.004)
            # Get the most recent frame and report some basic information
            frame = controller.frame()

            # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
            #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

            # Get hands
            for hand in frame.hands:

                if not hand.is_left:

                    h = HandInformation(hand)

                    if h.palm_velocity > 315 and frames_recorded == -1:
                        record = True 
                        frames_recorded = 0
                        movements_captured +=1

                    if record == True:
                        print "RECORDING",frames_recorded
                        resultStr = [int(x) for x in h.getArray()]
                        print resultStr
                        if (frames_recorded not in all_movements.keys()):
                            all_movements[frames_recorded] = [resultStr]
                        else:
                            all_movements[frames_recorded].append(resultStr)
                        # outfile.write(str(movements_captured)+','+str(frames_recorded)+','+str(resultStr)[1:-1]+'\n')
                        frames_recorded = frames_recorded + 1

                        if frames_recorded > 100:
                            frames_recorded = -1
                            record = False
                            print "total captured: ",movements_captured," out of 20 for ",m
                            # time.sleep(1)
                            if (movements_captured >= 20):
                                break
                            print "\n WAIT 3 SEC"
                            # time.sleep(1)
                            print "\n WAIT 2 SEC"
                            time.sleep(1)
                            print "\n WAIT 1 SEC"
                            time.sleep(1)


        everything[m] = all_movements


    # create a center of mass for each of the 3 movements at each of the 100 frames
    center_mass = {}
    for m in ['s','r','p','l','sp']:
        center_mass[m] = {}
        for i in range(101):
            # print everything[m]
            # print everything[m][i]
            center_mass[m][i] = get_averages(m,i,everything[m][i])
            outfile.write(str(i)+','+(str(center_mass[m][i])[1:-1])+','+m+'\n')



    file = open('training.json','wb')
    file.write(json.dumps(center_mass, separators=(',', ':')))

    # Have the sample listener receive events from the controller
    # controller.add_listener(listener)

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
