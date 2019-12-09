//AngryLibs.java
//Let's put out input fun into action! by implementing the totally original AngryLibs

import java.util.Scanner; //Don't forget this!

public class AngryLibs{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    
    System.out.println("Welcome to the totally original Mad Libs where you tell the story");
    
    System.out.println("Enter an adjective:");
    String adjective = sc.nextLine();
      
    System.out.println("Enter an adverb:");
    String adverb = sc.nextLine();

    System.out.println("Enter a verb:");
    String verb = sc.nextLine();
    
    System.out.println("Enter a place:");
    String place = sc.nextLine();
    
    System.out.println("Enter a name:");
    String name = sc.nextLine();
    
    System.out.println("Enter an improper noun. Like cat, country, name:");
    String impnoun = sc.nextLine();
    
    System.out.println("Enter a period of time:");
    String time = sc.nextLine();
    
    System.out.println("Last " + time +  ", I went to " + place + " where I, The Great "
                         + name +" "+adverb + " " + verb + " a " + adjective + " " + impnoun + ".");
  }
}