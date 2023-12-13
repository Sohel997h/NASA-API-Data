from flask import Flask , render_template , request
import requests
import json
from datetime import datetime , timedelta

app = Flask(__name__)

@app.route('/')
def NASAAPI():
    return render_template('datepicker.html')


@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form

        fromdate = request.form.get('fromdate')
        todate = request.form.get('todate')

        NASA_API_KEY ="OwPmaQUMi6Cjhj1eR9XkdnYYgPuK4gRnHiJLhLIf"
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&from_date={fromdate}&to_date={todate}"

        response = requests.get(url)
        nasa_images = response.json

        if fromdate and todate:
            try:
                fromdate = datetime.strptime(fromdate, "%Y-%m-%d")
                todate = datetime.strptime(todate, "%Y-%m-%d")

                current_date = fromdate
                results = []
                while current_date <= todate:
                    formatted_date = current_date.strftime("%Y-%m-%d")            
                    # response =nasa_images(formatted_date)
                    # print(response)

                    if response:
                        data = json.loads(response)
                        title = response['title']
                        explanation = response['explanation']
                        image_url = response['url'] 

                              
                        template_data = {
                            'date' : formatted_date ,
                            'img' : image_url,
                            'titleofpic' : title,
                            'des' : explanation
                        }
                        results.append(template_data)
                    #     print(template_data)
                    else:
                        print(f"failed to fetch data for {formatted_date}")
                    current_date+= timedelta(days=1)
            except ValueError:
                print(" Invalid date format. Please use YYYY-MM-DD. ")
    else:
        print(" Please provide both 'From Date' and 'To Date'. ")
   
    return render_template("api.txt", result = result, nasa_images = nasa_images)
    