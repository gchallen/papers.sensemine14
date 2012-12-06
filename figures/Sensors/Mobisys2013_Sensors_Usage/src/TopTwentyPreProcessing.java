import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;

public class TopTwentyPreProcessing
{
	public static void main(String args[])
	{

		
		FileInputStream fstream;
		
		
		try{
		
			fstream = new FileInputStream("/home/sonali/Desktop/data.out");
			
			FileWriter write_stream = new FileWriter("/home/sonali/Desktop/topTwentyPreProcessing.out");
			  BufferedWriter out = new BufferedWriter(write_stream);
		
	
	
	 DataInputStream in = new DataInputStream(fstream);
	  BufferedReader br = new BufferedReader(new InputStreamReader(in));
	  String strLine;
	  
	  
	  
	  while ((strLine = br.readLine()) != null)   {
		
		  if((strLine.contains("UidInfo") )&&(strLine.contains("PhoneLabSystemAnalysis-Snapshot") ))
		  { 
			  out.write(strLine);
			  out.write("\n");
		      // System.out.println (strLine);
		     
		  }
		  
		  }
	  
	  br.close();
	  fstream.close();
	  out.close();
	  
	  
		}
		
		catch(Exception e)
		{
			System.out.println(e.toString());
		}
}
	}
