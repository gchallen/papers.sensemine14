import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.Set;

import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;

public class apps_per_device_3
{
	public static void main(String args[])
	{
		FileInputStream fstream;
		
		Multimap<String, String> map_device = ArrayListMultimap.create();
	//	Multimap<String, Double> map_percent = ArrayListMultimap.create();
		
		try {
			fstream = new FileInputStream("/home/sonali/Desktop/sensors_sensor_apps_NEW_DATA.csv");
			
			 DataInputStream in = new DataInputStream(fstream);
			  BufferedReader br = new BufferedReader(new InputStreamReader(in));
			  String strLine;
			  while ((strLine = br.readLine()) != null)   {
			  

					String delims = ",";
						  String[] tokens = strLine.split(delims); 
						  
						//  System.out.println(tokens[0]+"|"+tokens[1]);
						  map_device.put(tokens[0], tokens[1]);
				  
			  }
			  
			
			
			
			br.close();
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		try {
			FileInputStream fstream1 = new FileInputStream("/home/sonali/Desktop/sensors_total_apps_NEW_DATA.csv");
			
			 DataInputStream in1 = new DataInputStream(fstream1);
			  BufferedReader br1 = new BufferedReader(new InputStreamReader(in1));
			  String strLine;
			  while ((strLine = br1.readLine()) != null)   {
			  

					String delims = ",";
						  String[] tokens = strLine.split(delims); 
						  
						  System.out.println(tokens[0]+"|"+tokens[1]);
						  map_device.put(tokens[0], tokens[1]);
				  
			  }
			  
			
			
			
			br1.close();
			
			
		
		
		
		FileWriter write_stream1 = new FileWriter("/home/sonali/Desktop/sensors_percentage_NEW_DATA.csv");
		  BufferedWriter out1 = new BufferedWriter(write_stream1);
		  
			Set keySet1 = map_device.keySet();
		    Iterator keyIterator1 = keySet1.iterator();
		    while (keyIterator1.hasNext() ) {
		        String key = (String) keyIterator1.next();
		       
		        Collection <String> values = map_device.get( key );
		        //values.s
		      //  System.out.println(key+","+"No of UserApps:"+values.size());
		        out1.write(key);
		        out1.write(",");
		      
		        Iterator<String> it_col= values.iterator();
		        
		        ArrayList<String > arr = new ArrayList<String>();
		        while(it_col.hasNext())
		        {
		        	arr.add(it_col.next());
		        }
		        
		    Double sens= Double.parseDouble(arr.get(0));
		    Double tot= Double.parseDouble(arr.get(1));
		    Double per = (sens/tot)*100;
		    out1.write(per.toString());
		    out1.write("\n");
		    System.out.println(key+","+per);
		        
		    }
		    
		   
		    
		    out1.close();
		
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
	}
}