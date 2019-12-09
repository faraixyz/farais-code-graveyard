import java.awt.Desktop;
import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.UUID;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.FirebaseError;
import com.firebase.client.ValueEventListener;
import com.leapmotion.leap.*;

class Runner implements ValueEventListener{
    
    ArrayList<Recognizer> rock = new ArrayList<Recognizer>();
    ArrayList<Recognizer> paper = new ArrayList<Recognizer>();
    ArrayList<Recognizer> scissors = new ArrayList<Recognizer>();
    Controller c;
    Firebase f;
    String playerId;
    
    final int trainings = 3;
    final int frameNum = 300;
    final int milliSleep = 4;
    final double fastGuessTolerance = .6;
    
    Runner (Firebase firebase, String p) {
        this.c = new Controller();
        while(!c.isConnected());
        this.f = firebase;
        this.playerId = p;
    }
    Runner (Firebase firebase, String p, String filepath) {
        this.c = new Controller();
        this.f = firebase;
        this.playerId = p;
        
        try
        {
           FileInputStream fileIn = new FileInputStream(filepath + "rock.ser");
           ObjectInputStream in = new ObjectInputStream(fileIn);
           rock = (ArrayList<Recognizer>) in.readObject();
           in.close();
           fileIn.close();
           
           fileIn = new FileInputStream(filepath + "paper.ser");
           in = new ObjectInputStream(fileIn);
           paper = (ArrayList<Recognizer>) in.readObject();
           in.close();
           fileIn.close();
           
           fileIn = new FileInputStream(filepath + "scissors.ser");
           in = new ObjectInputStream(fileIn);
           scissors = (ArrayList<Recognizer>) in.readObject();
           in.close();
           fileIn.close();
        }catch(IOException i)
        {
           i.printStackTrace();
           return;
        }catch(ClassNotFoundException c)
        {
           System.out.println("class not found");
           c.printStackTrace();
           return;
        }
        
    }
    
