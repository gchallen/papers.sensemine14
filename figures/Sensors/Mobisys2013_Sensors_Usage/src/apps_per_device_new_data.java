import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;



public class apps_per_device_new_data
{
	
	static String TAG="parse";
	
	public static void main(String args[])
	{
		File folder = new File("/home/sonali/Desktop/ALL");
		
		File[] listOfFiles = folder.listFiles();
				
			//FileInputStream fstream;
			
			
			try{
				
				for (int i = 0; i < listOfFiles.length; i++) {
					
					
					
					System.out.println(listOfFiles[i].getName());
			
				FileInputStream fstream = new FileInputStream(listOfFiles[i]);
				
				FileWriter write_stream = new FileWriter("/home/sonali/Desktop/New_Data_Ratio/sensors_info_ratio_new_data"+i+".out");
				
		
				  BufferedWriter out = new BufferedWriter(write_stream);
			
		
		
		 DataInputStream in = new DataInputStream(fstream);
		  BufferedReader br = new BufferedReader(new InputStreamReader(in));
		  String strLine;
		  
		  
		  
		  while ((strLine = br.readLine()) != null)   {
			
			  if(strLine.contains("PhoneLabSystemAnalysis-Snapshot")&&(strLine.contains("InstalledUserApp")|| strLine.contains("InstalledSystemApp")))
			  { 
				  out.write(strLine);
				  out.write("\n");
			       //System.out.println (strLine);
			     
			  }
			  
			  }
		  
		  //br.close();
		  //fstream.close();
		 // write_stream.close();
		  //out.close();
				}
		  
			}
			
			catch(Exception e)
			{
				System.out.println(e.toString());
			}
	}
}