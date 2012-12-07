import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;

public class Sensors_regular_use
{
	public static void main(String args[])
	{
		System.out.println("latest file!!");
		
		
		Multimap<String, String> sensor_device_regular = ArrayListMultimap.create();
		Multimap<String, String> sensor_device_regular_final = ArrayListMultimap.create();
		
			try{
			
			  File folder_new = new File("/home/sonali/Desktop/New_Data");
				
				File[] listOfFiles_new = folder_new.listFiles();
				
				for (int k = 0; k < listOfFiles_new.length; k++) {
					
					
					
					//System.out.println("Second set(Final!):"+listOfFiles_new[k].getName());
			
				FileInputStream fstream1 = new FileInputStream(listOfFiles_new[k]);
			 
			  DataInputStream in1 = new DataInputStream(fstream1);
			  BufferedReader br1 = new BufferedReader(new InputStreamReader(in1));
			  String strLine1;
			  
			  

			  while ((strLine1 = br1.readLine()) != null)   {
				  if(strLine1.contains("SensorInfo")&& !strLine1.contains("GPS"))
				  { 
					 
				String delims = "[ ]+";
					  String[] tokens = strLine1.split(delims); 
					  
					  
					  String deviceName=tokens[0].substring(0, 40); //Device name
					 
					  
					 sensor_device_regular.put(deviceName,tokens[0].substring(tokens[0].length()-10, tokens[0].length()));
					// System.out.println(deviceName+","+tokens[0].substring(tokens[0].length()-10, tokens[0].length()));
					   
						   }
					   }
					
					    
				
			  
			  br1.close();
			  fstream1.close();
			//  out1.close();
			  
				}//end of for
				
				//System.out.println("End of for loop for second set of files");
				

				  Set<String> keys= sensor_device_regular.keySet();
					
					Iterator<String> it_sensor = keys.iterator();
					  
					  while(it_sensor.hasNext())
					  {
						  String str= (String)it_sensor.next(); //key
						  //System.out.println(str);
						  Collection<String> values=sensor_device_regular.get(str);
						  //map_user_app.removeAll(str);
						  Set<String> values1=new HashSet<String>();
						  
						 		  
						  Iterator<String> it1 = values.iterator();
						  while (it1.hasNext())
						  {
							 // map_user_app.put(str, (String)it1.next());
							  values1.add((String)it1.next());
						  }
						  
						  Iterator<String> it2 = values1.iterator();
						  
						  while (it2.hasNext())
						  {
							  sensor_device_regular_final.put(str, (String)it2.next());
							  //values1.add((String)it1.next());
						  }
						  
						  
						  
					  }
					  
					  ArrayList<String> regular_devices= new ArrayList<String>();
					  

					  Set<String> keys_1= sensor_device_regular_final.keySet();
						
						Iterator<String> it_sensor_1 = keys_1.iterator();
						  
						  while(it_sensor_1.hasNext())
						  {
							  String str= (String)it_sensor_1.next(); //key
							  //System.out.println(str);
							 // System.out.print(str+",");
							  Collection<String> values=sensor_device_regular_final.get(str);
							  //map_user_app.removeAll(str);
							  						 		  
							 /* Iterator<String> it1 = values.iterator();
							  while (it1.hasNext())
							  {
								  System.out.print(it1.next()+",");
								 
							  }
							 System.out.print("\n"); 
							  */
							  if(values.size()==14)
								  regular_devices.add(str);
							  
							  
							  
						  }
					  
					  
				System.out.println("No of devices using sensors regularly:"+regular_devices.size());
				System.out.println("No. of unique devices:"+keys.size());
			
	
	}catch(Exception e){
		System.out.println(e.getMessage());
	}
	
	
	
}
}
