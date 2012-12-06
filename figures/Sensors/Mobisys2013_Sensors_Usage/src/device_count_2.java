import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;

public class device_count_2
{
	public static void main(String args[])
	{
		
		ArrayList array = new ArrayList();
			
			
			Multimap<String, String> map_sensor_app = ArrayListMultimap.create();
			Multimap<String, String> map_sensor_app_final = ArrayListMultimap.create();
				
		FileInputStream fstream;
		
		 Set devices= new HashSet();
				
		try{
		
			fstream = new FileInputStream("/home/sonali/Desktop/sensors_info");
			
			FileWriter write_stream = new FileWriter("/home/sonali/Desktop/sensors.csv");
			  BufferedWriter out = new BufferedWriter(write_stream);
		
	
	 DataInputStream in = new DataInputStream(fstream);
	  BufferedReader br = new BufferedReader(new InputStreamReader(in));
	  String strLine;
	  
	  
	  while ((strLine = br.readLine()) != null)   {
		  if(strLine.contains("SensorInfo"))
		  { 
			  device_sensor_field f = new device_sensor_field();
			  String toWrite="";
			  

		
		String delims = "[ ]+";
			  String[] tokens = strLine.split(delims); 
			  
			  
			  String deviceName=tokens[0].substring(0, 40); //Device name
			  toWrite+=deviceName+",";
			  //System.out.println(tokens[0]);
			  System.out.println(tokens[0].substring(tokens[0].length()-10, tokens[0].length()));
			  
			  
			 
			  
			  String sensorName= tokens[7]+tokens[8]+tokens[9];
			  String delims2 = ",";
			  String[] tokens2 = sensorName.split(delims2); 
			  toWrite+=tokens2[0]+",";  //SensorName
			  
			  
			 
			   for(int i=0;i<tokens.length;i++)
			   {
				   
				   //System.out.println(tokens[i]);
				   if(tokens[i].contains("Uid"))
					   //System.out.println(tokens[i]);
				   {
					   String uidString=tokens[i];
					   String delims1 = ":";
					   String[] tokens_uid = uidString.split(delims1); 
					          // System.out.println(tokens_uid[tokens_uid.length-1]);
					   
					  // for(int j=0;i<tokens_uid.length;i++)
						//   System.out.println(tokens_uid[j]);
					   
					   String uid_extra=tokens_uid[tokens_uid.length-1];
					   //String snapshotId=tokens_uid[tokens_uid.length-3];
					  // System.out.println(snapshotId);
					   uid_extra=uid_extra.substring(0, uid_extra.length()-1);
					   devices.add(tokens[0].substring(0, 40));
					  //ystem.out.println(uid_extra);
					 toWrite+=uid_extra;
					
					 
					 f.uid= tokens[0].substring(0, 40)+uid_extra;
					 f.sensor=sensorName;
					 f.device=deviceName;
					 map_sensor_app.put(tokens[0].substring(0, 40), uid_extra);
					 array.add(f);
					
					   
					   out.write(toWrite);
					   out.write("\n");
				   
				   }
			   }
			
			    
			    
		  }

	  
		}
	  
	  br.close();
	  fstream.close();
	  out.close();
	  
	  
	  ///Sensing Apps
	  
	  
	  Set<String> keys= map_sensor_app.keySet();
		
		Iterator<String> it_sensor = keys.iterator();
		  
		  while(it_sensor.hasNext())
		  {
			  String str= (String)it_sensor.next(); //key
			  //System.out.println(str);
			  Collection<String> values=map_sensor_app.get(str);
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
				  map_sensor_app_final.put(str, (String)it2.next());
				  //values1.add((String)it1.next());
			  }
			  
			  
			  
		  }
	  
		  FileWriter write_stream2 = new FileWriter("/home/sonali/Desktop/sensors_sensor_apps.csv");
		  BufferedWriter out2 = new BufferedWriter(write_stream2);
		  
		  Set keySet2 = map_sensor_app_final.keySet();
		    Iterator keyIterator2 = keySet2.iterator();
		    while (keyIterator2.hasNext() ) {
		        String key = (String) keyIterator2.next();
		       
		        Collection <String> values = map_sensor_app_final.get( key );
		        //values.s
		       System.out.println(key+","+"No of SensorApps:"+values.size());
		        out2.write(key);
		        out2.write(",");
		        Integer size=(Integer)values.size();
		        out2.write(size.toString());
		        out2.write("\n");
		       
		        
		    }  
		  
	  out2.close();
	  
	  ///
	  
	  
	  
	 
	  

	  Set s = new HashSet();
	  
	  
	  for(int i=0;i<array.size();i++)
	  {
		  device_sensor_field d = (device_sensor_field)array.get(i);
		 // System.out.println(d.sensor);
		  s.add(d.sensor);
		 
	  }
		
	
	  Iterator it = s.iterator();
	  
	  while(it.hasNext())
	  {
		  String str= (String)it.next();
		  //System.out.println(str);
		  
	  }
	 // array.
	  
	  
	 Set acc= new HashSet();
	 Set gps= new HashSet();
	 Set prox= new HashSet();
	 Set mag= new HashSet();
	 Set light= new HashSet();
	 Set gyro= new HashSet();
	 
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
	 
	 
	/*(System.out.println("devices using acc "+ acc.size()) ;
	System.out.println("devices using mag"+ mag.size()) ;
	System.out.println("devices using gps "+ gps.size()) ;
	System.out.println("devices using gyro "+ gyro.size()) ;
	System.out.println("devices using prox"+ prox.size()) ;
	System.out.println("devices using light "+ light.size()) ;
	
	System.out.println("Unique devices using sensors" + devices.size());*/
	
	fstream = new FileInputStream("/home/sonali/Desktop/sensors_info");
	
	FileWriter write_stream1 = new FileWriter("/home/sonali/Desktop/sensors_data.csv");
	  BufferedWriter out1 = new BufferedWriter(write_stream1);
	  
	  out1.write("Accelerometer,"+acc.size()+"\n");
	  out1.write("Magnetometer,"+mag.size()+"\n");
	  out1.write("GPS,"+gps.size()+"\n");
	  out1.write("Gyroscope,"+gyro.size()+"\n");
	  out1.write("Proximity,"+prox.size()+"\n");
	  out1.write("Light,"+light.size()+"\n");
	  out1.write("Unique,"+devices.size()+"\n");
	  
	  out1.close();
		}	
		
		catch(Exception e)
		{
			//System.out.println("Exception");
			e.printStackTrace();
		}
		
		 
		
		 

	}
}