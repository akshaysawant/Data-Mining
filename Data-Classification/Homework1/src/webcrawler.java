import java.io.*;
import java.net.*;
import org.jsoup.*;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;       
import org.jsoup.nodes.Element;


public class webcrawler {

	static Socket client = null;
	static BufferedReader ipMsg = null;
	static PrintWriter out = null;
	static InputStreamReader isr = null;
	
	public static void main(String args[]) throws IOException
	{
		String username = null, password = null, host = null;
		int port = 80;
		
		username = args[0];
		password = args[1];
		
		host = "cs5700f14.ccs.neu.edu";
		
		try
		{
			InetAddress inet = InetAddress.getByName(host);
			client = new Socket(inet , port);
		
			out = new PrintWriter(client.getOutputStream(), true);
		
			isr = new InputStreamReader(client.getInputStream());
        	ipMsg = new BufferedReader(isr);
        
        	makeHTTPConnection(host, username, password);
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			if (client != null)
				client.close();
		}
	}
	
	static void makeHTTPConnection(String host, String username, String password) throws IOException
	{
		String HTTPmsg = null, loginLink = null, message = null, CRLF = "\r\n", html = null;
		String csrftoken = null, sessionid = null, user_field = null, pass_field = null;
		String csrf_field = null, next_link = null, httpPost = null, action = null, data = null;
		String[] splitMsg = null;
		char[] inPage = null;
		Document doc = null;
		char[] data = null;
		
		html = data.toString();
		loginLink = "/accounts/login/?next=/fakebook/";
		
		HTTPmsg = "GET " + loginLink + " HTTP/1.1" + CRLF;
		httpPost += "Connection: Keep-alive" + CRLF;
		HTTPmsg += "Host: " + host + ":80" + CRLF + CRLF;
		
		
		out.write(HTTPmsg);
		
		out.flush();
		
		message = ipMsg.readLine();
		html += message + "\n";
		
		splitMsg = message.split(" ");
		
		if (splitMsg[1].equals("200")) /* Page found. */
		{
			while((message = ipMsg.readLine()) != null)
			{
				if (message.contains("csrftoken"))
				{
					message = message.split("=")[1].trim();
					csrftoken = message.split(";")[0];
				}
				else if (message.contains("sessionid"))
				{
					message = message.split("=")[1].trim();
					sessionid = message.split(";")[0];
				}
				html += message;
			}
			//System.out.println(html);
			
			doc = Jsoup.parse(html);
			Elements inputs = doc.select("input");
			
			for (Element input : inputs)
			{
				if (input.attr("id").equals("id_username"))
					user_field = input.attr("name");
				
				if (input.attr("id").equals("id_password"))
					pass_field = input.attr("name");
				
				if (input.attr("name").equals("csrfmiddlewaretoken"))
					csrf_field = input.attr("name");
				
				if (input.attr("name").equals("next"))
				{
					next_link = input.attr("value");
					next_link = next_link.replaceAll("/", "%2F");
				}
			}
			
			Elements forms = doc.select("form");
			for (Element form : forms)
				if (form.attr("method").equals("post"))
					action = form.attr("action");
			
			data = user_field + "=" + username + "&" + pass_field + "=" + password;
			data += "&" + csrf_field + "=" + csrftoken + "&next=" + next_link;
			
			httpPost = "POST " + loginLink + " HTTP/1.1" + CRLF;
			httpPost += "Connection: keep-alive" + CRLF;
			//httpPost += "Cookie: csrfmiddlewaretoken=" + csrftoken + "; sessionid=" + sessionid + CRLF;
			//httpPost += "User-Agent: HTTPTool/1.1" + CRLF;
			httpPost += "Content-Type: application/x-www-form-urlencoded" + CRLF;
			httpPost += "Content-Length: " + data.length() + CRLF;
			httpPost += CRLF + data + CRLF;
			
			
			InetAddress inet = InetAddress.getByName(host);
			client = new Socket(inet , 80);
			
			out = new PrintWriter(client.getOutputStream(), true);
			
			isr = new InputStreamReader(client.getInputStream());
        	ipMsg = new BufferedReader(isr);
        	
			System.out.println(httpPost);
			out.write(httpPost);
			out.flush();
			
			ipMsg.r
			message = null;
			while((message = ipMsg.readLine()) != null)
				System.out.println(message);
			
		}
		else if (splitMsg[1].equals("301"))	/* Moved to new URL. */
		{
			// Code to move to new link.
			while((message = ipMsg.readLine()) != null)
			{
				System.out.println(message);
			}
			return;
		}
		else if (splitMsg[1].equals("403") || splitMsg[1].equals("404")) /* Page not found. */
		{
			System.out.println("Error Occurred : " + splitMsg[1]);
			return;
		}
		else if (splitMsg[1].equals("500")) /* Internal Server Error. */
		{
			System.out.println(" Trying Again.");
			makeHTTPConnection(host, username, password);
		}
		
	}
}
