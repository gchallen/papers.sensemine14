import java.util.Comparator;

public class field_class implements Comparable<field_class>
{
	String pkg;
	int freq;
	
	public field_class(String key,int freq1)
	{
		pkg=key;
		freq=freq1;
		
	}
	
	public int compareTo(field_class o1) {
	  
		if(o1.freq<freq)
			return -1;
		else
			if(o1.freq==freq)
				return 0;
			else
				if(o1.freq>freq)
					return 1;
		return 0;
		
	}
}