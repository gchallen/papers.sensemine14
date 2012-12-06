import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;



public class device_count_1_new_data
{
	
	static String TAG="parse";
	
	public static void main(String args[])
	{
		File folder = new File("/home/sonali/Desktop/ALL");
		
		File[] listOfFiles = folder.listFiles();
		
		
		for (int i = 0; i < listOfFiles.length; i++) {
			
			
				
			System.out.println(listOfFiles[i].getName());
			
			
			try{
			
				FileInputStream fstream = new FileInputStream(listOfFiles[i]);
				
				FileWriter write_stream = new FileWriter("/home/sonali/Desktop/New_Data/sensors_info_new_data"+i+".out");
				  BufferedWriter out = new BufferedWriter(write_stream);
			
		
		
		 DataInputStream in = new DataInputStream(fstream);
		  BufferedReader br = new BufferedReader(new InputStreamReader(in));
		  String strLine;
		  
		  while ((strLine = br.readLine()) != null)   {
			  // Print the content on the console
			  if(strLine.contains("SensorInfo")&& !strLine.contains("GPS"))
			  { 
				  out.append(strLine);
				  out.append("\n");
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
	
	
	
	}//end of for
	}//end of main
	
}