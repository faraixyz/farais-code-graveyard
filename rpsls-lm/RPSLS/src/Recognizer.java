import java.util.ArrayList;

import com.leapmotion.leap.*;
import com.leapmotion.leap.Bone.Type;

public class Recognizer implements java.io.Serializable{
    
    //Thumb to pinky - same as hand.fingers();
    ArrayList<FingerGesture> gesture = new ArrayList<FingerGesture>();
   
    int handId;
    
    Recognizer(ArrayList<Frame> frames) {
        Hand tracking = frames.get(0).hands().get(0);
        this.handId = tracking.id();
        generateGesture(frames);
    }
    
    //Generates a list of five finger gestures over the given frames
    void generateGesture(ArrayList<Frame> frames) {
        for (int finger = 0; finger < 5; finger++) {
            float oldx = this.transformToPalm(frames.get(0).hand(handId).fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), 
                    frames.get(0).hand(handId)).getX();
            float oldy = this.transformToPalm(frames.get(0).hand(handId).fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), 
                    frames.get(0).hand(handId)).getY();
            float oldz = this.transformToPalm(frames.get(0).hand(handId).fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), 
                    frames.get(0).hand(handId)).getZ();
            ArrayList<Float> dxs = new ArrayList<Float>();
            ArrayList<Float> dys = new ArrayList<Float>();
            ArrayList<Float> dzs = new ArrayList<Float>();
            int stillCount = 0;
            for (Frame f : frames) {
                Hand curHand = f.hand(handId);
                float tempX =  this.transformToPalm(curHand.fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), curHand).getX();
                float tempY = this.transformToPalm(curHand.fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), curHand).getY();
                float tempZ = this.transformToPalm(curHand.fingers().get(finger).bone(Type.TYPE_PROXIMAL).direction(), curHand).getY();
                dxs.add(tempX - oldx);
                dys.add(tempY - oldy);
                dzs.add(tempZ - oldz);
                if (Math.abs(tempX - oldx) > .005 && Math.abs(tempY - oldy) > .005 || Math.abs(tempZ - oldz) > .005) {
                    stillCount += 1;
                }
                else {
                    stillCount = 0;
                }
                oldx = tempX;
                oldy = tempY;
                oldz = tempZ;
                if (stillCount > 5 && dxs.size() > 80) {
                    break;
                }
                
            }
            FingerGesture g = new FingerGesture(dxs, dys, dzs);
            g.simplify();
            gesture.add(g);
        }
    }
    
    //returns the percent that another gesture matches this one
    double matchesMe(ArrayList<FingerGesture> other) {
        if (other.size() != 5) {
            throw new IllegalArgumentException("I can't compare hands with different numbers of fingers");
        }
        int matches = 0;
        for (int i = 0; i < gesture.size(); i++) {
            if (gesture.get(i).sameAsMe(other.get(i))) {
                matches += 1;
            }
        }
        return matches / 5.0;
    }
    
    //Returns a new vector equal to the given vector, but translated to be relative to the given hand
    Vector transformToPalm(Vector unNormalized, Hand h) {
        Vector x = new Vector(1, 0, 0);
        Vector y = new Vector(0, 1, 0);
        Vector z = new Vector(0, 0, 1);
        Vector x1 = h.basis().getXBasis();
        Vector y1 = h.basis().getYBasis();
        Vector z1 = h.basis().getYBasis();
        return new Vector((float)((Math.cos(x1.angleTo(x)) * unNormalized.getX()) + (Math.cos(x1.angleTo(y)) * unNormalized.getY()) + (Math.cos(x1.angleTo(z)) * unNormalized.getZ())),
                (float) ((Math.cos(y1.angleTo(x)) * unNormalized.getX()) + (Math.cos(y1.angleTo(y)) * unNormalized.getY()) + (Math.cos(y1.angleTo(z)) * unNormalized.getZ())), 
                (float) ((Math.cos(z1.angleTo(x)) * unNormalized.getX()) + (Math.cos(z1.angleTo(y)) * unNormalized.getY()) + (Math.cos(z1.angleTo(z)) * unNormalized.getZ())));
                 
        
    }
    
    
}
