 package ex;

public class Q2

{

  public static void main(String args[])

  {

      int t1=0,t2=0,t3=0,t4=0,count=0;

      Q2Demo q= new Q2Demo();

      if(q.add(1,0)==1)

      {

		 t1=1;

      }

      if(q.add(95,47)==142)

      {

		 t2=1;

      }

      if(q.add(79,89)==168)

      {

		 t3=1;

      }

      if(q.add(597,16849)==17446)

     {

		 t4=1;

      } 

     if (t1==1)

     {

        System.out.println("Test1 (1 0) is passed");

		count++;
	 }

     else

     {

         System.out.println("Test1 (1 0) is failed");

     }

     if (t2==1)

     {

         System.out.println("Test2 (95 47) is passed");
		 count++;

     }

     else

     {

         System.out.println("Test2 (95 47) is failed");
     }

     if (t3==1)

     {

         System.out.println("Test3 (79 89) is passed");
	     count++;

     } 

     else

     {

         System.out.println("Test3 (79 89) is failed");

     }

     if (t4==1)

     {		  

         System.out.println("Test4 (597 16849) is passed");

		 count++;
	 } 

     else

     {

        System.out.println("Test4 (597 16849) is failed");

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