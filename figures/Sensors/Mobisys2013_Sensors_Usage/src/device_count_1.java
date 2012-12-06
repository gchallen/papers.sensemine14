import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;



public class device_count_1
{
	
	static String TAG="parse";
	
	public static void main(String args[])
	{
		
				
			FileInputStream fstream;
			
			
			try{
			
				fstream = new FileInputStream("/home/sonali/Desktop/data.out");
				
				FileWriter write_stream = new FileWriter("/home/sonali/Desktop/sensors_info");
				  BufferedWriter out = new BufferedWriter(write_stream);
			
		
		
		 DataInputStream in = new DataInputStream(fstream);
		  BufferedReader br = new BufferedReader(new InputStreamReader(in));
		  String strLine;
		  
		  while ((strLine = br.readLine()) != null)   {
			  // Print the content on the console
			  if(strLine.contains("SensorInfo")&& !strLine.contains("GPS"))
			  { 
				  out.write(strLine);
				  out.write("\n");
			     //System.out.println (strLine);
			     
			  }
			  //count++;
			  //if (count>100)
				//  break;
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