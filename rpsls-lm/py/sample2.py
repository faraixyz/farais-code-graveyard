import os, sys, inspect, thread, time
# src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


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
		
		self.frames = [x for x in self.frames if x > (time.time()-1)]
		print "FPS: ",len(self.frames)


class SampleListener (Leap.Listener):

	def on_connect(self, controller):
		print "Connected"
		self.FPS1 = FPS()
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_frame(self, controller):
		print "Frame available!"
		frame = controller.frame()
		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
          frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
		FPS.new()


def main():

	listener = SampleListener()

	controller = Leap.Controller()
	controller.add_listener(listener)

	# keep this process running 
	print "Press Enter to quit"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		#remove sample listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()