    //Displays a 3 second countdown for the given string prompt
    void countdown(String prompt) {
        
        System.out.println(prompt + " in 3...");
        try {
            Thread.sleep(1000);                 
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        System.out.println(prompt + " in 2...");
        try {
            Thread.sleep(1000);                 
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        System.out.println(prompt + " in 1...");
        try {
            Thread.sleep(1000);                 
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        System.out.println("Throw!");  
    }
    
    //initializes rock, paper, and scissors with comparison values
    void train() {
        System.out.println("Activating leapmotion");
        try {
            Thread.sleep(1000);                 
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        ArrayList<Frame> frames;
        for (int  i = 0; i < trainings; i++) {
            countdown("Capturing your rock");

            frames = new ArrayList<Frame>();
            f.child(playerId).child("training").setValue("R");       // Rock Training!
            while (frames.size() < frameNum) {
                try {
                    Thread.sleep(milliSleep);                 
                } catch(InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
                frames.add(c.frame());
            }
            f.child(playerId).child("training").setValue("N");       // Rock Training Done!
            rock.add(new Recognizer(frames));
        }
        
        for (int  i = 0; i < trainings; i++) {
            countdown("Capturing your paper");

            frames = new ArrayList<Frame> ();
            f.child(playerId).child("training").setValue("P");       // Paper Training!
            while (frames.size() < frameNum) {
                try {
                    Thread.sleep(milliSleep);                 
                } catch(InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
                frames.add(c.frame());
            }
            f.child(playerId).child("training").setValue("N");       // Paper Training Done!
            paper.add(new Recognizer(frames));
        }
        
        for (int  i = 0; i < trainings; i++) {
            countdown("Capturing your scissors");

            frames = new ArrayList<Frame> ();
            f.child(playerId).child("training").setValue("S");       // Scissors Training!
            while (frames.size() < frameNum) {
                try {
                    Thread.sleep(milliSleep);                 
                } catch(InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
                frames.add(c.frame());
            }
            f.child(playerId).child("training").setValue("N");       // Scissors Training Done!
            scissors.add(new Recognizer(frames));
        }
    }
    
    //Returns the string of the gesture recorded after the countdown, based on predictive stuff
    String predict() {    
        // countdown("Predicting you");
        f.child(playerId).child("value").setValue("N");
        
        f.child(playerId).child("prediction").setValue("T");
        ArrayList<Frame> frames = new ArrayList<Frame>();
        while (frames.size() < 80) {
            try {
                Thread.sleep(milliSleep);                 
            } catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
            frames.add(c.frame());
        }
        f.child(playerId).child("prediction").setValue("F");
        Recognizer test = new Recognizer(frames);
        double rockMatch = 0;
        for (int i = 0; i < rock.size(); i++) {
            rockMatch += rock.get(i).matchesMe(test.gesture);
        }
        double scisMatch = 0;
        for (int i = 0; i < scissors.size(); i++) {
            scisMatch += scissors.get(i).matchesMe(test.gesture);
        }
        double paperMatch = 0;
        for (int i = 0; i < paper.size(); i++) {
            paperMatch += paper.get(i).matchesMe(test.gesture);
        }
        
        if (rockMatch > scisMatch && rockMatch > paperMatch) {
            System.out.println("I think it's rock");
            return "R";
        }
        else if (scisMatch > paperMatch) {
            System.out.println("I think it's scissors");
            return "S" ;
        }
        else if (paperMatch > 1) {
            System.out.println("I think it's paper");
            return "P" ;
        }
        else {
            System.out.println("I think it's default");
            return "P";
        }
    }
    
    String fastPredict() {
        countdown("Predicting you");
        f.child(playerId).child("value").setValue("N");
        
        f.child(playerId).child("prediction").setValue("T");
        ArrayList<Frame> frames = new ArrayList<Frame>();
        boolean predicted = false;
        while (frames.size() < frameNum/3) {
            frames.add(c.frame());
            Recognizer test = new Recognizer(frames);
            
            double rockMatch = 0;
            for (int i = 0; i < rock.size(); i++) {
                rockMatch += rock.get(i).matchesMe(test.gesture);
            }
            double scisMatch = 0;
            for (int i = 0; i < scissors.size(); i++) {
                scisMatch += scissors.get(i).matchesMe(test.gesture);
            }
            double paperMatch = 0;
            for (int i = 0; i < paper.size(); i++) {
                paperMatch += paper.get(i).matchesMe(test.gesture);
            }
            System.out.println("RockMatch: " + rockMatch);
            System.out.println("ScissorsMatch: " + scisMatch);
            System.out.println("PaperMatch: " + paperMatch);
            if (rockMatch > fastGuessTolerance + .2 && 
                    frames.size() > 30 && 
                    Math.max(rockMatch, Math.max(scisMatch, paperMatch)) == rockMatch) {
                System.out.println("I took " + frames.size() + " frames");
                System.out.println("I think it's rock");
                return "R";
            }
            else if (scisMatch > fastGuessTolerance && frames.size() > 30 && 
                    Math.max(rockMatch, Math.max(scisMatch, paperMatch)) == scisMatch) {
                System.out.println("I took " + frames.size() + " frames");
                System.out.println("I think it's scissors");
                return "S" ;
            }
            else if (paperMatch > fastGuessTolerance && frames.size() > 30 && 
                    Math.max(rockMatch, Math.max(scisMatch, paperMatch)) == paperMatch) {
                System.out.println("I took " + frames.size() + " frames");
                System.out.println("I think it's paper");
                return "P" ;
            }
        }
        System.out.println("I never came to a conclusion");
        return "P";
    }

    //Starts training and prediction once any data changes on the firebase
    @Override
    public void onDataChange(DataSnapshot arg0) {
        try {
            Thread.sleep(5000);                 
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
        f.child(playerId).child("value").setValue(predict());
    }

    @Override
    public void onCancelled(FirebaseError arg0) {
        // TODO Auto-generated method stub
    }
    
    public void saveTraining() {
        try
        {
           FileOutputStream fileOut =
           new FileOutputStream("rock.ser");
           ObjectOutputStream out = new ObjectOutputStream(fileOut);
           out.writeObject(this.rock);
           out.close();
           fileOut.close();
           
           fileOut = new FileOutputStream("paper.ser");
           out = new ObjectOutputStream(fileOut);
           out.writeObject(this.paper);
           out.close();
           fileOut.close();
           
           fileOut = new FileOutputStream("scissors.ser");
           out = new ObjectOutputStream(fileOut);
           out.writeObject(this.scissors);
           out.close();
           fileOut.close();
        }catch(IOException i)
        {
            i.printStackTrace();
        }
    }
    
}

class Main {
    
    //Creates the link to the firebase and makes a listener
    public static void main(String[] args) throws InterruptedException {
        Firebase ref = new Firebase("https://rpsuh16.firebaseio.com/games");

        // Generate Random UUID and create id.js
        String id = UUID.randomUUID().toString();
        PrintWriter writer;
        try {
            writer = new PrintWriter("../id.js", "UTF-8");
            writer.println("var firebaseID=" + '"' + id + '"');
            writer.close();
        } catch (FileNotFoundException | UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        // Open HTML file with a default HTML file opener.
        try {
            Desktop.getDesktop().browse(new File("../index.html").toURI()); //new URI("http://localhost:8000/index.html"));
        } catch (IOException e) {
            e.printStackTrace();
        }
        Thread.sleep(5000);

        // Reset firebase with initial values
        ref.child(id).child("value").setValue("N");
        ref.child(id).child("training").setValue("N");
        ref.child(id).child("prediction").setValue("F");

        Runner r = new Runner(ref, id);
        r.train();
        r.saveTraining();
        ref.child(id).child("id").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.exists()) {
                    ref.child(id).child("value").setValue(r.predict());
                }
            }
            @Override
            public void onCancelled(FirebaseError firebaseError) {
                System.out.println("The read failed: " + firebaseError.getMessage());
            }
        });
         // ref.child(id).child("id").addValueEventListener(r);
        while (true) ;
    }
}