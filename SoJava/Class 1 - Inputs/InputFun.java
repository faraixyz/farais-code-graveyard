//InputFun.java
//Demonstrating how to take console input

//To use a Java Class, you need to import it before the main clas declaration

import java.util.Scanner;//Allows us to handle console input

public class InputFun{

  public static void main(String[] args){
    
    System.out.println("Let's play around with inputs!");
    
    Scanner sc = new Scanner(System.in);//creates a Scanner that allows us to take console input
    
    String firstSTR = sc.nextLine(); //Allows us to read the line of a file
    
    System.out.println(firstSTR);
    
    System.out.println("Try and type two words and see what happens");
    String secondSTR = sc.next(); //Reads a string up until the first white space
    
    System.out.println("The input is " + secondSTR);
    System.out.println("Strange. I thought you put two words");
    
    String thirsdSTR = sc.next();//If the user typed two words, this will be the second word
    
    System.out.println("The other word you typed is " + thirsdSTR);    
    System.out.println("Goodbye!");
    
    sc.close();//Once we're done, we can close the scanner.
  }
}