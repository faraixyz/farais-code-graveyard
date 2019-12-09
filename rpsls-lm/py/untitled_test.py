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
from firebase import Firebase


# gesture = sys.argv[1]


# outfile = open('data'+gesture+'.csv','wb')
jsonfile = open('training.json','r')
for line in jsonfile:
    jsonstring = line

training_set = json.loads(jsonstring)
# print "Training:",training_set['r']['3']

#WORKING OK


class FirebaseClass(object):

    def __init__(self):
        self.userid = raw_input('Enter your user id')
        self.myurl = 'https://rpsuh16.firebaseio.com/games/'+self.userid
        self.fb = Firebase(self.myurl)
        self.fb.put({'prediction': 'R', 'confidence' : 0 , "value": "R"})
        self.fb.patch({'confidence' : 0})

        fbfile = open('../id.js','w')
        fbfile.write("var firebaseID = "+self.userid)

    def change(self,p,c):
        if (c == True):
            c = 1
        else:
            c = 0
        self.fb.patch({'value' : p.upper() , 'confidence' : c })


f = FirebaseClass()


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
        self.total = 0

    def new(self):
        self.total += 1
        if self.frames == []:
            self.frames = time.time()
        else:
            self.frames.append(time.time())
        
        now = time.time()
        self.frames = [x for x in self.frames if x > (now-1)]
    
        if self.total % 15 == 0:
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


def euclidean(v1,v2):

    return math.sqrt(sum( (v1 - v2)**2 for v1, v2 in zip(v1, v2)))


def get_distances(v,frame):

    # get the distance of this vector (given frame read) vs all other vectors 
    v = v[1:]
    train_rock = training_set['r'][str(frame)][1:]
    train_paper = training_set['p'][str(frame)][1:]
    train_scissor = training_set['s'][str(frame)][1:]
    # train_lizard = training_set['l'][str(frame)][1:]

    dr = euclidean(v,train_rock)
    dp = euclidean(v,train_paper)
    ds = euclidean(v,train_scissor)

    return [dr,dp,ds]



def choose_play(dr,dp,ds):
    """ It will return a boolean if it's confident and otherwise some other value """

    choose = ""
    valid = False

    best = min(dr, dp, ds)
    others = sorted([dr,dp,ds])[1:]

    confidence = sorted([(x/best) for x in others])

    if confidence[0] > 2.3:
        valid = True


    if (best == dr):
        choose = 'r'

    elif (best == dp):
        choose = 'p'
    else:
        choose = 's'

    if others[-1] < 90:
        valid = False

    return choose, valid




def main():
    # Create a sample listener and controller

    record = False


    
    # listener = SampleListener()
    FPS1 = FPS()
    controller = Leap.Controller()

    everything = {}
    movements_captured = 0
    frames_recorded = -1

    while (movements_captured < 80):
        FPS1.new()
        time.sleep(0.004)
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        done = False
        # Get hands

        if (len(frame.hands) == 0):
            print "WAIT"
            continue

        for hand in frame.hands:

            if not hand.is_left:

                h = HandInformation(hand)

                if h.palm_velocity > 315 and frames_recorded == -1:
                    record = True 
                    frames_recorded = 0
                    movements_captured +=1

                if record == True:
                    # print "RECORDING",frames_recorded
                    resultStr = [int(x) for x in h.getArray()]
                    # now we predict the proper classification based on some algorithm (distance from center)
                    dr,dp,ds = get_distances(resultStr,frames_recorded)

                    choose, done = choose_play(dr,dp,ds)
                    if (done == True):
                        print "Frame: ",frames_recorded," : ",dr,dp,ds
                        print "I predict a ",choose," in frame: ",frames_recorded
                        f.change(choose, done)




                    frames_recorded = frames_recorded + 1

                    # now we just print them for now

                    if frames_recorded > 100 or done==True:
                        frames_recorded = -1
                        record = False
                        print "total captured: ",movements_captured
                        time.sleep(1)
                        f.change(choose,False)
                        print "\n WAIT 2 SEC"
                        time.sleep(1)
                        print "\n WAIT 1 SEC"
                        time.sleep(1)




    # create a center of mass for each of the 3 movements at each of the 100 frames


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
