/* JTypes
 * #All about thos types
 * Showing the various data types in Java
 * Farai Gandiya
*/

public class JTypes{
  public static void main(String[] args){
  
    //Bytes are whole numbers between -128 and 127. They use one byte of memory

    System.out.println("Let's talk about bytes!");
    byte byte1 = -12;
    byte byte2 = 106;
    System.out.println("The first byte is " + byte1);
    System.out.println("The second byte is " + byte2);
    
    //shorts are whole numbers between -32768 and 32767. They use 2 bytes of memory
    
    System.out.println("\nLet's talk about shorts!");
    short shorty1 = -1130;
    short shorty2 = 6545;
    System.out.println("The first short is " + shorty1);
    System.out.println("The second short is " + shorty2);    
    
    //ints are whole numbers between -2^31 and 2^31-1. These take up 4 bytes of memory
    
    System.out.println("\nLet's talk about ints!");
    int inty1 = 1000000000;
    int inty2 = -43234313;
    System.out.println("The first int is " + inty1);
    System.out.println("The second int is " + inty2);  
    
    //longs are whole numbers between -2^63 and 2^63 -1. These take up 8 bytes of memory
    //Great for storing Zimbabwe Dollars or other really big numbers.

    System.out.println("\nLet's talk about longs!");
    long longjohn1 = 1000000000000L;//Always add the L at the end of a long
    long longjohn2 = -432343654232324333L;
    System.out.println("The first long is " + longjohn1);
    System.out.println("The second long is " + longjohn2);
    
    //Floats are "decimal" numbers between 2^-149 to (2-2^-23)*2^127. They use 4 bytes of memory
    //You should never use because of it's lack of precision unless you have a really good reason
    
    System.out.println("\nLet's move onto floats!");
    float floaty1 = 127.973377662646f; //Always add the f after a float
    float floaty2 = -1333.332277636362f;
    
    //Notice how the whole number isn't shown, even though we typed it
    System.out.println("The first float is " + floaty1);//127.97338 
    System.out.println("The second float is " + floaty2);//-1333.3323 
    
    //DOubles are "decimal" numbers between 2^-1074 and (2-2^52)*2^1023. They use 8 bits of memory
    //These are more accurate than floats
    
    System.out.println("\nLet's talk about doubles");
    
    double dub1 = 127.973377662646;
    double dub2 = -1333.332277636362;
    
    //Notice how unlinke floats, the whole number is shown
    System.out.println("The first double is " +  dub1);
    System.out.println("The first double is " +  dub2);
    
    //Booleans are a value that is either true or false
    //These will be used...ALOT!
    //You don't always have to set them to true or false. An inline evaluation would work
    
    System.out.println("\nLet's talk about booleans!");
    
    Boolean boo = 3<2; //false
    Boolean hoo = 2<3; //true
    Boolean bool1 = false;
    Boolean bool2 = true;
    
    System.out.println("3<2 is " +  boo);
    System.out.println("2<3 is " +  hoo);    
    System.out.println("bool1 is " + bool1);
    System.out.println("bool2 is " + bool2);
    
    //chars are is a 2 byte representation of a unicode character
    System.out.println("\nLet's talk about chars!");
    
    char A = 'A'; //single quotes are important!
    char q = 98; //supports all ASCII codes
    char pi = '\u03C0'; //for unicode, use \\u followed by the code
    char snowman = '\u2603';
    
    //Some of these will print depending on the suported font
    //? means it can't
    System.out.println("This is " + A);//A
    System.out.println("65 is the ASCII code for " + q);//x
    System.out.println("U R A QT" + pi);//pi symbol
    System.out.println("Do you wanna build a" + snowman + "?");//Little Snowman
    
    //Strings are a squence of characters and number, even unicode and hex codes!
    System.out.println("\nLet's talk about strings!");
    
    String cheese = "I like myself a big block of cheese";
    String fish = "My favorite fish is Surstr\u00f6ming";//uu00d6 is umlat
    
    System.out.println(cheese);
    System.out.println(fish);
    
    
  }
}