import java.util.Scanner;
import java.lang.Math;

public class Mathical{
  
  public static void main(String[] args){
  
    System.out.println("This is Mathical, where we explore Java's mathamatical operations");
    
    Scanner sc = new Scanner(System.in); 
    
    //+1
    System.out.println("Java can do addition using the '+' operator.");
    System.out.println("For example, type a whole number and I'll add it by one.");
    
    int num1 = sc.nextInt();//Don't forget to use nextInt for ints!
    int sum = num1 + 1;   
    System.out.println(num1 + "+1 is equal to " + sum);
    
    //Kelvins to Celcius
    System.out.println("Java can also do subtraction using the '-' operator.");
    System.out.println("In this example, type a temprature in Kelvin and I will convert it into Celcius.");
    
    double kelvins = sc.nextDouble();     
    //A final prevents the variable from being changed once it has been declared
    //They are declared using visibility, datatypeand variable name in capital as convension  
    final double TEMPCONVERSION = 273.15;
    double celcius = kelvins - TEMPCONVERSION;
    System.out.println(kelvins +"K is " + celcius + " degrees Celcius.");//It looks kinda funny
    
    //Miles to Kilometers
    System.out.println("Java can do multiplication using the '*' operator.");
    System.out.println("For example, type a number in Miles and we will turn it into Kilometers");
    
    double miles = sc.nextDouble();
    final double MILECONVERSION = 1.609344;
    double kilometers = miles * MILECONVERSION;
    System.out.println(miles + " miles is equal to " + kilometers +" kilometers");
    
    //Pounds to Kilograms
    System.out.println("Java can also do division using the '/' operator.");
    System.out.println("For example, type a number in pounds and we'll turn it into kilograms");    
    
    double pounds = sc.nextDouble();
    final double KILOCONVERSION = 0.45359237;
    double kilograms = pounds * KILOCONVERSION;
    
    System.out.println(pounds + "lbs is equal to " + kilograms + "kgs");
    
    //Other Java Math operations
    System.out.println("Java also has the Math library, java.lang.Math, that does other stuff");
    System.out.println("Type two whole numbers and a decimal number, separated by spaces");
    int basenum = sc.nextInt();
    int secnum = sc.nextInt();
    double decimecy = sc.nextDouble();
    
    double power = Math.pow(basenum, 2);//pow raises the first argument to the second power
    double sqrt = Math.sqrt(basenum); //sqrt returns the square root of a number
    double logb10 = Math.log10(basenum);//log10 returns the base10 log of a number
    int maxinum = Math.max(basenum, secnum); //max returns the largest of two numbers
    int mininum = Math.min(basenum, secnum);//min returns the smallest of two numbers
    double sin = Math.sin(decimecy);
    
    System.out.println(basenum + " to the power of 2 is " + power);
    System.out.println("The Square Root of " + basenum + " is " + sqrt);
    System.out.println(basenum + "to the log base 10 is " + logb10);
    System.out.println(maxinum +" is bigger than " + mininum);
    System.out.println(sin + " is the sin of " + decimecy);
   
    sc.close();
    
  }

}