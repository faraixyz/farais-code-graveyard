import java.util.ArrayList;

public class FingerGesture implements java.io.Serializable {
    
    float dx;
    float dy;
    float dz;
    
    final int TOLERANCE = 10;
    
    FingerGesture(ArrayList<Float> dxs, ArrayList<Float> dys, ArrayList<Float> dzs) {
        for (float x : dxs) {
            this.dx += 10000 * x;
        }
        this.dx /= dxs.size();
        for (float y : dys) {
            this.dy += 10000 * y;
        }
        this.dy /= dys.size();
        for (float z : dzs) {
            this.dz += 10000 * z;
        }
        this.dz /= dzs.size();
    }
    
    
    //Returns true if the given finger gesture matches the general trends ( no movement, positive movement, negative movement) as this one
    boolean sameAsMe(FingerGesture other) {
        return dx == other.dx && dy == other.dy && dz == other.dz; 
    }
    
    //Normalizes the values of this gesture to be only positive, negative, or no movement
    void simplify() {
        dx = simplify(dx);
        dy = simplify(dy);
        dz = simplify(dz);
    }
    
    //Returns the given float normalized into a simpler ternary value
    int simplify(float input) {
        if (Math.abs(input) < TOLERANCE) {
            return 0;
        }
        else if (input > 0) {
            return 1;
        }
        return -1;
    }

}
