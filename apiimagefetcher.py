from flask import Flask , render_template , request
import subprocess
from datetime import datetime , timedelta
import json

app = Flask(__name__)

@app.route('/')
def NASAAPI():
    return render_template('datepicker.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form

    NASA_API_KEY = "OwPmaQUMi6Cjhj1eR9XkdnYYgPuK4gRnHiJLhLIf"
    def get_apod_image(date):
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date}"
        curl_command = f'curl -s "{url}"'
        result = subprocess.run(curl_command , shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return None
    
    
    fromdate = request.form.get('fromdate')
    todate = request.form.get('todate')

    if fromdate and todate:
        try:
            fromdate = datetime.strptime(fromdate, "%Y-%m-%d")
            todate = datetime.strptime(todate, "%Y-%m-%d")

            current_date = fromdate
            results = []
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
                        'img' : image_url,
                        'titleofpic' : title,
                        'des' : explanation
                    }
                    results.append(template_data)
                    print(results)
                
                else:
                    print(f"failed to fetch data for {formatted_date}")

                current_date+= timedelta(days=1)
            
            return render_template('apiimageshow.html', results=results)
        except ValueError:
            print(" Invalid date format. Please use YYYY-MM-DD. ")
    else:
        print(" Please provide both 'From Date' and 'To Date'. ")

if __name__ == '__main__':
    app.run(debug=True)

    