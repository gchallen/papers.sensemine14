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

public class Unique_devices_excluding_system_new_data
{
	public static void main(String args[])
	{
		System.out.println("latest file!!");
		//FileInputStream fstream_twenty;
		Map<String,String> map=new HashMap<String, String>();
		
		Multimap<String, String> map_sensor_app = ArrayListMultimap.create();
		Multimap<String, String> map_sensor_app_final = ArrayListMultimap.create();
		Multimap<String, String> sensor_type = ArrayListMultimap.create();
		Multimap<String, String> sensor_type_final = ArrayListMultimap.create();
		
		Multimap<String, String> sensor_device_regular = ArrayListMultimap.create();
		Multimap<String, String> sensor_device_regular_final = ArrayListMultimap.create();
		//Multimap<String, String> map_acc_app = ArrayListMultimap.create();
		//Multimap<String, String> map_acc_app_final= ArrayListMultimap.create();
		ArrayList <String> popular= new ArrayList<String>();
		ArrayList <field_class> popular_sorted= new ArrayList<field_class>();
		//ArrayList <String> popular_acc= new ArrayList<String>();
		ArrayList <String> unique_app= new ArrayList<String>();
		ArrayList <String> category= new ArrayList<String>();
		
		
		ArrayList <field_class> popular_sorted_acc= new ArrayList<field_class>();
		
		 File folder = new File("/home/sonali/Desktop/TopTwentyNewData");
			
			File[] listOfFiles = folder.listFiles();
		
		try {
			
			for (int k = 0; k < listOfFiles.length; k++) {
				
				
				
				System.out.println("First Set:"+listOfFiles[k].getName());
		
			FileInputStream fstream_twenty = new FileInputStream(listOfFiles[k]);
			
			//FileInputStream fstream_twenty = new FileInputStream("/home/sonali/Desktop/topTwentyPreProcessing.out");
			DataInputStream in = new DataInputStream(fstream_twenty);
			  BufferedReader br = new BufferedReader(new InputStreamReader(in));
			  String strLine;
			  
			
			
			  while ((strLine = br.readLine()) != null)   {
				  // Print the content on the console
				  
				  String delims = "\\s+";
				  String[] tokens = strLine.split(delims); 
				  
				  String device=tokens[0].substring(0,40);

				  String UID="";
				  String UidName="";
				  String snapshotId="";
				  
				  for(int i=0;i<tokens.length;i++)
				  {
					 
					  
					  if(tokens[i].contains("UID"))
						  UID=tokens[i+1].substring(0,tokens[i+1].length()-1);
						 
						
					  
					  if(tokens[i].contains("UidName"))
						  UidName=tokens[i+1].substring(0,tokens[i+1].length()-1);
					  
					  if(tokens[i].contains("SnapshotId"))
					  {
						  String delims1 = ":|,";
						  String[] tokens1 = tokens[i].split(delims1); 
						  snapshotId=tokens1[1];
						 
						  
					  }
					  
				  }
					 
				 // System.out.println(device+","+UID+","+UidName+","+snapshotId);
				  map.put(device+UID+snapshotId, UidName);
				  
				  }
			  
			}
			  
			  System.out.println("map created!");
			
			
			///////////Sensor Part/////////////////
			
			  Set acc= new HashSet();
				 Set gps= new HashSet();
				 Set prox= new HashSet();
				 Set mag= new HashSet();
				 Set light= new HashSet();
				 Set gyro= new HashSet();
				 
				 Set devices= new HashSet();
				 
				 ArrayList<device_sensor_field> array = new ArrayList<device_sensor_field>();	 
			  
			
			  File folder_new = new File("/home/sonali/Desktop/New_Data");
				
				File[] listOfFiles_new = folder_new.listFiles();
				
				for (int k = 0; k < listOfFiles_new.length; k++) {
					
					
					
					System.out.println("Second set(Final!):"+listOfFiles_new[k].getName());
			
				FileInputStream fstream1 = new FileInputStream(listOfFiles_new[k]);
			  
			  //FileInputStream fstream1 = new FileInputStream("/home/sonali/Desktop/sensors_info");
			  DataInputStream in1 = new DataInputStream(fstream1);
			  BufferedReader br1 = new BufferedReader(new InputStreamReader(in1));
			  String strLine1;
			  
			  

			  while ((strLine1 = br1.readLine()) != null)   {
				  if(strLine1.contains("SensorInfo")&& !strLine1.contains("GPS"))
				  { 
					 // device_sensor_field f = new device_sensor_field();
					  //String toWrite="";
					  

				
				String delims = "[ ]+";
					  String[] tokens = strLine1.split(delims); 
					  
					  
					  String deviceName=tokens[0].substring(0, 40); //Device name
					 // toWrite+=deviceName+",";;
					 devices.add(deviceName);
					  
					  String sensorName= tokens[7]+tokens[8]+tokens[9];
					  String delims2 = ",";
					  String[] tokens2 = sensorName.split(delims2); 
					
					 String sensor=tokens2[0];
					  
					 sensor_device_regular.put(deviceName,tokens[0].substring(tokens[0].length()-10, tokens[0].length()));
					 
					   for(int i=0;i<tokens.length;i++)
					   {
						   
						   //System.out.println(tokens[i]);
						   if(tokens[i].contains("Uid"))
							   //System.out.println(tokens[i]);
						   {
							   String uidString=tokens[i];
							  // System.out.println(uidString);
							   String delims1 = ":|,";
							   String[] tokens_uid = uidString.split(delims1); 
							          // System.out.println(tokens_uid[tokens_uid.length-1]);
							   
							  // System.out.println(tokens_uid.length);
							   
							  //for(int j=0;j<tokens_uid.length;j++)
								//  System.out.println(tokens_uid[j]);
							   
							   String uid_extra=tokens_uid[tokens_uid.length-1];
							   String snapshotId=tokens_uid[tokens_uid.length-3];
							  // System.out.println(snapshotId);
							   uid_extra=uid_extra.substring(0, uid_extra.length()-1);
							  // System.out.println(deviceName+uid_extra+"|"+snapshotId);
							   String key= deviceName+uid_extra+snapshotId;
							   String app=map.get(key);
							   
							   device_sensor_field f= new device_sensor_field();
								  f.sensor=sensor;
								  f.device=deviceName;
								  f.uid="uid";
							   
							  if(app!=null){
								  if(app.contains("maps"))
									  {map_sensor_app.put(deviceName,"com.google.android.apps.maps");
									  sensor_type.put("com.google.android.apps.maps", sensor);
									  array.add(f);
									  }
								  else if 
								  (app.contains("amazon"))
									  {map_sensor_app.put(deviceName,"com.amazon");
									  sensor_type.put("com.amazon", sensor);
									  array.add(f);
									  }
								  else
							   {map_sensor_app.put(deviceName, app);
								  sensor_type.put(app, sensor);
								if(!app.contains("system"))  
								{
									 array.add(f);
								}
							   
							   }
							  }
							   
							   //if(sensor.contains("Accelerometer"))
								  // map_acc_app.put(deviceName,map.get(key));
							   
						   
						   }
					   }
					
					    
					    
				  }

			  
				}
			  
			  br1.close();
			  fstream1.close();
			//  out1.close();
			  
				}//end of for
				
				
					  
					  
					  
					  
				
				
				for(int j=0;j<array.size();j++)
				 {
					 device_sensor_field f = new device_sensor_field();
					 f=(device_sensor_field)array.get(j);
					 if(f.sensor.contains("Accelerometer"))
						 acc.add(f.device);
					 if(f.sensor.contains("Proximity"))
						 prox.add(f.device);
					 if(f.sensor.contains("Gyro"))
						 gyro.add(f.device);
					 if(f.sensor.contains("Light"))
						 light.add(f.device);
					 if(f.sensor.contains("GPS"))
						 gps.add(f.device);
					 if(f.sensor.contains("Magnetic"))
						 mag.add(f.device);
					 
				 }
				 
				 
				System.out.println("devices using acc "+ acc.size()) ;
				System.out.println("devices using mag"+ mag.size()) ;
				System.out.println("devices using gps "+ gps.size()) ;
				System.out.println("devices using gyro "+ gyro.size()) ;
				System.out.println("devices using prox"+ prox.size()) ;
				System.out.println("devices using light "+ light.size()) ;
				
				System.out.println("Unique devices using sensors" + devices.size());
				//System.out.println("No. of devices using sensors regularly="+regular.size());
				
			  
			
				
				
			
	}
	
	catch(Exception e)
	{
		//System.out.println(e.getMessage());
	}
		
		
	
}
}