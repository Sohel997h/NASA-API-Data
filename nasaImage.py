#!/usr/bin/python3

import cgi
import subprocess
import json
from urllib.parse import urlencode
from datetime import datetime , timedelta
from jinja2 import FileSystemLoader , Environment

NASA_API_KEY ="OwPmaQUMi6Cjhj1eR9XkdnYYgPuK4gRnHiJLhLIf"

def get_apod_image(date):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date}"
    curl_command =f'curl -s "{url}"'
    result = subprocess.run(curl_command , shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout
    else:
        return None
    
print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>NASA APOD Image Fetcher</title>')
print('</head>')
print('<body>')
print('<h1> NASA APOD Image Fetcher</h1>')

form = cgi.FieldStorage()

fromdate = form.getvalue('fromdate')
todate = form.getvalue('todate')

if fromdate and todate:
    try:
        fromdate = datetime.strptime(fromdate, "%Y-%m-%d")
        todate = datetime.strptime(todate, "%Y-%m-%d")

        current_date = fromdate
        while current_date <= todate:
            formatted_date = current_date.strftime("%Y-%m-%d")            
            response =get_apod_image(formatted_date)

            if response:
                data = json.loads(response)
                title = data['title']
                explanation = data['explanation']
                image_url = data['url'] 
                
                template_data = {
                    'date' : formatted_date ,
                    'img' : data['url'],
                    'titleofpic' : title,
                    'des' : explanation
                }
                environment = Environment(loader=FileSystemLoader("templates/"))
                template = environment.get_template("api.txt")
                rendered_template = template.render(template_data)
                print(rendered_template)
            
            else:
                print(f"<p>failed to fetch data for {formatted_date}</p>")

            current_date+= timedelta(days=1)
    except ValueError:
        print("<p> Invalid date format. Please use YYYY-MM-DD. </p>")
else:
    print("<p> Please provide both 'From Date' and 'To Date'. </p>")
print('</body>')
print('</html>')
