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

public class Accurate_Sensing_Apps_1_New_Data
{
	public static void main(String args[])
	{
		System.out.println("latest file");
		//FileInputStream fstream_twenty;
		Map<String,String> map=new HashMap<String, String>();
		
		Multimap<String, String> map_sensor_app = ArrayListMultimap.create();
		Multimap<String, String> map_sensor_app_final = ArrayListMultimap.create();
		Multimap<String, String> sensor_type = ArrayListMultimap.create();
		Multimap<String, String> sensor_type_final = ArrayListMultimap.create();
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
					 
					  
					  String sensorName= tokens[7]+tokens[8]+tokens[9];
					  String delims2 = ",";
					  String[] tokens2 = sensorName.split(delims2); 
					  String sensor=tokens2[0];
					  
					  
					 
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
							  if(app!=null){
								  if(app.contains("maps"))
									  {map_sensor_app.put(deviceName,"com.google.android.apps.maps");
									  sensor_type.put("com.google.android.apps.maps", sensor);
									  }
								  else if 
								  (app.contains("amazon"))
									  {map_sensor_app.put(deviceName,"com.amazon");
									  sensor_type.put("com.amazon", sensor);
									  }
								  else
							   {map_sensor_app.put(deviceName, app);
								  sensor_type.put(app, sensor);}
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
			  
				}
			  
			
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
				  
				  
				  Set<String> keys_sensor= sensor_type.keySet();
					
					Iterator<String> it_sensor_type = keys_sensor.iterator();
					  
					  while(it_sensor_type.hasNext())
					  {
						  String str= (String)it_sensor_type.next(); //key
						  //System.out.println(str);
						  Collection<String> values=sensor_type.get(str);
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
							  sensor_type_final.put(str, (String)it2.next());
							  //values1.add((String)it1.next());
						  }
						  
						  
						  
					  }	  
				  
				  
				  
			/*	  Set<String> keys_acc= map_acc_app.keySet();
					
					Iterator<String> it_sensor_acc = keys_acc.iterator();
					  
					  while(it_sensor_acc.hasNext())
					  {
						  String str= (String)it_sensor_acc.next(); //key
						  //System.out.println(str);
						  Collection<String> values=map_acc_app.get(str);
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
							  map_acc_app_final.put(str, (String)it2.next());
							  //values1.add((String)it1.next());
						  }
						  
						  
						  
					  }
					  */
					  
				  
				  
				  
				  FileWriter write_stream2 = new FileWriter("/home/sonali/Desktop/sensors_sensor_apps_NEW_DATA.csv");
				  BufferedWriter out2 = new BufferedWriter(write_stream2);
				  
				  Set keySet2 = map_sensor_app_final.keySet();
				    Iterator keyIterator2 = keySet2.iterator();
				    while (keyIterator2.hasNext() ) {
				        String key = (String) keyIterator2.next();
				       
				        Collection <String> values = map_sensor_app_final.get( key );
				        //values.s
				       //System.out.println(key+","+"No of SensorApps:"+values.size());
				        out2.write(key);
				       out2.write(",");
				        Integer size=(Integer)values.size();
				        out2.write(size.toString());
				        out2.write("\n");
				        
				        Iterator itr = values.iterator(); 
				        while(itr.hasNext()) {
				        popular.add((String)itr.next());
				       // popular_category.add(getCategory((String)itr.next()));
				        	
				        }
				       
				        
				    } 
				    
				  /*  Set keySet2_acc = map_acc_app_final.keySet();
				    Iterator keyIterator2_acc = keySet2_acc.iterator();
				    while (keyIterator2_acc.hasNext() ) {
				        String key = (String) keyIterator2_acc.next();
				       
				        Collection <String> values = map_acc_app_final.get( key );
				        //values.s
				       //System.out.println(key+","+"No of SensorApps:"+values.size());
				        
				        
				        Iterator itr = values.iterator(); 
				        while(itr.hasNext()) {
				        popular_acc.add((String)itr.next());
				        	
				        }
				       
				        
				    }
				    
				    */
				    
				    
			  out2.close();
			  
