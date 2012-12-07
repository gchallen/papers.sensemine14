import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;

public class apps_per_device_2
{
	public static void main(String args[])
	{
		
		Multimap<String, String> map_user_app = ArrayListMultimap.create();
		Multimap<String, String> map_user_app_final = ArrayListMultimap.create();
		 Multimap<String, String> map_system_app = ArrayListMultimap.create();
		 Multimap<String, String> map_system_app_final = ArrayListMultimap.create();
		 Multimap<String, String> map_total_app = ArrayListMultimap.create();
		 Multimap<String, String> map_total_app_final = ArrayListMultimap.create();
		 
		
		 
		FileInputStream fstream;
		
		
		
		  
		  try{
		
			fstream = new FileInputStream("/home/sonali/Desktop/sensors_info_ratio.out");
			
			//FileWriter write_stream = new FileWriter("/home/sonali/Desktop/sensors_user_apps");
			  //BufferedWriter out = new BufferedWriter(write_stream);

			  //out.write("hellooo");
	
	 DataInputStream in = new DataInputStream(fstream);
	  BufferedReader br = new BufferedReader(new InputStreamReader(in));
	  String strLine;
	  
	  while ((strLine = br.readLine()) != null)   {
		  // Print the content on the console
		  
		  String delims = "[ ]+";
		  String[] tokens = strLine.split(delims); 
		  
		  for(int i=0;i<tokens.length;i++)
		  {
			  if(tokens[i].contains("AppName"))
				{
				  //System.out.println("uid:"+tokens[i+3]);
				  map_total_app.put(tokens[0].substring(0,40),tokens[i+1]);
				}
			  
			  if(tokens[i].contains("Uid"))
				  System.out.println(tokens[i+1].substring(0,tokens[i+1].length()-1));
		  }
		  
		  //map_total_app.put(tokens[0].substring(0,40),tokens[i+1]);
		  
		  if(strLine.contains("InstalledUserApp")){
			  
			  
					  
			for(int i=0;i<tokens.length;i++)  
			{
				
				
				if(tokens[i].contains("AppName"))
				{
					map_user_app.put(tokens[0].substring(0,40),tokens[i+1]);
				}
			}
		  }
		  
		  else
			  
			  if(strLine.contains("InstalledSystemApp")){
				  
					for(int i=0;i<tokens.length;i++)  
					{
						if(tokens[i].contains("AppName"))
						{
							map_system_app.put(tokens[0].substring(0,40),tokens[i+1]);
						}
					}
				  }
				   
		     
		  }
		 
	  
	 br.close();
	 in.close();
	 
	// Set keySet = map_user_app.keySet();
	

	Set<String> keys= map_user_app.keySet();
	
	Iterator<String> it = keys.iterator();
	  
	  while(it.hasNext())
	  {
		  String str= (String)it.next(); //key
		  //System.out.println(str);
		  Collection<String> values=map_user_app.get(str);
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
			  map_user_app_final.put(str, (String)it2.next());
			  //values1.add((String)it1.next());
		  }
		  
		  
		  
	  }
		Set<String> keys_sys= map_system_app.keySet();
		
		Iterator<String> it_sys = keys_sys.iterator();
		  
		  while(it_sys.hasNext())
		  {
			  String str= (String)it_sys.next(); //key
			  //System.out.println(str);
			  Collection<String> values=map_system_app.get(str);
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
				  map_system_app_final.put(str, (String)it2.next());
				  //values1.add((String)it1.next());
			  }
			  
			  
			  
		  }
		  
		  Set<String> keys_tot= map_total_app.keySet();
			
			Iterator<String> it_tot = keys_tot.iterator();
			  
			  while(it_tot.hasNext())
			  {
				  String str= (String)it_tot.next(); //key
				  //System.out.println(str);
				  Collection<String> values=map_total_app.get(str);
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
					  map_total_app_final.put(str, (String)it2.next());
					  //values1.add((String)it1.next());
				  }
				  
				  
				  
			  }
			  
			  FileWriter write_stream3 = new FileWriter("/home/sonali/Desktop/sensors_total_apps.csv");
			  BufferedWriter out3 = new BufferedWriter(write_stream3);
		  
			  
			  
			  Set keySet1_tot = map_total_app_final.keySet();
			    Iterator keyIterator1_tot = keySet1_tot.iterator();
			    while (keyIterator1_tot.hasNext() ) {
			        String key = (String) keyIterator1_tot.next();
			       
			        Collection <String> values_tot = map_total_app_final.get( key );
			        //values.s
			        //System.out.println(key+","+"No of total Apps:"+values_tot.size());
			        out3.write(key);
			        out3.write(",");
			        Integer size=(Integer)values_tot.size();
			        out3.write(size.toString());
			        out3.write("\n");
			      /* Iterator<String> it_col= values_sys.iterator();
			        while(it_col.hasNext())
			        {
			        	System.out.println(it_col.next());
			        }
			        System.out.println("-----------------------------------------------------");*/
			        
			    }
		  
		  out3.close();
		  
		  FileWriter write_stream2 = new FileWriter("/home/sonali/Desktop/sensors_system_apps.csv");
		  BufferedWriter out2 = new BufferedWriter(write_stream2);
	  
		  Set keySet1_sys = map_system_app_final.keySet();
		    Iterator keyIterator1_sys = keySet1_sys.iterator();
		    while (keyIterator1_sys.hasNext() ) {
		        String key = (String) keyIterator1_sys.next();
		       
		        Collection <String> values_sys = map_system_app_final.get( key );
		        //values.s
		        //System.out.println(key+","+"No of System Apps:"+values_sys.size());
		        out2.write(key);
		        out2.write(",");
		        Integer size=(Integer)values_sys.size();
		        out2.write(size.toString());
		        out2.write("\n");
		      /* Iterator<String> it_col= values_sys.iterator();
		        while(it_col.hasNext())
		        {
		        	System.out.println(it_col.next());
		        }
		        System.out.println("-----------------------------------------------------");*/
		        
		    }
	  
		out2.close();
		
		
	//	map_user_app.
	  
	  
	  FileWriter write_stream1 = new FileWriter("/home/sonali/Desktop/sensors_user_apps.csv");
	  BufferedWriter out1 = new BufferedWriter(write_stream1);
	  
		Set keySet1 = map_user_app_final.keySet();
	    Iterator keyIterator1 = keySet1.iterator();
	    while (keyIterator1.hasNext() ) {
	        String key = (String) keyIterator1.next();
	       
	        Collection <String> values = map_user_app_final.get( key );
	        //values.s
	      //  System.out.println(key+","+"No of UserApps:"+values.size());
	        out1.write(key);
	        out1.write(",");
	        Integer size=(Integer)values.size();
	        out1.write(size.toString());
	        out1.write("\n");
	       /* Iterator<String> it_col= values.iterator();
	        while(it_col.hasNext())
	        {
	        	System.out.println(it_col.next());
	        }
	        System.out.println("-----------------------------------------------------");*/
	        
	    }
	    
	   // write_stream.close();
	    //out.close();
	    
	    
	    out1.close();
	    
	    
		}
	 
		
		catch(Exception e)
		{
			System.out.println(e.toString());
		}
		
		
	}
}