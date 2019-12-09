import java.util.*;

public class Loops{
  
  public static void main(String[] args){
  Scanner sc = new Scanner(System.in);
  System.out.println("Let's compute the factorial of a number");
  int n = sc.nextInt();
  long factorial = 1;
  
  for(int i = 1; i < n + 1; i++){
    factorial *= i;
  }
  System.out.println(n + " factorial is equal to " + factorial);
  
  System.out.println("Let's see the difference between i-- and --i");
  
  int j = sc.nextInt();
  String minusJ = "";
  String jMinus = "";
  
  for(int i = j; i > 0; --i){
    minusJ += i + " ";
  }
  for(int i = j; i > 0; i--){
    jMinus += i + " ";
  }
  
  System.out.println("This is what happens if the increment is before " + minusJ);
  System.out.println("This is what happens if the increment is after " + jMinus);
  
  System.out.println("Moving on, let's see what you can do");
  
  int age = sc.nextInt();
  Boolean isVotingYear = sc.nextBoolean();
  Boolean isTeatotaller = sc.nextBoolean();
  if(age > 18 && isVotingYear){
  System.out.println("You can vote this year");
  }
  else if(age < 21 || isTeatotaller){
     System.out.println("No drink for you!");
  }
  else{
     System.out.println("What do you want to drink boss?"):
  }
    Calendar c = new GregorianCalendar;
    int day = calendar.get(Calendar.DAY_OF_WEEK);
    switch(day){
    // Sunday is 0 through Saturday 6
    case 1:
    case 2:
    case 3:
    case 4:
        System.out.println("Today's hours are 7am to 7pn");
        break;
    case 5:
        System.out.println("Today's hours are 7am to 4:30pm");
        break;
    case 6:
    case 0:
        System.out.println("We are closed today.");
    default:
        System.out.println("Is that a new day?");
        break;
    
    }
  sc.close();
  }
}