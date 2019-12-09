/*
 * Conversions
 * Farai Gandiya
 * Practicing with Java's mathematical operations
 */

import java.util.Scanner;
import java.lang.Math;

public class Conversions{
  public static void main(String[] args){
    
    Scanner sc = new Scanner(System.in);
    System.out.println("Let's do some cool calculations");
    
    //Celcius to Fahrenheit
    System.out.println("Lets start with converting Celcius into Farheneit.");
    System.out.println("Type a temperature in Celcius");
    
    double celcius = sc.nextDouble();
    double fahrenheit = (9 * celcius / 5) + 32;
    System.out.println(celcius + " degrees Celcius in Fahrenheit is " + fahrenheit + " degrees Fahrenheit");
    
    //Volume and Area of sphere
    System.out.println("Let's find the surface area and volume of a sphere");
    System.out.println("Type the radius of the sphere");
    
    double radius = sc.nextDouble();
    double area = Math.PI * Math.pow(radius,2);
    double volume = area * radius *(4/3);
    System.out.println("The sphere with radius " + radius + " has area " + area + " and volume " + volume);
    
    //Distance between two points
    System.out.println("\nMoving on, let's find the distance between two points");
    System.out.println("Type in two points where each coordinate is separated with a space like X1 Y1 X2 Y2");
    
    double X1 = sc.nextDouble();
    double Y1 = sc.nextDouble();
    double X2 = sc.nextDouble();
    double Y2 = sc.nextDouble();
    double xPart = Math.pow((X2-X1), 2);
    double yPart = Math.pow((Y2-Y1), 2);
    double distance = Math.sqrt(xPart + yPart);
    
    System.out.println("The Distance between two points is " + distance);
    
    //Windchill
    System.out.println("It's cold outside! Let's calculate the windchill");
    System.out.println("Type the temperature followed by the wind speed");
    
    double temperature = sc.nextDouble();
    double windspeed = sc.nextDouble();
    double windchill = 35.74 + (0.6215 * temperature) - (35.75 * Math.pow(windspeed,0.16)) + (0.4275 * Math.pow(windspeed,0.16) * temperature);
    System.out.println("The windchill is " + windchill);
    
    //Tablespoons to Buttloads (https://en.wiktionary.org/wiki/buttload)
    System.out.println("For the lols, let's turn buttloads into teaspoons!");
    System.out.println("Type the number of buttloads you have");
    
    double buttloads = sc.nextDouble();
    double teaspoons = buttloads * 126 * 128 * 2;//A buttload is 126 gal. A gal is 128fl oz. A fl oz. is 2tbsps
    
    System.out.println(buttloads + " buttloads is " + teaspoons + " teaspoons");
    
    
  }
}