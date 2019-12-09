//Farai Gandiya
//LoopyChoices
//Learning how to work with for, while, if and switch statements

import java.util.*;
import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LoopyChoices{
  public static void main(String[] args) throws IOException{
    
    Scanner sc = new Scanner(System.in);
    
    //Syrcuse Number
    System.out.println("Let's do the Syrcuse Number");
    
    System.out.println("Type a number");
    long x = sc.nextLong();
    String sequence = x + ",";
    
    while(x != 1){
      if(x%2 == 0){
        x /= 2;
      }
      else{
        x = (3*x) + 1;
      }
      sequence += x + ",";
    }
    sc.close();

    Scanner sc2 = new Scanner(System.in);
    System.out.println("The Sycrause sequence for " + x + " is " + sequence);
    
    //LF Converter
    System.out.println("\nLet's learn some LF language!");
    System.out.println("Give me a file with words in it: ");
    
    String filename = sc2.nextLine();
    File file = new File(filename);
    Scanner input = new Scanner(file);

    System.out.println("Where do you want your new lf language to be? End the file name in .txt");
    String output = sc2.nextLine();
    
    PrintWriter outfile = new PrintWriter(output);
    String results = "";
    
    while(input.hasNextLine()){
      String word = input.next();
      Pattern vowels = Pattern.compile("a|A|e|E|i|I|o|O|u|U");//creates a patern
      Matcher m = vowels.matcher(word);//finds patterns of the expression vowels in word
      boolean hasVowel = m.find();
      if(hasVowel){
        int start = m.start();//gets starting index of pattern m
        String[] toElf = word.split("");
        toElf[start] = toElf[start] + "lf" + toElf[start];
        word = String.join("", toElf);
      }
      results += " " + word;
    }
    outfile.println(results);
    outfile.close();
    input.close();
    sc2.close();

    //Date Validation
    Scanner sc3 = new Scanner(System.in);
    System.out.println("Let's print some dates!");
    System.out.println("Input a date in the format dd/MM/yyyy like 29/05/1995");
    String date = sc3.nextLine();
    String[] dateArr = date.split("/");
    int day = Integer.parseInt(dateArr[0]);
    int month = Integer.parseInt(dateArr[1]);
    int year = Integer.parseInt(dateArr[2]);
    boolean isLeapYear = (year%400 == 0) || ((year%100) != 0 && (year%4 == 0));
    switch(month){
      case 1:
      case 3:
      case 5:
      case 7:
      case 8:
      case 10:
      case 12:
        if(day < 32){
          System.out.println("This date is legit");
        }
        else{
          System.out.println("This date is not legal");
        }
        break;
      case 4:
      case 6:
      case 9:
      case 11:
        if(day < 31){
          System.out.println("This date is legit");
        }
        else{
          System.out.println("This date is not legal");
        }
        break;
      case 2:
      if(isLeapYear){
        if (day < 30){
          System.out.println("This date is legit");
         }
        else{
          System.out.println("This date is not legit");
        }
      }
       else{
        if (day < 29){
          System.out.println("This date is legit");
         }
        else{
          System.out.println("This date not legit");
        }
       }
       break;
      default:
        System.out.println("Congrats! You just made a new month since that doesn't work!");
        break;
    }
    
    sc3.close();

    //I am doing the typical programming interview question FizzBuzz for my extra credit
    //Given a number i of loop n, if i is divisible by 3, print Fizz, if n is divisible by 5 print Buzz
    //If the number is divisible by both 3 and 5, print FizzBuzz. Else print n at point i
    Scanner sc5 = new Scanner(System.in);
    System.out.println("Let's do the enterprise grade FizzBuzz Problem");
    System.out.println("Input a number");
    int n = sc5.nextInt();
    for(int i = 1; i < n + 1; i++){
      if(i % 3 == 0 && i % 5 == 0){
        System.out.println("FizzBuzz");
      }
      else if(i%3 == 0){
        System.out.println("Fizz");    
      }
      else if(i%5 == 0){
        System.out.println("Buzz");
      }
      else{
        System.out.println(i);  
      }
    }
    sc5.close();
    
    Scanner sc4 = new Scanner(System.in);
    System.out.println("Let's get chaotic!");
    System.out.println("Enter the first chaotic value between 0 and 1");    
    double c1 = sc4.nextDouble();
    System.out.println("Enter the second chaotic value between 0 and 1");   
    double c2 = sc4.nextDouble();    
    System.out.println("index   " + c1 + "   " + c2);   
    System.out.println("____________________________");   
    for(int i = 1; i < 11; i++){
      c1 *= 3.9 * (1-c1);
      c2 *= 3.9 * (1-c2);
      String c = String.format("%.6f", c2);
      String b = String.format("%.6f", c1);
      String d = String.format("%3d", i);
      System.out.println(d + "     " +b + "   " + c);    
    }
    sc4.close();
  }
}

