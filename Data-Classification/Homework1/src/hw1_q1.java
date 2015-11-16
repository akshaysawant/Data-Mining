import java.io.*;
import java.io.FileInputStream;
import java.util.*;


public class hw1_q1 {

	public static void main(String args[])
	{
		String file_name, line, token, data, curr_authors[] = null, curr_pub;
		FileReader file = null;
		BufferedReader reader = null;
		int author_count = 0, venue_count = 0, pub_count = 0;
		int[] auth_data;
		String line_split[];
		
		HashSet authors = new HashSet();
		HashSet venues = new HashSet();
		HashSet pubs = new HashSet();
		//HashSet author_pub = new HashSet();
		//HashSet author_cit = new HashSet();
		Hashtable<String, int[]> authors_data = new Hashtable<String, int[]>();
		
		file_name = args[0];
		
		try 
		{
			file = new FileReader(file_name);
			reader = new BufferedReader(file);
		    
		    while ((line = reader.readLine()) != null)
		    {
		        System.out.println(line);
		        if (line.trim().isEmpty())
		        	continue;
		        else
		        {
		        	line_split = line.split(" ", 2);
		        	token = line_split[0];
		        	data = line_split[1];

		        	if (token.equals("#index"))
		        	{
		        		curr_pub = null;
		        		curr_authors = null;
		        	}
		        	else if (token.equals("#*"))
		        	{
		        		curr_pub = data;
		        		if (!pubs.contains(data))
		        		{
		        			pubs.add(data);
		        			pub_count++;
		        		}
		        	}
		        	else if (token.equals("#@"))
		        	{
		        		curr_authors = data.split(";");
		        		for (String author : curr_authors)
		        		{
		        			if (authors_data.containsKey(author))
		        			{
		        				authors_data.get(author)[0]++;
		        			}
		        			else
		        			{
		        				auth_data = new int[]{1, 0};
		        				authors_data.put(author, auth_data);
		        				author_count++;
		        			}
		        		}
		        	}
		        	else if (token.equals("#c"))
		        	{
		        		if (!venues.contains(data))
		    			{
		        			venues.add(data);
		        			venue_count++;
		    			}
		        	}
		        	else if (token.equals("#%"))
		        	{
		        		for (String author : curr_authors)
		        			authors_data.get(author)[1]++;
		        	}
		        }
		    }
		    
		    System.out.println("Total authors : " + author_count);
		    System.out.println("Total venues : " + venue_count);
		    System.out.println("Total publications : " + pub_count);
		}
		catch (IOException e) 
		{
			e.printStackTrace();
		}
		finally 
		{
			try 
			{
                file.close();
            }
			catch (IOException ex)
			{
                ex.printStackTrace();
			}
		}
	}
}
