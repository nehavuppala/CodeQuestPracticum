package ex;
import java.util.Arrays;
public class Q3 
{
   public static void main(String args[])
   {
          int t1=0,t2=0,t3=0,t4=0,count=0;
          Q3Demo q3= new Q3Demo;
          int a1={10,90,78,62,14}
          int aa1={10,14,62,78,90}
          int b1={5,1,9,2,7,6,4,65,3}
          int bb1={1,2,3,4,5,6,7,9,65}
          int c1={84,95,21,6,74,33,27,64,9 }
          int cc1={6,9,21,27,33,64,74,84,95}
          int d1={22,44,77,66,10,99,46,27}
          int d1={10,22,27,44,46,66,77,99}
          if(Arrays.equals(q3.sortArray(a1),aa1))
          {
          	t1=1;
          }	  
          if(Arrays.equals(q3.sortArray(b1),bb1))
          {
          	t2=1;	
          }	
          if(Arrays.equals(q3.sortArray(c1),cc1))
          {
          	t3=1;	
          }	
          if(Arrays.equals(q3.sortArray(d1),dd1))
          {
          	t4=1;	
          }	
if (t1==1)

     {

        System.out.println("Test1 (10,14,62,78,90) is passed");

		count++;
	 }

     else

     {

         System.out.println("Test1 (10,14,62,78,90) is failed");

     }

     if (t2==1)

     {

         System.out.println("Test2 (1 2 3 4 5 6 7 9 65) is passed");
		 count++;

     }

     else

     {

         System.out.println("Test2 (1 2 3 4 5 6 7 9 65) is failed");
     }

     if (t3==1)

     {

         System.out.println("Test3 (6 9 21 27 33 64 74 84 95) is passed");
	     count++;

     } 

     else

     {

         System.out.println("Test3 (6 9 21 27 33 64 74 84 95) is failed");

     }

     if (t4==1)

     {		  

         System.out.println("Test4 (10 22 27 44 46 66 77 99) is passed");

		 count++;
	 } 

     else

     {

        System.out.println("Test4 (10 22 27 44 46 66 77 99) is failed");

     }
    if(count==4)
 {
System.out.println("");		 
System.out.println("Your score is 10");
	 }
	 else 
	 {
System.out.println("");		 
System.out.println("Your score is 0");
	 }
          
            
   }

} 