			  int count=0;
			  
			  Set<String> unique = new HashSet<String>(popular);
			  for (String key : unique) {
			      //System.out.println(key + ": " + Collections.frequency(popular, key));
			      field_class f=new field_class(key,Collections.frequency(popular, key));
			      count=count+Collections.frequency(popular, key);
			      popular_sorted.add(f);
			  }
			  
			  Collections.sort(popular_sorted);
			  
			  /*
			  
			  int count_acc=0;
			  
			  Set<String> unique_acc = new HashSet<String>(popular_acc);
			  for (String key : unique_acc) {
			      //System.out.println(key + ": " + Collections.frequency(popular, key));
			      field_class f=new field_class(key,Collections.frequency(popular_acc, key));
			      count_acc=count_acc+Collections.frequency(popular_acc, key);
			      popular_sorted_acc.add(f);
			  }
			  
			  Collections.sort(popular_sorted_acc);
			  */
			 
			
			  
			
			
			for(int i=0;i<popular_sorted.size();i++)  
			{
				//System.out.println(popular_sorted.get(i).pkg+":"+popular_sorted.get(i).freq;
				String s=popular_sorted.get(i).pkg;
				//if((s!=null)&&(!s.contains("amazon"))&&(!s.contains("com.google.android.apps.maps")))
					unique_app.add(s);
			
			
			}
			
			for(int i=0;i<unique_app.size();i++)
			{
				//System.out.println(unique_app.get(i)+",Category:"+getCategory(unique_app.get(i)));
				category.add(getCategory(unique_app.get(i)));
			}
		
			System.out.println("---------------------------------------");
			 Set<String> unique_cat = new HashSet<String>(category);
			  for (String key : unique_cat) {
			      System.out.println(key + ": " + Collections.frequency(category, key));
			     // field_class f=new field_class(key,Collections.frequency(popular_acc, key));
			      //count_acc=count_acc+Collections.frequency(popular_acc, key);
			      //popular_sorted_acc.add(f);
			  }
			  
			  //Collections.sort(popular_sorted_acc);
			
			
			//popular_sorted.re
			
			//System.out.println("total instances of all:"+count);
			
			  System.out.println("-------------------------------------------");
			
			for(int i=0;i<popular_sorted.size();i++)  
			{
				System.out.println("App:"+popular_sorted.get(i).pkg+":"+popular_sorted.get(i).freq);
				 Collection <String> values = sensor_type_final.get(popular_sorted.get(i).pkg);
				 Iterator itr = values.iterator(); 
			        while(itr.hasNext()) {
			        System.out.print(itr.next()+",");
			        	
			        }
			        System.out.print("\n");
				
			}
	
		
		} 
	
	catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	public static String getCategory(String key)
	{
		try{
			String url="https://play.google.com/store/apps/details?id="+key;
			String url1="https://play.google.com/store/apps/details?id="+key;
			//System.out.println(url1);
			/*
				if (key.contains("amazon"))
					url="https://play.google.com/store/apps/details?id=com.amazon.windowshop";
				else 
					if (key.contains("firefox"))
						url="https://play.google.com/store/apps/details?id=com.mozilla.firefox";
			*/
							
				
		Document doc = Jsoup.connect(url1).get();
		Elements links = doc.select("a");
		
		for (Element link:links){

		String text = doc.body().text(); // "An example link"
		String linkHref = link.attr("href"); // "http://example.com/"
		String linkText = link.text(); // "example""

		String linkOuterH = link.outerHtml(); 
		    // "<a href="http://example.com"><b>example</b></a>"
		String linkInnerH = link.html(); // "<b>example</b>"
		
		if(linkOuterH.contains("category"))
		//System.out.println(linkInnerH);
			return linkInnerH;
		}
	}
	
	catch(Exception e)
	{
		//System.out.println(e.getMessage());
	}
		
		return "";
	
}
}