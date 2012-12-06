import java.io.File;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Scrape_From_Google_Play
{
	public static void main(String args[])
	{
		try{
		//File input = new File("/tmp/input.html");
		//Document doc = Jsoup.parse(input, "UTF-8", "http://example.com/");
			Document doc = Jsoup.connect("https://play.google.com/store/apps/details?id=com.dancingsquirrel.elf").get();
			Elements links = doc.select("a");
			
			for (Element link:links){

			String text = doc.body().text(); // "An example link"
			String linkHref = link.attr("href"); // "http://example.com/"
			String linkText = link.text(); // "example""

			String linkOuterH = link.outerHtml(); 
			    // "<a href="http://example.com"><b>example</b></a>"
			String linkInnerH = link.html(); // "<b>example</b>"
			
			if(linkOuterH.contains("category"))
			System.out.println(linkInnerH);
			}
		}
		catch(Exception e)
		{
			System.out.println(e.getMessage());
		}
	}

}